import tkinter as tk
import csv

# Create the main window
root = tk.Tk()
root.title("Flashcards")
root.attributes('-topmost', True)
font = ('Helvetica', 26, 'bold')

# Read in the CSV file and store the data in a list of tuples
flashcards = []
with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        #skip the header row
        if reader.line_num == 1:
            continue
        
        flashcards.append((row[1], row[2]))

# Create variables to store the current flashcard and the current side (front or back)
current_flashcard = 0
current_side = "front"

# Create a label to display the current flashcard
label = tk.Label(root, text="", font=font)
label.pack()

# Create a function to update the label with the current flashcard
def update_label():
    global current_flashcard, current_side
    if current_side == "front":
        text = flashcards[current_flashcard][0]
    else:
        text = flashcards[current_flashcard][1]
    label.config(text=text)

# Create a function to flip to the next flashcard
def next_flashcard():
    global current_flashcard, current_side
    if current_side == "front":
        current_side = "back"
    else:
        current_side = "front"
        current_flashcard = (current_flashcard + 1) % len(flashcards)
    update_label()

# Create a button to flip to the next flashcard
button = tk.Button(root, text="Next", command=next_flashcard, font=font)
button.pack()



# Update the label with the first flashcard
update_label()

# Run the Tkinter event loop
root.mainloop()
