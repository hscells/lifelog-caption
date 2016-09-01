import pg8000, sys, os, argparse, json, re
from xml.dom import minidom


def innerText(element, name):
    return element.getElementsByTagName(name)[0].firstChild.nodeValue


def export_json(dataset, output):
    # parse the xml doc into a decent lookup table
    xmldoc = minidom.parse(dataset)
    images = xmldoc.getElementsByTagName('image')
    lookup = {}
    for image in images:
        path = innerText(image, 'image-path')
        id = path.split('/')[-1].split('.')[0]
        lookup[id] = path


    print("Connecting...")
    conn = pg8000.connect(user=os.environ.get("LIFELOG_DB_USER"),
                          password=os.environ.get("LIFELOG_DB_PASS"),
                          host=os.environ.get("LIFELOG_DB_HOST"),
                          database=os.environ.get("LIFELOG_DB_NAME"))
    cursor = conn.cursor()
    sql = 'SELECT i.name, a.annotation from annotated_text_images a JOIN images i ON a.image_id = i.id;'
    cursor.execute(sql)

    results = cursor.fetchall()
    data = []
    for row in results:
        id, caption = row
        caption = re.sub(r'(.)\.(.)', r'\1. \2', caption)
        if len(caption.strip()) > 0:
            data.append({'file_path': 'images/' + lookup[id].split("/")[-1], 'captions': [caption]})
    cursor.close()

    with open(output, 'w') as f:
        f.write(json.dumps(data, sort_keys=False, indent=2, separators=(',', ': ')))


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
