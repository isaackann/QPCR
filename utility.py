#!/usr/bin/env python3

''' Houses utility functions for GUI and QPCR algorithm 
 *  ________________________
 * < Here there be dragons! >
 *  ------------------------
 *                        \                    ^    /^
 *                         \                  / \  // \\
 *                          \   |\___/|      /   \//  .\\
 *                           \  /O  O  \__  /    //  | \ \           *----*
 *                             /     /  \/_/    //   |  \  \          \   |
 *                             @___@`    \/_   //    |   \   \         \/\ \\
 *                            0/0/|       \/_ //     |    \    \         \  \\
 *                        0/0/0/0/|        \///      |     \     \       |   |
 *                     0/0/0/0/0/_|_ /   (  //       |      \     _\     |   /
 *                  0/0/0/0/0/0/`/,_ _ _/  ) ; -.    |    _ _\.-~       /    /
 *                              ,-}        _      *-.|.-~-.           .~    ~
 *             \     \__/        `/\      /                 ~-. _ .-~      /
 *              \____(oo)           *.   }            {                   /
 *              (    (--)          .----~-.\        \-`                 .~
 *              //__\\  \__ Ack!   ///.----..<        \             _ -~
 *             //    \\               ///-._ _ _ _ _ _ _{^ - - - - ~
'''

import os
import csv 


''' Used for Terminal GUI text formatting '''
class ANSI:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    BRIGHT_RED = '\033[91m'
    GREEN = '\033[32m'
    BRIGHT_GREEN = '\033[92m'
    EXCEL = '\033[94m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    COLORS = ['\033[31m', '\033[32m', '\033[33m', '\033[94m', '\033[35m', '\033[36m', '\033[93m', '\033[96m']
    
    
''' Utility function that gets the CSV files in the QPCR CSV folder '''
def csvs_in_dir(dir):
    return [os.path.join(dir, csv) for csv in os.listdir(dir)]


''' Utility function that reads provided CSV for a certain primer, and gets 
all Cq values for that primer and its samples '''
def csv_to_dict(filename, primer_name):
    reader = csv.DictReader(open(filename))
    
    primer_dict = {primer_name: {}}
    
    for row in reader:
        if row['Target'] == primer_name:
            sample = row['Sample']
            Cq = float(row['Cq'])  # typecast from string into float
            
            # initialize empty list for sample Cq's
            if sample not in primer_dict[primer_name]:
                primer_dict[primer_name][sample] = []  

            primer_dict[primer_name][sample].append(Cq)
            
    return primer_dict


''' Utility function that reads a CSV for all unique primer types '''
def get_primers(filename):
    reader = csv.DictReader(open(filename))
    
    primers = []
    
    for row in reader:
        if row['Target'] not in primers: primers.append(row['Target'])
    
    return primers


''' Exports the nested expression level results dictionary into a 
new CSV file within the Results folder '''
def export_dict_to_csv(result, filename):
    csv_file = os.path.join('Results', filename)  # nested file
    rows = [] # flatten data into list of rows

    for key, inner_dict in result.items():  # O(n^3) D:
        for inner_key, values in inner_dict.items():
            for value in values:
                row = [key, inner_key] + [value]  # single expression level value
                rows.append(row)
            
    # write data to the new CSV
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Target', 'Sample', 'Expression Level'])  # header label
        writer.writerows(rows)

    print(f'{ANSI.BOLD}CSV file created and exported to Results folder successfully.{ANSI.RESET}')