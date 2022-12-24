import pyperclip
import os
import keyboard
import win32clipboard
import time
import xlwings as xw
from win32com.client import Dispatch
import pythoncom
import requests
import pandas as pd
import json
import tkinter as tk


def on_ctrl_c():
    # Wait for the clipboard to be populated
    time.sleep(0.1)
    # Open the clipboard
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    #convert data to utf-8
    #print what is currently in the clipboard
    
    
    # Close the clipboard
    win32clipboard.CloseClipboard()
  # Write the clipboard contents to the CSV file
    write_to_csv(data)
    
    


def write_to_csv(data):
    #if it doesn't exist, create the file using pandas
    cwd = os.getcwd()
    if not os.path.isfile(cwd + '/data.csv'):
        
        df = pd.DataFrame(columns=['data'])
        df.to_csv('data.csv', index=False)
    #append the data to the csv file in the first column last row
    
    df = pd.read_csv('data.csv')
    
    spanish = deepl_translate(data)
    #append the spanish translation to the csv file in the second column last row
    df = df.append({'english': data, 'spanish': spanish}, ignore_index=True)
    
    sp_en_response = [data, spanish]
    df.to_csv('data.csv', index=False)
    show_strings(sp_en_response)
    
def deepl_translate(data):
    api_key = 'b86af888-a93c-5c99-9e3e-684ddedf564d:fx'
    #take the data and translate it into Spanish
    url = 'https://api-free.deepl.com/v2/translate'
    params = {'auth_key': api_key, 'text': data, 'target_lang': 'ES'}
    response = requests.post(url, params=params)
    #convert the response to json
    json_text = json.loads(response.text)
    response_Text = json_text['translations'][0]['text']
    return response_Text
        

import tkinter as tk

def show_strings(strings):
    root = tk.Tk()
    root.title("Translation")
    root.attributes('-topmost', True)
    font = ('Helvetica', 36, 'bold')

    label1 = tk.Label(root, text=strings[0], font=font)
    label1.pack()
    label2 = tk.Label(root, text=strings[1], font = font)
    label2.pack()

    root.mainloop()

# Example usage


    
def main():
    # Set up a keyboard shortcut to trigger the on_ctrl_c function
    # when Ctrl + C is pressed
    keyboard.add_hotkey('ctrl+c', on_ctrl_c)
    # Keep the program running
    keyboard.wait()


if __name__ == '__main__':
    main()