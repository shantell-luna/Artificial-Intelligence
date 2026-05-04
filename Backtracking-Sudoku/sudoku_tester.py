#!/usr/bin/env python
#coding:utf-8

"""
Sudoku tester file.

Usage: python3 sudoku_tester.py

Notes:
    * This file expects a file named 'sudokus_start.txt' to be in the same directory, which
    contains one Sudoku puzzle per line
    * There should also be a corresponding 'sudokus_finish.txt' with solutions to the puzzles
    * Do NOT submit this file, only submit sudoku.py and README.txt

TO-DO: Time your run of the sudoku boards
"""

import sys
import time 
import statistics
from sudoku import *

def main():
    if len(sys.argv) > 1:
        print("Usage: python3 sudoku_tester.py")
        sys.exit(1)
    
    try:
        #  Read boards from test and solution files
        test_filename = "sudokus_start.txt"
        sol_filename = "sudokus_finish.txt"
        testfile = open(test_filename, "r")
        solfile = open(sol_filename, "r")

        try:
            test_list = testfile.read()
        except:
            print("Error reading the sudoku file %s" % test_list)
            exit()
        
        try:
            sol_list = solfile.read()
        except:
            print("Error reading the sudoku file %s" % sol_list)
            exit()

        # Setup puzzles and solutions
        puzzles = test_list.split("\n")
        solutions = sol_list.split("\n")

        # Solve each board using backtracking
        test_no = 1
        successes = []
        failures = []
        skips = []
        solve_times = []

        for puzzle_no in range(len(puzzles)):
            puzzle = puzzles[puzzle_no]

            if len(puzzle) < 9:
                skips.append(test_no)
                test_no += 1
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(puzzle[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Uncomment this for debugging.
            print_board(board)

            # Solve with backtracking
            t0 = time.perf_counter()
            solved_board = backtracking(board)
            dt = time.perf_counter() - t0
            solve_times.append(dt)

            # Print solved board. TODO: Uncomment this for debugging.
            print_board(solved_board)

            if board_to_string(solved_board) == solutions[puzzle_no]:
                successes.append(test_no)
            else:
                failures.append((test_no, solved_board))
            test_no += 1

            # Compute timing stats
            attempted_count = (test_no - 1) - len(skips)
            solved_count = len(successes)
            min_t = min(solve_times) if solve_times else 0.0
            max_t = max(solve_times) if solve_times else 0.0
            mean_t = statistics.mean(solve_times) if solve_times else 0.0
            # stdev requires at least 2 values
            std_t = statistics.stdev(solve_times) if len(solve_times) >= 2 else 0.0
            

        # Print results
        print("=== Sudoku Test Results ===")
        print("Test case count: %d" % (test_no - 1))
        print("Attempted:\t %d" % attempted_count)
        print("Successes:\t %d" % len(successes))

        if len(failures) == 0:
            print("Failures:\t 0")
        else:
            print("Failures:")
            for failure in failures:
                print("    - Board #%d\t- got %s" % (failure[0], board_to_string(failure[1])))

        if len(skips) == 0:
            print("Skipped:\t 0")
        if len(skips) > 0:
            print("Skipped:")
            for skip in skips:
                print("    - %d" % skip)

        print("\nTiming (seconds):")
        print("  min:  %.6f" % min_t)
        print("  max:  %.6f" % max_t)
        print("  mean: %.6f" % mean_t)
        print("  stdev:%.6f" % std_t)

        # Write README.txt with the required summary
        with open("README.txt", "w") as f:
            f.write("Sudoku Solver Results\n")
            f.write("=====================\n\n")
            f.write(f"Boards in sudokus_start.txt: {test_no - 1}\n")
            f.write(f"Attempted: {attempted_count}\n")
            f.write(f"Solved: {solved_count}\n")
            f.write(f"Failed: {len(failures)}\n")
            f.write(f"Skipped: {len(skips)}\n\n")

            f.write("Running time statistics (seconds):\n")
            f.write(f"  min:   {min_t:.6f}\n")
            f.write(f"  max:   {max_t:.6f}\n")
            f.write(f"  mean:  {mean_t:.6f}\n")
            f.write(f"  stdev: {std_t:.6f}\n\n")

    except FileNotFoundError:
        print("Error: 'sudokus_start.txt' file not found.")
        exit()

if __name__ == '__main__':
    main()