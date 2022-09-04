# inporting necessary modules
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import stats
from IPython.display import display
import pandas as pd
import csv

run_ID = input("Please enter Run ID: ")
date = input("Please enter the date: ")
operator = input("Please enter the operator(s): ")
method = input("Please enter the method: ")
analyte = input("Please enter the analyte: ")
excel_name = input("Please enter the excel file name: ")

# Import calibration data from excel and add to list format to be read by pandas
cal_data = pd.read_excel(f'{excel_name}.xlsx', sheet_name='Cal')
cal_concs = cal_data["cal_conc"].tolist()
cal_areas = cal_data["cal_area"].tolist()
cal_list_length = len(cal_concs)

# Create a list of log values for concentrations and area
cal_conc_log = []
for i in range(cal_list_length):
    cal_conc_log.append(math.log10(cal_concs[i]))
cal_area_log = []
for i in range(cal_list_length):
    cal_area_log.append(math.log10(cal_areas[i]))

# Return a table showing calibration values rounded to 2 d.p.
cal_table = pd.DataFrame({'Calibration Concentration': cal_concs, 'Calibration Area': cal_areas})
cal_table.round(decimals=2)

# Check if calibration values suitable and perform linear regression

# Use linregress module to calculate values from straight-line graph
slope, intercept, r_value, p_value, std_err = stats.linregress(cal_conc_log, cal_area_log)
r2_value = r_value ** 2

# Check R^2 value is suitable
if (r2_value > 0.95) and (r2_value < 1.05):
    print(f'Correlation coefficient is {r2_value} therefore acceptable')
else:
    print(f'Correlation coefficient is {r2_value} therefore unacceptable')

print()

# Check how accurate values for the area of each calibration value are
check_per_total = []
j = 0

for i in range(cal_list_length):
    check_per = ((10 ** ((cal_area_log[j] - intercept) / slope)) / cal_concs[j]) * 100

    # Notify the user if value is far from expected
    if (check_per < 90) or (check_per > 110):
        print(f'percentage difference for calibration concentration {cal_concs[j]} is {check_per}')
        # Let the user decide whether include this in calibration curve
        if input("If you want to exclude this from the calibration enter y: ") == "y":
            del cal_conc_log[j]
            del cal_area_log[j]
            del cal_concs[j]
            del cal_areas[j]
        else:
            check_per_total.append(check_per)
            j += 1
    else:
        check_per_total.append(check_per)
        j += 1

# Calculate the mean percentage difference of calibration expected v. obtained areas
total = 0
for i in check_per_total:
    total += i
mean = total / len(check_per_total)
print("The mean calculated percentage is: ", mean)

# Recalculate straight line values with updated data set which excludes anomolies
slope, intercept, r_value, p_value, std_err = stats.linregress(cal_conc_log, cal_area_log)

# Create linear regression line to plot
x = cal_conc_log[:]
y = []
for i in range(len(x)):
    y.append(slope * x[i] + intercept)

plt.plot(cal_conc_log, cal_area_log, 'r.')
plt.xlabel("log([MS])")
plt.ylabel("log(area)")
plt.title(f'Calibration curve for Run ID {run_ID}')
plt.plot(x, y)
# Add R value to plot
plt.annotate(
    f'R\u00b2 = {(r_value ** 2).round(decimals=4)} \n y = {slope.round(decimals=4)}x + {intercept.round(decimals=4)}',
    xy=(cal_conc_log[-1] / 3, cal_area_log[-1] / 4))
plt.savefig(f'{run_ID}_fig.pdf')
plt.show()

print(f'The Correlation coefficient is now {r_value ** 2}, congratulations!')

# Read in analyte data

# Analyte volume
vol = int(input("Enter the volume of the sample in ml: "))
#vol = 20

values_data = pd.read_excel(f'{excel_name}.xlsx', sheet_name='Values')
sample_label = values_data["sample"].tolist()
sample_value = values_data["area"].tolist()
cal_list_length = len(cal_concs)

# Calculate concentrations of analyte samples from their area
sample_value_log = []
result = []
result_perml = []

for i in range(len(sample_value)):
    sample_value_log.append(math.log10(sample_value[i]))
    result.append((10**((sample_value_log[i]-intercept)/slope))*vol)

for i in range(len(sample_value)):
    sample_value_log.append(math.log10(sample_value[i]))
    result_perml.append(10**((sample_value_log[i]-intercept)/slope))

# Results

# threshold = float(input("Enter threshold value to highlight: "))

# def colour_change(val):
#     if val > threshold:
#         colour = 'red'
#     else:
#         colour = 'black'
#     return 'color: % s' % colour

print("All samples and results: ")
results = pd.DataFrame({'Sample' : sample_label,'Result / μg' : result, 'Result/ μg ml-1' : result_perml})
print(results)
#results.style.applymap(colour_change, subset = 'Result / μg')

# positive_results = result[:]
# positive_labels = sample_label[:]

# k = 0
# for j in result:
#     if j < threshold:
#         del positive_results[k]
#         del positive_labels[k]
#     else:
#         k += 1

# print("Samples and results above threshold: ")
# positive = pd.DataFrame({'Sample' : positive_labels,'Result' : positive_results})
# positive.style

# Export results to excel-readable file
excel_writer = pd.ExcelWriter(f'{run_ID}_results.xlsx', engine='xlsxwriter')

num = range(1)
info = pd.DataFrame({'Number of tears': num, 'date' : date, 'operator' : operator, 'method' : method, 'analyte': analyte}) #, 'Threshold Value': threshold
info.to_excel(excel_writer, sheet_name='info', index = False)

cal_data = pd.DataFrame({'Concentrations' : cal_concs,'Area' : cal_areas})
cal_data.to_excel(excel_writer, sheet_name='cal data', index = False)

raw_results = pd.DataFrame({'Sample' : sample_label, 'Area' : sample_value})
raw_results.to_excel(excel_writer, sheet_name='raw_results', index=False)

results.to_excel(excel_writer, sheet_name='results', index = False)

# positive.to_excel(excel_writer, sheet_name='positive_results', index = False)

excel_writer.save()