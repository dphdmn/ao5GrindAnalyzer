import sys
import argparse
import os
RED = "\033[91m"
DARK_RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
SKIPPED_STRING = "Skipped"
DNF = 999999
DNS = 9999999
os.system('')
def classify_solves(solves, good_solve_threshold, ok_solve_threshold, overlappingAllowed):
    sequence_counts = [0, 0, 0, 0, 0]
    total_sequences = 0
    sequences_with_lucky = []

    i = 0
    while i < len(solves):
        if solves[i] < good_solve_threshold:
            total_sequences += 1
            lucky_counter = 0
            penalty = False
            current_sequence = [solves[i]]

            for j in range(1, 5):
                if i + j >= len(solves):
                    break

                current_sequence.append(solves[i + j])

                if solves[i + j] < ok_solve_threshold:
                    lucky_counter += 1
                else:
                    if penalty:
                        sequence_counts[lucky_counter] += 1
                        sequences_with_lucky.append((lucky_counter, current_sequence))
                        break
                    else:
                        penalty = True

            else:
                if not penalty:
                    sequence_counts[lucky_counter] += 1
                sequences_with_lucky.append((lucky_counter, current_sequence))
            if overlappingAllowed == 1:
                i += 1
            else:
                i += j
        else:
            i += 1

    return total_sequences, sequence_counts, sequences_with_lucky

def read_solves_from_file(file_path, ok_solve_threshold):
    solves = []
    completed_amount = 0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    time = parts[0]
                    completedString = parts[1]
                    completed = completedString.strip().upper() == 'TRUE'
                    if time == SKIPPED_STRING:
                        solve_time = DNS
                    else:
                        if completed:
                            solve_time = float(time)
                            completed_amount += 1
                        else:
                            solve_time = DNF
                    solves.append(solve_time)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data format in file. {e}")
        sys.exit(1)
    return solves, completed_amount

def format_and_print_sequence_counts(sequence_counts):
    labels = [
        "0 lucky solves",
        "1 lucky solve",
        "2 lucky solves",
        "3 lucky solves",
        "4 lucky solves"
    ]

    for i, count in enumerate(sequence_counts):
        print(f'{labels[i]}: {count}')

# Define the Ao5 calculation functions
def getAo5(sequence):
    sorted_sequence = sorted(sequence)
    return sum(sorted_sequence[1:-1]) / 3  # Exclude the best and worst, then calculate mean

def getWorstPossibleAo5(sequence):
    sorted_sequence = sorted(sequence)
    return sum(sorted_sequence[1:]) / 3  # Exclude the best, then calculate mean

def getBestPossibleAo5(sequence):
    sorted_sequence = sorted(sequence)
    return sum(sorted_sequence[:-1]) / 3  # Exclude the worst, then calculate mean


def main():
    parser = argparse.ArgumentParser(description='Classify sequences of solves.')
    parser.add_argument('--file', type=str, default='input.txt', help='Input file containing solves from oldest to latest. Format: "SOLVE_TIME{TAB}COMPLETED". SOLVE_TIME is a float or a string for skipped scrambles. COMPLETED is a string TRUE or FALSE. Separator is a TAB. Default file: "input.txt"')
    parser.add_argument('--good', type=float, default=0.4, help='Threshold for a good solve to start a sequence (for example, solve less than your average). Default: 0.4')
    parser.add_argument('--ok', type=float, default=0.5, help='Threshold for an ok solve (solve that you think would be nice for an average). Default: 0.5')
    parser.add_argument('--minlucky', type=int, default=1, help='Minimum amount of solves in sequnce to print (from 0 to 4). Default: 1') 
    parser.add_argument('--overlap', type=int, default=1, help='1 to allow sequence overlapping, 0 to not allow (can help finding certain averages). Default: 1') 
    args = parser.parse_args()
    minlucky = args.minlucky
    if minlucky < 0 or minlucky > 4:
        print("Error parsing minlucky, range must be between 0 and 4, which is amount of lucky solves, excluding the first one. Showing ALL solves (value 0)")
        minlucky = 0

    solves, completed_amount = read_solves_from_file(args.file, args.ok)
    print(f"\nAttempts amount: {len(solves)} (Completed: {completed_amount})")
    total_sequences, sequence_counts, sequences_with_lucky = classify_solves(solves, args.good, args.ok, args.overlap)
    sequences_with_lucky.sort(key=lambda x: x[0], reverse=True)

    print(f'Total Sequences (first solve good): {total_sequences}')
    format_and_print_sequence_counts(sequence_counts)

    print(f"\nSequences (min {minlucky}):")
    threshold = args.ok

    for lucky_counter, sequence in sequences_with_lucky:
        if lucky_counter >= minlucky:
            seq_len = len(sequence) - sequence.count(DNF) - sequence.count(DNS)
            colored_sequence = [
                f"{DARK_RED}_DNF_{RESET}" if num == DNF else
                f"{DARK_RED}_DNS_{RESET}" if num == DNS else
                f"{RED}{num:.3f}{RESET}" if num > threshold else
                f"{GREEN}{num:.3f}{RESET}"
                for num in sequence
            ]
            colored_sequence_str = "\t".join(colored_sequence)
            print(f"Lucky solves: {lucky_counter}: {colored_sequence_str}", end='')
            if seq_len == 5:
                ao5 = getAo5(sequence)
                print(f"\t[ao5: {ao5:.3f}]")
            elif seq_len == 4:
                worst_possible_ao5 = getWorstPossibleAo5(sequence)
                best_possible_ao5 = getBestPossibleAo5(sequence)
                if DNF in sequence and len(sequence) == 5:
                    print(f"\t[ao5: {best_possible_ao5:.3f}] (if slidysim allowed DNF/DNS)")
                else:
                    print(f"\t\t[BPA: {best_possible_ao5:.3f} / WPA: {worst_possible_ao5:.3f}]")
            elif seq_len == 3:
                if len(sequence) == 4:
                    best_possible_ao5 = getBestPossibleAo5(sequence)
                    print(f"\t\t[BPA: {best_possible_ao5:.3f} / WPA: inf]")
            else:
                print(f"\t\t[BPA: inf / WPA: inf]")


if __name__ == "__main__":
    main()
