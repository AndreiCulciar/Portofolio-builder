#!/usr/bin/env python
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Button, Text, END, ttk
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
    
    with open("C:/Users/andre/Proiect stocuri/q.pkl", "rb") as f:
        q = pickle.load(f)
    with open("C:/Users/andre/Proiect stocuri/a.pkl", "rb") as f:
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

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    
def printPositions():
    global canvas, text_box, toolbar, positions_output,q,a
    with open("C:/Users/andre/Proiect stocuri/q.pkl", "rb") as f:
        q = pickle.load(f)
    with open("C:/Users/andre/Proiect stocuri/a.pkl", "rb") as f:
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
    text_box = Text(root, height=15, width=100)
    # Show and update text box
    text_box.pack()
    text_box.delete('1.0', END) 
    for line in positions_output:
        text_box.insert(END, line + "\n")

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

def runs():
    loading_label.config(text="🔄 Extracting Stocks")
    root.update_idletasks()
    result = runpy.run_path("C:/Users/andre/Proiect stocuri/Untitled1.py")
    loading_label.config(text="✅ Done extracting Stocks")

    loading_label.config(text="🔄 Checking stock values")
    root.update_idletasks()
    result = runpy.run_path("C:/Users/andre/Proiect stocuri/Untitled2.py")
    loading_label.config(text="✅ Checked stock values")

    loading_label.config(text="🔄 Building portfolio")
    root.update_idletasks()
    result = runpy.run_path("C:/Users/andre/Proiect stocuri/Untitled3.py")
    loading_label.config(text="✅ Portfolio built")
 
    
def start_tasks():
    csv_files = glob.glob(os.path.join("C:/Users/andre/Proiect stocuri", "*.csv"))
    for file in csv_files:
        os.remove(file)
    threading.Thread(target=runs).start()
    
root = Tk()
root.title("Portfolio Pie Chart")
root.state("zoomed")

button = Button(root, command=printSomething, text="Show Portfolio Pie Chart")
button.pack()

button1 = Button(root, command=printPositions, text="Show Positions")
button1.pack()

loading_label = ttk.Label(root, text="Click 'Run' to start", font=('Arial', 12))
loading_label.pack(pady=20)
button2 = Button(root, command=start_tasks, text="Extractions")
button2.pack()

root.mainloop()




