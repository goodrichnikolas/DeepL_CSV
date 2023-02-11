
import pyperclip
import os
import keyboard as kyb
import win32clipboard
import time
import xlwings as xw
from win32com.client import Dispatch
import pythoncom
import requests
import pandas as pd
import json
import tkinter as tk
import webbrowser
import sys
import psutil
import logging
import pynput

#global variables
g_root = None
translation = None

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
    data = write_to_csv(data)
    # set global translation variable to data
    global translation
    translation = data
    #clear the clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    #clear the keyboard listener
    print('On Ctrl C done')
    return None
    


def write_to_csv(data):
    #if it doesn't exist, create the file using pandas
    cwd = os.getcwd()
    if not os.path.isfile(cwd + '/data.csv'):
        
        df = pd.DataFrame(columns=['data'])
        df.to_csv('data.csv', index=False, encoding='utf-8')
    #append the data to the csv file in the first column last row
    
    df = pd.read_csv('data.csv', encoding='utf-8')
    
    spanish = deepl_translate(data)
    #append the spanish translation to the csv file in the second column last row
    df = df.append({'english': data, 'spanish': spanish}, ignore_index=True)
    
    sp_en_response = [data, spanish]
    df.to_csv('data.csv', index=False, encoding = 'utf-8')
    return sp_en_response
    
    
def deepl_translate(data):
    api_key = 'API'
    #take the data and translate it into Spanish
    url = 'https://api-free.deepl.com/v2/translate'
    params = {'auth_key': api_key, 'text': data, 'target_lang': 'ES'}
    response = requests.post(url, params=params)
    #convert the response to json
    json_text = json.loads(response.text)
    response_Text = json_text['translations'][0]['text']
    return response_Text
     

    
def main():
    def open_website():
        webbrowser.open("https://www.deepl.com/translator")
    
    def close_window():
        #end the program and then restart it
        #close window
        
        root.destroy()
    
    def on_press(key):
        #pynput.keyboard.Key for q
        if key == pynput.keyboard.Key.esc:
            close_window()
    
    # Set up a keyboard shortcut to trigger the on_ctrl_c function
    # when Ctrl + C is pressed
    #close any Tkinter root windows that are open
        
    #clear any keyboard listeners that are open
    
    print('Starting program')
    kyb.add_hotkey('ctrl+c', on_ctrl_c)
    # Wait for the user to press Ctrl + C
    kyb.wait('ctrl+c')
    
        
    # Create the Tkinter GUI
    root = tk.Tk()
    root.title("Translation")
    root.attributes('-topmost', True)
    font = ('Helvetica', 26, 'bold')

    label1 = tk.Label(root, text=translation[0], font=font)
    label1.pack()
    label2 = tk.Label(root, text=translation[1], font=font)
    label2.pack()
    label3 = tk.Label(root, text="Press 'q' to close", font=font)
    label3.pack()

    button = tk.Button(root, text="Go to website", font=font, command=open_website)
    button.pack()

    # Start the keyboard listener
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()

    # Start the Tkinter GUI's main loop
    root.mainloop()

    # Stop the keyboard listener
    listener.stop()
    try:
        kyb.unhook_all()
    except:
        pass
    try:
        kyb.unhook_all_hotkeys()
    except:
        pass        


if __name__ == '__main__':
   main()
   os.execv(sys.executable, ['python'] + sys.argv)
    


