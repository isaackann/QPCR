#!/usr/bin/env python3

""" Isaac Kan QPCR Algorithm
    ------------------------
    This file should not be run - run the qpcr_gui.py file instead!
    Contains implementation of algorithm that calculates expression levels from QPCR data (in spreadsheet)
    Reads CSV file, parses data, and applies calculations. Creates some nice graphs for each primer at the end! 
    The calculated results and graphs are saved in the Images & Results folders 
"""

import pandas as pd, plotly.express as px 
import numpy as np
import utility as ut


""" Gets the average Cq value for a sample group, for the control primer's samples """
def ctrl_primer_analysis(filename, ctrl_primer):
    ctrl_primer_dict = ut.csv_to_dict(filename, ctrl_primer)
    
    # converts the list of control primer Cq's into an average, grouped by sample
    avg_ctrl_dict = {ctrl_primer: {}}
    
    for sample, cq_list in ctrl_primer_dict[ctrl_primer].items():
        avg = sum(cq_list) / len(cq_list)
        avg_ctrl_dict[ctrl_primer][sample] = round(avg, 3)
        
    return avg_ctrl_dict


""" Calculates dCt value for a primer's samples by subtracting average Cq of the 
control primer's matching samples from the primer's sample's Cqs"""
def get_dct(filename, primer, ctrl_primer, avg_dict):
    primer_dict = ut.csv_to_dict(filename, primer)
    results = {}  # dict to return
    
    # subtract all of primer's cq values by corresponding cq average from control
    for sample, cq_list in primer_dict[primer].items():
        if sample not in avg_dict[ctrl_primer]: avg = 0  # error correction
        else: avg = avg_dict[ctrl_primer][sample]
        
        # create new cq_list with list comprehension
        results[sample] = [round(cq - avg, 3) for cq in cq_list]
        
    return {primer: results}


""" Calculates ddCts for a primer by subtracting the dCt of the primer's control sample
from the dCt's of its non-control samples """
def get_ddct(primer, ctrl_sample, primer_dict):
    sample_dict = primer_dict[primer]
    
    sampleCtrl_avg = round(sum(sample_dict[ctrl_sample]) / len(sample_dict[ctrl_sample]), 3)
    
    for cq_list in sample_dict.values():
        for i in range(len(cq_list)):  # directly edit list elements
            cq_list[i] = round(cq_list[i] - sampleCtrl_avg, 3)

    return {primer: sample_dict}


""" Calculates expression level with the formula 2^(-ddCt)"""
def get_exp_level(ddct_dict, primer):
    inner = ddct_dict[primer]
    
    for cq_list in inner.values():
        for i in range(len(cq_list)):  # directly edit list elements again
            cq_list[i] = round(pow(2, -1 * cq_list[i]), 3)
            
    return {primer: inner}


""" Takes in CSV filename, control primer, and control sample from user input
Creates dictionary of expression levels for each category """
def qpcr_analysis(filename, ctrl_primer, ctrl_sample):
    ctrl_avg_dict = ctrl_primer_analysis(filename, ctrl_primer)
    primers = ut.get_primers(filename)  # find all non-control primers
    primers.remove(ctrl_primer)
    
    results = {primer:{} for primer in primers}
    
    # populate results dictionary
    for primer in primers:
        dct = get_dct(filename, primer, ctrl_primer, ctrl_avg_dict)
        ddct = get_ddct(primer, ctrl_sample, dct)
        exp = get_exp_level(ddct, primer)
        
        results[primer] = exp[primer]
    
    # visualize results
    for primer in primers: visualize(results, primer, filename)
    
    return results


""" Draws graphs for a specific primer using the pyplot library """
def visualize(results_dict, primer, filename):
    primer_dict = results_dict[primer]  # data for the specific primer we're looking at
    
    samples = list(primer_dict.keys())  # gets sample groups, average expression levels, and the standard deviation
    exp_levels = [round(np.mean(primer_dict[sample]), 3) for sample in samples]
    errors = [np.std(primer_dict[sample]) for sample in samples]
    
    df = pd.DataFrame(data={'Sample Name': samples, 'Expression Level': exp_levels})  # saves data as a dataframe
    fig = px.bar(df, x='Sample Name', y='Expression Level', error_y=errors, color=samples, title=f'{primer} Expression Levels ({filename[5:]})')
    
    for i in range(len(samples)):  # adds the expression level values on top of the bar chart
        offset = exp_levels[i] + errors[i] + max(errors) * 0.3
        fig.add_annotation(x=samples[i], y=offset, text=str(exp_levels[i]), showarrow=False, font=(dict(color='black')))
        
    fig.update_layout(title_font_size=20, legend_title='Samples', width=1000, height=700)  # formatting
    fig.update_xaxes(title_font_size=15)
    fig.update_yaxes(title_font_size=15)

    fig.write_image(f'images/{primer} {filename[5:-4]}.png')  # saves image to folder
    fig.show()  # we're done!


def main():
    files = ut.csvs_in_dir('CSVs')
    
    # one test case
    result = qpcr_analysis(files[1], 'GAPDH', 'sgCtrl')
    print(result)
    

if __name__ == "__main__":
    main()
