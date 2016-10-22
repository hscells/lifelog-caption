from xml.dom import minidom

import argparse
import json
import os
import pg8000
import re
import sys


def inner_text(element, name):
    return element.getElementsByTagName(name)[0].firstChild.nodeValue


def export_json(dataset, output):
    # parse the xml doc into a decent lookup table
    xmldoc = minidom.parse(dataset)
    images = xmldoc.getElementsByTagName('image')
    lookup = {}
    for image in images:
        path = inner_text(image, 'image-path')
        image_id = path.split('/')[-1].split('.')[0]
        lookup[image_id] = path

    print("Connecting...")
    conn = pg8000.connect(user=os.environ.get("LIFELOG_DB_USER"),
                          password=os.environ.get("LIFELOG_DB_PASS"),
                          host=os.environ.get("LIFELOG_DB_HOST"),
                          database=os.environ.get("LIFELOG_DB_NAME"))
    cursor = conn.cursor()
    tables = ['annotated_text_images', 'annotated_query_images', 'annotated_tag_images']

    for table in tables:
        sql = 'SELECT i.name, a.annotation ' \
              'FROM {} a ' \
              'JOIN images i ON a.image_id = i.id;'.format(table)
        cursor.execute(sql)

        results = cursor.fetchall()
        data = []
        for row in results:
            image_id, caption = row
            if table in ['annotated_text_images', 'annotated_query_images']:
                caption = str(re.sub(r'(.)\.(.)', r'\1. \2', caption)).strip()
                if len(caption) > 0:
                    captions = caption.split('.')
                    captions = list(
                        filter(None, [x.replace(',', '').strip() for x in captions]))
            else:
                captions = caption
            if len(captions) > 0:
                image_name = lookup[image_id].split("/")[-1]
                data.append({'file_path': '/neuraltalk2/flat-images/' + image_name,
                             'captions': captions, 'id': image_name.split('.')[0]})

        with open('{}-{}'.format(table, output), 'w') as f:
            f.write(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))
    cursor.close()


if __name__ == '__main__':
    if os.environ.get("LIFELOG_DB_USER") is None or \
                    os.environ.get("LIFELOG_DB_PASS") is None or \
                    os.environ.get("LIFELOG_DB_HOST") is None or \
                    os.environ.get("LIFELOG_DB_NAME") is None:
        print("Environment variables are not set!")
        sys.exit(1)

    argparser = argparse.ArgumentParser(description='Creating training dataset')
    argparser.add_argument('dataset', help='The NTCIR lifelog dataset')
    argparser.add_argument('output', help='The file to output the json data to')
    args = argparser.parse_args()

    export_json(args.dataset, args.output)
