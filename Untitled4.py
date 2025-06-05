#!/usr/bin/env python
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Button, Text, END, ttk, Frame
from matplotlib.figure import Figure
import papermill as pm
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import ipywidgets as widgets
from IPython.display import display, clear_output
import threading
import time
import asyncio
import sys
import runpy
import pickle
import os
import glob
 

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# In[3]:


canvas = None
text_box = None
positions_output = []
toolbar = None 

def printSomething():
    global canvas, text_box, toolbar, positions_output,q,a
    
    with open(f"{os.getcwd()}/q.pkl", "rb") as f:
        q = pickle.load(f)
    with open(f"{os.getcwd()}/a.pkl", "rb") as f:
        a = pickle.load(f)

    try:
        if canvas:
            canvas.get_tk_widget().destroy()
        if text_box:
            text_box.destroy()
        if toolbar:
            toolbar.destroy()
    except:
        pass
    
    positions_output = []
    for i in range(len(q)):
        var = q[i]
        line = f"{a[i]} {'Long' if var > 0 else 'Short'}  {var * 100:.4f}"
        positions_output.append(line)
        
    labels = []
    values = []
    colors = []
    for line in positions_output:
        parts = line.split()
        ticker = parts[0]
        position_type = parts[1]
        value = float(parts[2])
        
        labels.append(f"{ticker} {position_type}")
        values.append(abs(value))
        colors.append('#76c893' if position_type == 'Long' else '#ff6b6b')
    
    fig = Figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title('Portfolio Allocation: Long vs Short Positions')
    ax.axis('equal')

    # Create and pack canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    loading_label.config(text="🔄 Building portfolio")
    root.update_idletasks()
    result = runpy.run_path(f"{os.getcwd()}/Untitled3.py")
    loading_label.config(text="✅ Portfolio built")
    
    
def printPositions():
    global canvas, text_box, toolbar, positions_output,q,a
    try:
        if canvas:
            canvas.get_tk_widget().destroy()
        if text_box:
            text_box.destroy()
        if toolbar:
            toolbar.destroy()
    except:
        pass

    positions_output = []
    for i in range(len(q)):
        var = q[i]
        line = f"{a[i]} {'Long' if var > 0 else 'Short'}  {var * 100:.4f}"
        positions_output.append(line)
    text_box = Text(root, height=15, width=100)
    # Show and update text box
    text_box.pack()
    text_box.delete('1.0', END) 
    for line in positions_output:
        text_box.insert(END, line + "\n")
    with open(f"{os.getcwd()}/q.pkl", "rb") as f:
        q = pickle.load(f)
    with open(f"{os.getcwd()}/a.pkl", "rb") as f:
        a = pickle.load(f)

def run_notebook(notebook_path):
    print(f"Running {notebook_path}\n")
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb)
    print(f"Executed {notebook_path}\n")

    # Loop through cells and print outputs
    for cell in nb.cells:
        for output in cell.get('outputs', []):
            if output.output_type == 'stream':
                print(output.text)
    loading_label.config(text="🔄 Building portfolio")
    root.update_idletasks()
    result = runpy.run_path(f"{os.getcwd()}/Untitled3.py")
    loading_label.config(text="✅ Portfolio built")

def runs():
    loading_label.config(text="🔄 Extracting Stocks")
    root.update_idletasks()
    result = runpy.run_path(f"{os.getcwd()}/Untitled1.py")
    loading_label.config(text="✅ Done extracting Stocks")

    loading_label.config(text="🔄 Checking stock values")
    root.update_idletasks()
    result = runpy.run_path(f"{os.getcwd()}/Untitled2.py")
    loading_label.config(text="✅ Checked stock values")

    stock_label.config(text="Number of Stocks")
    perf_label.config(text="Performance")
    
 
def get_input():
    number_of_stocks = int(entry_numberofstocks.get())
    performanta=int(entry_performanta.get())/256/100
    with open(f"{os.getcwd()}/number_of_stocks.pkl", "wb") as f:
        pickle.dump(number_of_stocks, f)
    stock_label.config(text="✅ Number of Stocks")
    with open(f"{os.getcwd()}/performanta.pkl", "wb") as f:
        pickle.dump(performanta, f)
    perf_label.config(text="✅ Performance")
    
    
def start_tasks():
    csv_files = glob.glob(os.path.join(os.path.dirname(os.path.join(os.getcwd(), "q.pkl")), "*.csv"))
    for file in csv_files:
        os.remove(file)
    threading.Thread(target=runs).start()
    
root = Tk()
root.title("Portfolio Pie Chart")
root.state("zoomed")

# Left
left_frame = Frame(root)
left_frame.pack(side='left', anchor='n', padx=20, pady=20)

stock_label = ttk.Label(left_frame, text="Number of Stocks:", font=('Arial', 12))
stock_label.pack(anchor='w', pady=5)
entry_numberofstocks = ttk.Entry(left_frame,width=10)
entry_numberofstocks.pack(anchor='w', pady=5)

perf_label = ttk.Label(left_frame, text="Performance:", font=('Arial', 12))
perf_label.pack(anchor='w', pady=5)
entry_performanta = ttk.Entry(left_frame,width=10)
entry_performanta.pack(anchor='w', pady=5)

button3 = Button(left_frame, text="Submit", command=lambda: print("Submitted"))
button3.pack(anchor='w', pady=10)

# Top
top_frame = Frame(root)
top_frame.pack(side='top', pady=10)

button = Button(top_frame, command=lambda: print("Show Chart"), text="Show Portfolio Pie Chart")
button.pack(pady=5)

button1 = Button(top_frame, command=lambda: print("Show Positions"), text="Show Positions")
button1.pack(pady=5)

loading_label = ttk.Label(top_frame, text="Click 'Run' to start", font=('Arial', 12))
loading_label.pack(pady=5)

button2 = Button(top_frame, command=lambda: print("Run Extractions"), text="Extractions")
button2.pack(pady=5)


root.mainloop()




