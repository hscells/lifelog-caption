# python 3

import argparse, json, re

# data_regex = re.compile(r'.*\"(.*)\".*:(.*)\n')
image_regex = re.compile(r'\".*/(.*).jpg\"')
caption_regex = re.compile(r': (.*)\n')


def parse(input_file, output_file):

    with open(input_file, 'r') as f:
        data = f.read()

    images = image_regex.findall(data)
    captions = caption_regex.findall(data)
    parsed_data = dict(zip(images, captions))
    print(parsed_data)

    with open(output_file, 'w') as f:
        f.write(json.dumps(parsed_data, sort_keys=False, indent=2, separators=(',', ': ')))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parse and output the evaluation data')
    argparser.add_argument('input', help='The input text file')
    argparser.add_argument('output', help='The JSON file to output to')
    args = argparser.parse_args()

    parse(args.input, args.output)
