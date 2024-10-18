# SAT Solver - Incremental Search
# This script generates random well-formed formulas (WFFs) and tests each for satisfiability.
# The test returns "Satisfiable" (S) or "Unsatisfiable" (U), and the time it took to determine the result.
# A WFF is expressed as a list of lists, where each inner list is a clause, and each integer in a clause is a literal.
# A positive literal (e.g., 3) indicates that the clause is satisfied if the corresponding variable (var 3) is true.
# A negative literal (e.g., -3) indicates that the clause is satisfied if the corresponding variable is false.
# A clause is satisfiable if at least one of its literals is true. A WFF is satisfiable if all its clauses are satisfiable.
# An assignment is a list of values (0 or 1) for n variables, where 0 means False and 1 means True.

import time
import random
import matplotlib.pyplot as plt

# Following is an example of a wff with 3 variables, 3 literals/clause, and 4 clauses
Num_Vars=3
Num_Clauses=4
wff=[[1,-2,-2],[2,3,3],[-1,-3,-3],[-1,-2,3],[1,2,-3]]


# Following is an example of a wff with 3 variables, 3 literals/clause, and 8 clauses
Num_Clauses=8
wff=[[-1,-2,-3],[-1,-2,3],[-1,2,-3],[-1,2,3],[1,-2,-3],[1,-2,3],[1,2,-3],[1,2,3]]

#  read WFF from a file
def read_wff_from_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        Nvars = int(lines[0].strip())  # Number of variables
        Nclauses = int(lines[1].strip())  # Number of clauses
        wff = []
        for line in lines[2:]:
            clause = list(map(int, line.strip().split())) # Extract clause
            wff.append(clause)
    return Nvars, Nclauses, wff

# write results to a file
def write_results_to_file(output_file, timing_data):
    with open(output_file, 'a') as file:
        for size, exec_time, sat_flag in timing_data:
            result = 'Satisfiable' if sat_flag else 'Unsatisfiable'
            file.write(f"Problem Size: {size}, Execution Time: {exec_time} microseconds, Result: {result}\n")

#  incrementally check satisfiability
def check_incremental(Wff, Nvars, Nclauses):
    Assignment = [0] * (Nvars + 1) # all false assignment

    # helper function to check if current assignment satisfies the WFF
    def is_satisfiable(Assignment):
        for clause in Wff:
            satisfied = False
            for literal in clause:
                if literal > 0 and Assignment[literal] == 1:
                    satisfied = True
                    break
                elif literal < 0 and Assignment[-literal] == 0:
                    satisfied = True
                    break
            if not satisfied:
                return False
        return True
    
    # Try all 2^Nvars assignments and check for satisfiability
    for i in range(2 ** Nvars):
        if is_satisfiable(Assignment):
            return True, Assignment
        
        # Increment assignment to the next possible combination
        for j in range(1, Nvars + 1):
            Assignment[j] ^= 1  # Flip the bit 
            if Assignment[j] == 1:
                break
    
    return False, Assignment

# build random WFF
def build_wff(Nvars, Nclauses, LitsPerClause):
    wff = []
    for i in range(Nclauses):
        clause = []
        for j in range(LitsPerClause):
            var = random.randint(1, Nvars)
            if random.randint(0, 1) == 0: 
                var = -var
            clause.append(var)
        wff.append(clause)
    return wff

# test the given WFF and measure execution time
def test_wff(wff, Nvars, Nclauses):
    start = time.time()  # Start timer
    SatFlag, Assignment = check_incremental(wff, Nvars, Nclauses)
    end = time.time()  # End timer
    exec_time = int((end - start) * 1e6)  # Execution time in microseconds
    return wff, Assignment, SatFlag, exec_time

# plot timing results from the data
def plot_timing_results(timing_data):
    x_yes = [size for size, time, sat in timing_data if sat]
    y_yes = [time for size, time, sat in timing_data if sat]

    x_no = [size for size, time, sat in timing_data if not sat]
    y_no = [time for size, time, sat in timing_data if not sat]

    plt.scatter(x_yes, y_yes, color='green', label='Satisfiable (Yes)', marker='o')
    plt.scatter(x_no, y_no, color='red', label='Unsatisfiable (No)', marker='x')

    plt.xlabel('Problem Size (Number of Variables)')
    plt.ylabel('Execution Time (microseconds)')
    plt.title('SAT Solver Timing by Problem Size')
    plt.legend()
    plt.show()

#run the SAT solver for multiple problem sizes and trials
def run_sat_solver(input_file, output_file, plot_results=True):
    timing_data = []
    
    # read problem sizes from input file
    Nvars, Nclauses, wff = read_wff_from_file(input_file)

    random.seed(42)
    problem_sizes = [5, 7, 11, 15, 19, 21, 23]

    # run multiple trials for each problem size 
    for size in problem_sizes:
        for trial in range(0, 20, 3):
            wff = build_wff(size, size * 4, 3)
            results = test_wff(wff, size, size * 2)
            timing_data.append((size, results[3], results[2]))

    # Write results to output file
    write_results_to_file(output_file, timing_data)

    # If plotting is enabled, plot timing results
    if plot_results:
        plot_timing_results(timing_data)

# Example usage:
input_file = 'data_aarnett2.txt'
output_file = 'output_aarnett2.txt'
run_sat_solver(input_file, output_file)

