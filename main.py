BACKGROUND_COLOR = "#B1DDC6"
import pandas
from tkinter import *
import random

current_word = {}
to_learn = {}
# -----------------------PICK RANDOM WORD-------------------#


try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient='records')




def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    canvas.itemconfig(word_text, text=current_word['French'], fill='black')
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text='French', fill='black')
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_word)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv('data/words_to_learn.csv', index=False)



def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(word_text, text=current_word['English'])
    canvas.itemconfig(title_text, text='English')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashcard")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
wrong = PhotoImage(file='images/wrong.png')
right = PhotoImage(file='images/right.png')
canvas_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 163, text="Title", fill="black", font=("Courier", 40, 'italic'))
word_text = canvas.create_text(400, 263, text="Word", fill="black", font=("Courier", 54, 'bold'))
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
right_button = Button(image=right, highlightthickness=0, command=is_known)
canvas.grid(row=0, column=0, columnspan=2)
wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)
next_card()

window.mainloop()
