import sys
import argparse

def classify_solves(solves, good_solve_threshold, ok_solve_threshold):
    sequence_counts = [0, 0, 0, 0, 0]
    total_sequences = 0

    i = 0
    while i < len(solves):
        if solves[i] < good_solve_threshold:
            total_sequences += 1
            lucky_counter = 0
            penalty = False

            for j in range(1, 5):
                if i + j >= len(solves):
                    break

                if solves[i + j] < ok_solve_threshold:
                    lucky_counter += 1
                else:
                    penalty = True

                if penalty:
                    sequence_counts[min(lucky_counter, 4)] += 1
                    break
            else:
                # If we completed the loop without a break (all 4 solves are OK)
                if i + 4 < len(solves) and solves[i + 4] < ok_solve_threshold:
                    lucky_counter += 1

                sequence_counts[min(lucky_counter, 4)] += 1

            i += j
        else:
            i += 1

    return total_sequences, sequence_counts

def read_solves_from_file(file_path, ok_solve_threshold):
    solves = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    completed = parts[1].strip().upper() == 'TRUE'
                    if completed:
                        solve_time = float(parts[0])
                    else:
                        solve_time = ok_solve_threshold
                    solves.append(solve_time)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data format in file. {e}")
        sys.exit(1)
    return solves

def format_and_print_sequence_counts(sequence_counts):
    labels = [
        "No lucky solves (reset after 3 solves)",
        "1 lucky solve (reset after 4 solves)",
        "2 lucky solves (painful reset after 5 solves)",
        "3 lucky solves (ao5!)",
        "4 lucky solves (very good ao5!)"
    ]

    for i, count in enumerate(sequence_counts):
        print(f'{labels[i]}: {count}')


def main():
    parser = argparse.ArgumentParser(description='Classify sequences of solves.')
    parser.add_argument('--file', type=str, default='input.txt', help='Input file containing solves from oldest ot latest. Format: "SOLVE_TIME{TAB}COMPLETED". SOLVE_TIME is a float or a string for skipped scrambles. COMPLETED is a string TRUE or FALSE. Separator is a TAB.')
    parser.add_argument('--good', type=float, default=0.4, help='Threshold for a good solve to start a sequence (for example, solve less than your average.')
    parser.add_argument('--ok', type=float, default=0.5, help='Threshold for an ok solve (solve that you think would be nice for an average)')

    args = parser.parse_args()

    solves = read_solves_from_file(args.file, args.ok)
    total_sequences, sequence_counts = classify_solves(solves, args.good, args.ok)

    print(f'Total Sequences (first solve good): {total_sequences}')
    format_and_print_sequence_counts(sequence_counts)

if __name__ == "__main__":
    main()