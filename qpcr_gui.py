#!/usr/bin/env python3

""" Contains GUI to run the QPCR algorithm. 
You can run this file by typing 'python3 qpcr_gui.py' in the Python terminal """

import utility as ut
import qpcr as q

file_index = ''
print(f'{ut.ANSI.BOLD}{ut.ANSI.UNDERLINE}Enter \'END\' to end program{ut.ANSI.RESET}')

files = ut.csvs_in_dir('CSVs')

while True:
    print(f'\n{ut.ANSI.BOLD}CSV Files:{ut.ANSI.RESET}')  # display available CSVs
    for i in range(len(files)): print(f'{i + 1}. {ut.ANSI.EXCEL}{files[i][5:]}{ut.ANSI.RESET}')
    
    file_index = input(f'Please enter {ut.ANSI.GREEN}CSV filename number{ut.ANSI.RESET} (e.g. 1, 2 ...) or enter \'END\': ') 
    if file_index == 'END': break  # end loop
    
    filename = files[int(file_index) - 1]
    
    primers = ut.get_primers(filename)
    ctrl_primer = ''
    
    while ctrl_primer == '':  # error correction
        new_input = input(f'Please enter {ut.ANSI.CYAN}control primer{ut.ANSI.RESET} (e.g. GAPDH): ')
        if new_input in primers: ctrl_primer = new_input
        else: print(f'{ut.ANSI.BRIGHT_RED}Please enter a valid primer from the CSV{ut.ANSI.RESET}')
    
    avg_dict = q.ctrl_primer_analysis(filename, ctrl_primer)
    samples = list(avg_dict[ctrl_primer].keys())
    ctrl_sample = ''
    
    while ctrl_sample == '':  # error correction
        new_input = input(f'Please enter {ut.ANSI.MAGENTA}control sample {ut.ANSI.RESET}(e.g. sgCtrl): ')
        if new_input in samples: ctrl_sample = new_input
        else: print(f'{ut.ANSI.BRIGHT_RED}Please enter a valid sample group from the CSV{ut.ANSI.RESET}')
        
    result = q.qpcr_analysis(filename, ctrl_primer, ctrl_sample)  # we made it!        
    
    print(f'{ut.ANSI.BOLD}Images saved to Images folder{ut.ANSI.RESET}')  # exported the data
    ut.export_dict_to_csv(result, filename[5:])