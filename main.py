import ctypes
import random
import tkinter
from tkinter import *
from sentences import possibleTexts


ctypes.windll.shcore.SetProcessDpiAwareness(1)

flag = True
time_remaining = 60
mistakes = 0
letter_index = -1
value = ""
typed_words = []
text = ''
ResultLabel: tkinter.Label
ResultButton: tkinter.Button
textbox: tkinter.Text
time_left: tkinter.Label
entry: tkinter.Entry


letters = '''. a b c d e f g h i j k l m n o p q r s t u v w x y z space A B C D E F G H I J K L M N O P Q R S T U V W X Y Z , ? ! " ' \ / [ ] { } = + _ - ( ) * & ^ % $ # @ 0 1 2 3 4 5 6 7 8 9 < > ` ~'''

window = Tk()
window.geometry('700x600')

photo = PhotoImage(file='795.png')
window.iconphoto(False, photo)
window.title('Typing Speed Test')
window.config(bg='white')


def keypress(event=None):
    global flag, value, letter_index, mistakes

    if event.char != '':
        try:
            value = entry.get()
        except ValueError:
            value = ""
        try:
            if event.char in letters:
                letter_index += 1

            expected_value = textbox.get("1.0", "end")

            if expected_value[letter_index] == event.char:
                textbox.tag_add("right", f"1.{letter_index}")
                textbox.tag_remove("wrong", f"1.{letter_index}")
            else:
                mistakes += 1
                textbox.tag_add("wrong", f"1.{letter_index}")
                textbox.tag_remove("right", f"1.{letter_index}")

        except tkinter.TclError:
            pass


def clear_text(event=None):
    keypress(event)

    if entry.get() != '' and entry.get() != ' ':
        typed_words.append(entry.get())
    if value == text.split()[-1] or value == " " + text.split()[-1]:
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.configure(state="disabled")
    entry.delete(0, "end")


def back(_event):
    global letter_index
    if value != "" and value != " ":
        textbox.tag_remove("wrong", f"1.{letter_index}")
        textbox.tag_remove("right", f"1.{letter_index}")
        letter_index -= 1


def stop_test():
    global ResultLabel, ResultButton

    time_left.destroy()
    textbox.destroy()
    entry.destroy()

    ResultLabel = Label(text=f'Words per Minute: {len(typed_words)}', fg='black', bg='white')
    ResultLabel.pack(pady=20)

    ResultButton = Button(text='Retry', command=restart_typing, bg='black', fg='white', relief='flat')
    ResultButton.pack(pady=20)


def restart_typing():
    global ResultLabel, ResultButton, time_remaining, letter_index
    ResultLabel.destroy()
    ResultButton.destroy()

    time_remaining = 60
    letter_index = -1
    start_typing()


def minus_second():
    global time_remaining
    if time_remaining > 0:
        time_remaining -= 1
        time_left.config(text=f'{time_remaining} sec remaining')

        if flag:
            window.after(1000, minus_second)


def start_typing():
    global entry, textbox, time_left, text

    window.after(61000, stop_test)
    window.after(1000, minus_second)
    text = random.choice(possibleTexts)
    time_left = Label(text=f'{time_remaining} sec remaining', font=("Product Sans", 13, "normal"), bg='white')
    time_left.pack(padx=20, pady=(20, 10))

    textbox = Text(width=80, height=10, relief='flat', font=('Product Sans', 12, 'normal'), wrap='word')
    textbox.pack(padx=40, pady=(30, 0))
    textbox.insert(chars=text, index="1.0")
    textbox.tag_config("wrong", foreground='#FF1A98')
    textbox.tag_config("right", foreground="#5EFF42")
    textbox.config(state='disabled')

    entry = Entry(width=20, relief='solid', font=('Product Sans', 12, 'normal'))
    entry.focus()
    entry.pack()

    entry.bind("<Key>", keypress)
    entry.bind("<space>", clear_text)
    entry.bind("<BackSpace>", back)

start_typing()

window.mainloop()
