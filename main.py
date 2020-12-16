import argparse
from dataclasses import dataclass


@dataclass
class ProgramData:
    input_file: str
    output_file: str
    map_output_file: str
    port: str


def parse_cmd_args():
    parser = argparse.ArgumentParser()
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input_file", help="input shapefile", required=True)
    required.add_argument("-o", "--output_file", help="text file for saving results", required=True)
    required.add_argument("-m", "--map_output_file", help="file for saving colored map", required=True)
    required.add_argument("-p", "--port", help="port where board is connected", required=True)
    parser._action_groups.append(optional)
    args = parser.parse_args()
    return ProgramData(args.input_file, args.output_file, args.map_output_file, args.port)

print(parse_cmd_args())