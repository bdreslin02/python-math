import numpy as np
import pandas as pd 
import scipy.stats as stats
import matplotlib.pyplot as plot
from scipy.interpolate import make_interp_spline
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def import_data(file_path): 
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print("Error reading the file:", e)
        return None
    
def user_input_data():
    group1_data = entry_group1.get()
    group2_data = entry_group2.get()

    try:
        group1 = [float(x.strip()) for x in group1_data.split(',')]
        group2 = [float(x.strip()) for x in group2_data.split(',')]
        return group1, group2
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input data. Please enter numeric values separated by commas.")
        return None, None

def choose_data_source():
    source_choice = data_source_var.get()

    if source_choice == "User Input":
        group1, group2 = user_input_data()
        if group1 is not None and group2 is not None:
            perform_t_test(group1, group2)
    elif source_choice == "Input Data":
        file_path = filedialog.askopenfilename(title="Select CSV/Excel file")
        if file_path:
            data = import_data(file_path)
            if data is not None: 
                group1 = data['Group 1'].values
                group2 = data['Group 2'].values 
                perform_t_test(group1, group2)
    else:
        messagebox.showerror("Input Error", "Please choose a data source.")

def perform_t_test(group1, group2):
    try:
        levene_stat, levene_p = stats.levene(group1, group2)
        levene_stat = round(levene_stat, 3)
        levene_p = round(levene_p, 3)

        t_stat, t_p = stats.ttest_ind(group1, group2)

        equality_of_variances = levene_p > 0.05
        t_test_significant = t_p < 0.05

        mean_group1 = round(np.mean(group1), 3)
        std_group1 = round(np.std(group1, ddof = 1), 3)
        mean_group2 = round(np.mean(group2), 3)
        std_group2 = round(np.std(group2, ddof = 1), 3)

        descriptive_stats = pd.DataFrame({
            'Group 1': [mean_group1, std_group1],
            'Group 2': [mean_group2, std_group2]
        }, index = ['Mean', 'Standard Deviation'])

        result_text = "Descriptive Statistics:\n" + str(descriptive_stats) + "\n"
        result_text += "\nLevene's Test for Equality of Variances:\n"
        result_text += f"Levene Statistic: {levene_stat}\n"
        result_text += f"Levene p-value: {levene_p}\n\n"
        result_text += "Inferential Statistics:\n"
        result_text += f"t-statistic: {round(t_stat, 3)}\n"
        result_text += f"t-test p-value: {round(t_p, 3)}\n\n"
        result_text += "Results of hypothesis testing:\n"

        if equality_of_variances:
            if t_test_significant:
                result_text += "Equality of variances: Passed, groups are homogenous\nT-Test: Significant"
            else:
                result_text += "Equality of variances: Passed, groups are homogenous\nT-Test: Not significant"
        else:
            result_text += "Equality of variances: Failed, groups are not homogenous\nT-Test: Not performed"

        result_var.set(result_text)

        plot.figure(figsize = (8, 6))
        plot.subplot(2, 1, 1)
        x_smooth = np.linspace(1, len(group1), 300)
        spl = make_interp_spline(range(1, len(group1) + 1), group1, k = 3)
        y_smooth = spl(x_smooth)
        plot.plot(x_smooth, y_smooth, color = 'b')
        plot.title("Group 1 Data")
        plot.xlabel("Data Point")
        plot.ylabel("Value")
        plot.grid(True)

        plot.figure(figsize = (8, 6))
        plot.subplot(2, 1, 2)
        x_smooth = np.linspace(1, len(group2), 300)
        spl = make_interp_spline(range(1, len(group2) + 1), group2, k = 3)
        y_smooth = spl(x_smooth)
        plot.plot(x_smooth, y_smooth, color = 'r')
        plot.title("Group 2 Data")
        plot.xlabel("Data Point")
        plot.ylabel("Value")
        plot.grid(True)

        plot.tight_layout()

        plot.show()
    except Exception as e: 
        result_var.set("Error performing t-test:\n" + str(e))

# Create a GUI window
window = tk.Tk()
window.title("T-Test Results")

# Create a variable to store data source choice
data_source_var = tk.StringVar()
data_source_var.set("User Input")

# Create and place input fields and labels
label_data_source = ttk.Label(window, text = "Select Data Source:")
label_data_source.grid(row = 0, column = 0, padx = 5, pady = 5)
data_source_menu = ttk.OptionMenu(window, data_source_var, "User Input", "Import Data")
data_source_menu.grid(row = 0, column = 1, padx = 5, pady = 5)

label_group1 = ttk.Label(window, text = "Group 1 Data:")
label_group2 = ttk.Label(window, text = "Group 2 Data")

entry_group1 = ttk.Entry(window, width = 40)
entry_group2 = ttk.Entry(window, width = 40)

label_group1.grid(row = 1, column = 0, padx = 5, pady = 5)
entry_group1.grid(row = 1, column = 1, padx = 5, pady = 5)
label_group2.grid(row = 2, column = 0, padx = 5, pady = 5)
entry_group2.grid(row = 2, column = 1, padx = 5, pady = 5)

# Create a button to calculate statistics
calculate_button = ttk.Button(window, text = "Run independent-samples t-test", command = choose_data_source)
calculate_button.grid(row = 3, column = 0, columnspan = 2, padx = 5, pady = 10)

# Create a label to display the results
result_var = tk.StringVar()
result_label = ttk.Label(window, textvariable=result_var, wraplength = 600)
result_label.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 5)

# Start the GUI application
window.mainloop()