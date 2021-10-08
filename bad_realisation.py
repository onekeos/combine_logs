import ast
import time

filename1 = 'log_a.jsonl'
filename2 = 'log_b.jsonl'

start = time.time()

print('Start')

with open(filename1, 'r') as f1, open(filename2, 'r') as f2, open('log.txt', 'w') as f3:
    f1_lines = f1.readlines()
    f2_lines = f2.readlines()
    last_f2_index = 0
    last_f1_index = 0
    for f1_index in range(len(f1_lines) - 1):
        left_bound = ast.literal_eval(f1_lines[f1_index])['timestamp']
        right_bound = ast.literal_eval(f1_lines[f1_index + 1])['timestamp']
        under = []
        upper = []
        for f2_index in range(last_f2_index, len(f2_lines)):
            value = ast.literal_eval(f2_lines[f2_index])
            if value['timestamp'] > right_bound:
                last_f2_index = f2_index
                break

            if f2_index == len(f2_lines) - 1:
                last_f2_index = f2_index + 1
                break

            append_val = f2_lines[f2_index] if '\n' in f2_lines[f2_index] else f2_lines[f2_index] + '\n'

            if value['timestamp'] < left_bound:
                under.append(append_val)
            else:
                upper.append(append_val)

        f3.write(''.join([*under, f1_lines[f1_index], *upper]))

    else:
        last_f1_index = f1_index
        f3.write(f1_lines[-1])

    if last_f2_index == len(f2_lines) - 1:
        for line in range(last_f1_index, len(f1_lines)):
            f3.write(f1_lines[line])
    else:
        for line in range(last_f2_index, len(f2_lines)):
            f3.write(f2_lines[line])

print('End', time.time() - start)
