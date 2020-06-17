import csv
import json
import argparse

parser = argparse.ArgumentParser(description='Converts a csv file to a json file')
parser.add_argument('input', metavar='input', type=str, nargs=1, help='the input csv file')
parser.add_argument('output', metavar='output', type=str, nargs=1, help='the output csv file')


def main(arguments: argparse.Namespace):
    input_filename = arguments.input[0]
    output_filename = arguments.output[0]

    json_data = list()

    with open(input_filename, "r") as input_file:
        reader = csv.reader(input_file)

        keys = next(reader)

        for line in reader:
            json_line = {key: value for key, value in zip(keys, line)}
            json_data.append(json_line)

    with open(output_filename, "w") as output_file:
        json_string = json.dumps(json_data, sort_keys=True, indent=4)
        output_file.write(json_string)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
