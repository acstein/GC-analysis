# inporting necessary modules
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import stats
from IPython.display import display
import pandas as pd
import csv

cal_list_length = int(input("please enter number of calibration values: "))

cal_concs = []
for i in range(cal_list_length):
    cal_concs.append(float(input("Please enter calibration concentration in microgram per ml: ")))

cal_areas = []
for i in range(cal_list_length):
    cal_areas.append(float(input(f"Please enter area for calibration value {cal_concs[i]}: ")))

# Create a list of log values for concentrations and area
cal_conc_log = []
for i in range(cal_list_length):
    cal_conc_log.append(math.log10(cal_concs[i]))

cal_area_log = []
for i in range(cal_list_length):
    cal_area_log.append(math.log10(cal_areas[i]))

df = pd.DataFrame({'Calibration Concentration': cal_concs, 'Calibration Area': cal_areas})
df.round(decimals=2)
