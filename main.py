import pandas as pd
import csv
import tkinter as tk
import threading
import time
import socket
import esp


# threading to receive live data
def start_tracking():
    threading.Thread(target=esp.receive_data(), daemon=True).start()


window = tk.Tk() # instantiate an instance of a window
window.geometry('500x500')
window.title('FE Car Data')

#icon = PhotoImage() ##changes icon in top corner

frame = tk.Frame(window)
frame.config(width=250, height=250, borderwidth=2, relief='sunken')
frame.pack()

time_label = tk.Label(frame, text='Time:')
time_label.pack()

#time_var = tk.StringVar(value = testdata.iat[-1, 0])
#time_data = tk.Label(frame, textvariable = time_var)
#time_data.pack(pady = 20)

start_button = tk.Button(frame, text="Start Tracking", command=start_tracking)
start_button.pack()



window.mainloop() # places window in computer screen
