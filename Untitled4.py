#!/usr/bin/env python
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Button, Text, END, ttk, Frame
from matplotlib.figure import Figure
import papermill as pm
import pandas as pd
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

    # ``````````````````````````````````````````````````````````
    loading_label.config(text="🔄 Building portfolio")
    root.update_idletasks()
    root.update()
    result = runpy.run_path(f"{os.getcwd()}/Untitled3.py")
    loading_label.config(text="✅ Portfolio built")
    # ``````````````````````````````````````````````````````````
    
    global canvas, text_box, toolbar, positions_output,q,a
    
    with open(f"{os.getcwd()}/q.pkl", "rb") as f:
        q = pickle.load(f)
    with open(f"{os.getcwd()}/a.pkl", "rb") as f:
        a = pickle.load(f)

    if canvas:
        canvas.get_tk_widget().destroy()
    if text_box:
        text_box.destroy()
    if toolbar:
        toolbar.destroy()
    
    positions_output = []
    data = []
    for i in range(len(q)):
        var = q[i]
        line = f"{a[i]} {'Long' if var > 0 else 'Short'}  {var * 100:.4f}"
        positions_output.append(line)
        # ``````````````
        allocation = round(var * 100, 4)
        data.append({
        "Allocation (%)": allocation})
        # ``````````````
    pd.DataFrame(data).to_csv("portfolio_allocations.csv", index=False)
    runpy.run_path(f"{os.getcwd()}/Untitled5.py")
    with open(f"{os.getcwd()}/b.pkl", "rb") as f:
        b = pickle.load(f)
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
    b_value = int(b.iloc[0]) if isinstance(b, pd.Series) else int(b[0])
    fig.text(0.5, 0.05, f"Performanta portofoliului: {b_value - 100}", 
         ha='center', fontsize=10, color='black')
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title('Portfolio Allocation: Long vs Short Positions')
    ax.axis('equal')

    # Create and pack canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
def printPositions():
    
    loading_label.config(text="🔄 Building portfolio")
    root.update_idletasks()
    root.update()
    result = runpy.run_path(f"{os.getcwd()}/Untitled3.py")
    loading_label.config(text="✅ Portfolio built")
    
    global canvas, text_box, toolbar, positions_output,q,a
    with open(f"{os.getcwd()}/q.pkl", "rb") as f:
        q = pickle.load(f)
    with open(f"{os.getcwd()}/a.pkl", "rb") as f:
        a = pickle.load(f)
    if canvas:
        canvas.get_tk_widget().destroy()
    if text_box:
        text_box.destroy()
    if toolbar:
        toolbar.destroy()
    

    positions_output = []
    
    with open(f"{os.getcwd()}/suma.pkl", "rb") as f:
        suma = pickle.load(f)
    
    for i in range(len(q)):
        var = q[i]
        line = f"{a[i]} {'Long' if var > 0 else 'Short'}  {var * 100:.2f}%  {suma*var:.2f}"
        positions_output.append(line)
        
    
    text_box = Text(root, height=15, width=100)
    
    # Show and update text box
    text_box.pack()
    text_box.delete('1.0', END) 
    for line in positions_output:
        text_box.insert(END, line + "\n")
        

def runs():
    loading_label.config(text="🔄 Extracting Stocks")
    root.update_idletasks()
    result = runpy.run_path(f"{os.getcwd()}/Untitled1.py")
    loading_label.config(text="✅ Done extracting Stocks")
    root.update_idletasks()
    loading_label.config(text="🔄 Checking stock values")
    root.update_idletasks()
    result = runpy.run_path(f"{os.getcwd()}/Untitled2.py")
    loading_label.config(text="✅ Checked stock values")

    
    
 
def get_input():
    number_of_stocks = int(entry_numberofstocks.get())
    performanta=int(entry_performanta.get())/256/100
    suma=int(entry_suma.get())
    
    stock_label.config(text="Number of Stocks")
    perf_label.config(text="Performance")
    suma_label.config(text="Suma")
    
    with open(f"{os.getcwd()}/number_of_stocks.pkl", "wb") as f:
        pickle.dump(number_of_stocks, f)
    stock_label.config(text="✅ Number of Stocks")
    root.after(3000, lambda: stock_label.config(text="Number of Stocks"))
    
    with open(f"{os.getcwd()}/performanta.pkl", "wb") as f:
        pickle.dump(performanta, f)
    perf_label.config(text="✅ Performance")
    root.after(3000, lambda: perf_label.config(text="Performance"))
    
    with open(f"{os.getcwd()}/suma.pkl", "wb") as f:
        pickle.dump(suma, f)
    suma_label.config(text="✅ Suma")
    root.after(3000, lambda: suma_label.config(text="Suma"))

    
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

suma_label = ttk.Label(left_frame, text="Suma:", font=('Arial', 12))
suma_label.pack(anchor='w', pady=5)
entry_suma = ttk.Entry(left_frame,width=10)
entry_suma.pack(anchor='w', pady=5)

button3 = Button(left_frame, text="Submit", command=get_input)
button3.pack(anchor='w', pady=10)

# Top
top_frame = Frame(root)
top_frame.pack(side='top', pady=10)

button = Button(top_frame, command=printSomething, text="Show Portfolio Pie Chart")
button.pack(pady=5)

button1 = Button(top_frame, command=printPositions, text="Show Positions")
button1.pack(pady=5)

loading_label = ttk.Label(top_frame, text="Click 'Run Extractions' to start", font=('Arial', 12))
loading_label.pack(pady=5)

button2 = Button(top_frame, command=runs, text="Run Extractions")
button2.pack(pady=5)


root.mainloop()





