import csv

# Data to write to the CSV file
data_old = {'ifnb': {'sgCtrl': [0.938, 0.866, 1.232], 'sgCtrl dox': [40.113, 46.174, 52.82], 'sgSNRPA_1': [12.826, 13.214, 13.15], 
                 'sgSNRPA_2': [12.571, 15.412, 11.306], 'sgSNRPD1_1': [9.063, 8.568, 9.856], 'sgSNRPD1_2': [11.584, 14.774, 17.827]}, 
        'isg15': {'sgCtrl': [0.963, 0.767, 1.352], 'sgCtrl dox': [119.428, 127.116, 133.436], 'sgSNRPA_1': [10.042, 10.454, 11.089], 
                  'sgSNRPA_2': [8.907, 10.182, 9.626], 'sgSNRPD1_1': [7.295, 8.374, 7.057], 'sgSNRPD1_2': [17.667, 17.388, 15.552]}, 
        'mda5': {'sgCtrl': [1.039, 0.966, 0.997], 'sgCtrl dox': [314.083, 336.159, 321.795], 'sgSNRPA_1': [367.347, 366.076, 328.102], 
                 'sgSNRPA_2': [336.859, 305.282, 283.46], 'sgSNRPD1_1': [291.025, 318.688, 221.629], 'sgSNRPD1_2': [357.55, 350.191, 283.46]}, 
        'oas2': {'sgCtrl': [0.319, 3.055, 1.027], 'sgCtrl dox': [629.909, 935.763, 741.858], 'sgSNRPA_1': [38.827, 20.266, 49.936], 
                 'sgSNRPA_2': [27.531, 22.612, 20.478], 'sgSNRPD1_1': [29.836, 26.52, 31.823], 'sgSNRPD1_2': [69.551, 59.056, 20.337]}}

data = {
    'ifnb': {
        'sgCtrl': [0.938, 0.866, 1.232],
        'sgCtrl dox': [40.113, 46.174, 52.82],
        'sgSNRPA_1': [12.826, 13.214, 13.15],
        'sgSNRPA_2': [12.571, 15.412, 11.306],
        'sgSNRPD1_1': [9.063, 8.568, 9.856],
        'sgSNRPD1_2': [11.584, 14.774, 17.827]
    }
}

# Path to CSV file
csv_file = "example.csv"

# Flatten data into a list of rows
rows = []

for key, inner_dict in data_old.items():
    for inner_key, values in inner_dict.items():
        for value in values:
            row = [key, inner_key] + [value]
            rows.append(row)
        
# Write the data to the CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(['Target', 'Sample', 'Cq'])  # header label
    writer.writerows(rows)

print("CSV file created and exported successfully.")
