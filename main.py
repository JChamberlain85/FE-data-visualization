import pandas as pd
import csv
import tkinter as tk
import threading
import time

testdata = pd.read_csv('fe_sample.csv')

def update_data():
    while True:
        testdata = pd.read_csv('fe_sample.csv')  # Fetch latest price
        time_var.set(f"{testdata.iat[-1, 0]} seconds")  # Update label with current data
        #time.sleep(5)  # Update every 5 seconds

# threading to receive live data
def start_tracking():
    threading.Thread(target=update_data, daemon=True).start()

row_count = sum(1 for row in testdata)

window = tk.Tk() # instantiate an instance of a window
window.geometry('500x500')
window.title('FE Car Data')

#icon = PhotoImage() ##changes icon in top corner

frame = tk.Frame(window)
frame.config(width=250, height=250, borderwidth=2, relief='sunken')
frame.pack()

time_label = tk.Label(frame, text='Time:')
time_label.pack()

time_var = tk.StringVar(value = testdata.iat[-1, 0])
time_data = tk.Label(frame, textvariable = time_var)
time_data.pack(pady = 20)

start_button = tk.Button(frame, text="Start Tracking", command=start_tracking)
start_button.pack()



window.mainloop() # places window in computer screen