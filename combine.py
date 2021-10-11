import time
import argparse
import os
import json


def _combine(filename1: str, filename2: str, output_dir: str) -> None:
    start: int = int(time.time())

    print('Start combine')

    with open(filename1, 'r') as f1, \
            open(filename2, 'r') as f2, \
            open(output_dir + f"/{start}.jsonl", 'w') as f3:

        file_1: list = f1.readlines()
        file_2: list = f2.readlines()
        f1_index: int = 0
        f2_index: int = 0

        while f1_index < len(file_1):
            f1_value: str = json.loads(file_1[f1_index])['timestamp']
            while f2_index < len(file_2):
                f2_value: str = json.loads(file_2[f2_index])['timestamp']
                if f1_value <= f2_value:
                    f3.write(file_1[f1_index])
                    break
                else:
                    f3.write(file_2[f2_index])
                f2_index += 1
            f1_index += 1
        else:
            f3.write('\n')
            if f1_index < len(file_1) - 1:
                for index in range(f1_index, len(file_1)):
                    f3.write(file_1[index])
            else:
                for index in range(f2_index, len(file_2)):
                    f3.write(file_2[index])

    print('Combine ended', time.time() - start)


def main() -> None:
    parser = argparse.ArgumentParser(description='Program for union 2 log files')
    parser.add_argument('files', nargs=2, help='Filenames to combine')
    parser.add_argument('-o', '--output', default=os.getcwd(), help='Output dir')
    filenames = parser.parse_args()
    filename1, filename2 = filenames.files
    output_dir = filenames.output
    error_message: list = []

    if not os.path.isfile(filename1):
        error_message.append(f'File {filename1} not found')

    if not os.path.isfile(filename2):
        error_message.append(f'File {filename2} not found')

    if not os.path.exists(output_dir):
        error_message.append(f'Directory {output_dir} not found')

    if error_message:
        print('\n'.join(error_message))
    else:
        _combine(filename1, filename2, output_dir)


if __name__ == '__main__':
    main()
