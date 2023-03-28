import math
import time
import tkinter as tk
from datetime import date
import tkinter.font
from PIL import ImageTk
import speech_recognition as sr
from chatbot import generate_response
import pyttsx3
import threading
import numpy as np
#engine.say("")
#root.geometry('300x500')
root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=700)
canvas.grid(columnspan=1, rowspan=4)
import os
from sentiment_model import prediction
ask = 0
questions = ['Are you afraid of anyone?',
'What happens when you do something your parents don’t like?',
'do you have any secrets? If yes then does it hurt while playing?',
'while playing does someone touches your bump,lip, chest or shame part?',
'how are you feeling today?',
'anyone hurt you??',
'Is anything worrying you?',
'What are you doing during recess? Who are you spending time with?',
'How is your body feeling? Are you having stomach or headaches?',
'Is it easy for you to fall asleep?',
'Is something making you scared?',
'Do you have any problem paying attention?'
'Do you feel sad?',
'Have you been feeling strange',
'Is something bothering you?',
'Who are your friends now? What do you do with them?',
'Does anyone bother you at school? Has anyone hit you?',
'Has anything really frightening happened to you?']
#file delete after 30 days
folder = "daily_details" #change the path
max_age_days = 30

current_time = time.time()
cutoff_time = current_time - (max_age_days * 86400)

for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path):
        file_time = os.path.getmtime(file_path)
        if file_time < cutoff_time:
            os.remove(file_path)
#check whether folder is present or not if not then create it
new_folder = "daily_details"

if not os.path.exists(new_folder):
    os.makedirs(new_folder)


#check whether the file is present or not if not then create it
filename = f"{date.today()}.txt"
directory = "path"
if not os.path.exists("daily_details/" + filename):# Change the directory
    fp = open("daily_details/" + filename, 'x')
    fp.close()
#........................................................DAILY_ANALYSIS......................................................................



def call():
#...........................................................HELPER.............................................................................................
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox('all'))


    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def scrollbar(master, canvas):
        scrollbar = tk.Scrollbar(master, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return scrollbar


    def read_file(directory):
        t1 = os.listdir(directory)
        data = []
        for temp in t1:
            with open(os.path.join(directory, temp), 'r') as f:
                temp2 = [line.strip() for line in f.readlines()]
                data.append(temp2)
                f.close()
        print(data)
        return data


    def create_table(data):
        table = tk.Frame(canvas)
        table.pack(side=tk.TOP, padx=15, pady=10)
        tk.Label(table, text='Conversation', font=('Arial', 27, 'bold'), bg='black', fg='white').grid(row=0, column=0, padx=200, pady=15)
        tk.Label(table, text='Percentage', font=('Arial', 27, 'bold'), bg='black', fg='white').grid(row=0, column=1, padx=200, pady=15)
        per_add = 0
        take_this = 1
        for y in data:
            for i, line in enumerate(y):
                parts = line.split(':')
                conversation = parts[0]
                #print(conversation)
                try:
                    percentage = parts[1].strip()
                    try:
                        percentage = float(percentage)
                        per_add += percentage
                    except ValueError:
                        continue
                except:
                    continue
                tk.Label(table, text=f'{take_this}. {conversation}', font=('Arial', 14), bg='black', fg='white').grid(row=take_this, column=0, sticky='w', padx=5, pady=5)
                tk.Label(table, text=f'{percentage:.2f}', font=('Arial', 14), bg='black', fg='white').grid(row=take_this, column=1,
                                                                                                         padx=5, pady=5)
                take_this += 1
        org_len = 0
        org_len2 = 0
        for y in data:
            sub = 0
            for tmp in y:
                if len(tmp.split(';')) > 1:
                    sub += 1
            org_len2 += len(y) - sub
            org_len += len(y)
        avg_percentage = round(per_add/org_len2, 2)
        tk.Label(table, text='Average Percentage:', font=('Arial', 12, 'bold'), bg='black', fg='white').grid(row=org_len+1, column=0, padx=5, pady=5, sticky='e')
        tk.Label(table, text=f'{avg_percentage:.2f}', font=('Arial', 12), bg='black', fg='white').grid(row=org_len+1, column=1, padx=5, pady=5, sticky='w')

        return table
#...........................................................................................................................................
    root4 = tk.Tk()
    root4.title('Table from File')
    root4.geometry("{0}x{1}+0+0".format(root4.winfo_screenwidth(), root4.winfo_screenheight()))
    root4.configure(bg='black')
    root4.tk_setPalette(background='black', foreground='white')

    canvas = tk.Canvas(root4)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = scrollbar(root4, canvas)
    canvas.configure(yscrollcommand=scrollbar.set)

    data = read_file('daily_details')
    table = create_table(data)

    canvas.create_window((0, 0), window=table, anchor='nw')

    table.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'))

    canvas.bind('<Configure>', update_scroll_region)
    canvas.bind_all('<MouseWheel>', on_mousewheel)

    root4.mainloop()


#.......................................................File Management.......................................................................
#check whether folder is present or not if not then create it
'''new_folder = "daily_details"

if not os.path.exists(new_folder):
    os.makedirs(new_folder)


#check whether the file is present or not if not then create it
filename = f"{date.today()}.txt"
directory = "path"  # Change the directory'''

def file_handling(text):
    t1 = os.listdir("daily_details")
    filename = t1[-1]
    if os.path.exists("daily_details/" + filename) is True:
        with open("daily_details/" + filename, "a") as f:
            #with open(filename, "a") as f:
            f.write(text + "\n")
            f.close()




'''#file delete after 30 days
folder = "daily_details" #change the path
max_age_days = 30

current_time = time.time()
cutoff_time = current_time - (max_age_days * 86400)

for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path):
        file_time = os.path.getmtime(file_path)
        if file_time < cutoff_time:
            os.remove(file_path)'''



#..........................................................Helper Functions...................................................................................
def words(txt):
    count = 0
    for y in txt:
        if y == ' ':
            count += 1
    return count

def get_screen1(path):
    root.destroy()
    root2 = tk.Tk()
    def say(arr):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 120)
        engine.say(*arr)
        engine.runAndWait()
        engine.startLoop(False)
#............................................Animation (DO NOT INTERFERE)..........................................................
    temp = os.listdir(path)
    im = []
    for y in temp:
        im.append(ImageTk.PhotoImage(file=path + '/' + y))
    frames = len(im)
    count = 0
    anim = None
    gif_label = tk.Label(image='')
    gif_label.pack()
    def animation(count, start, inital, max_reps):
        if inital >= max_reps and count % 22 == 0:
            return
        if start is True:
            global anim
            im2 = im[count]

            gif_label.configure(image=im2)
            count += 1
            if count == frames:
                count = 0
            anim = root2.after(40, lambda: animation(count % 22, start, inital+1, max_reps))

#......................................CHAT BUTTON (DO NOT INTERFERE).........................................................
    img2 = ImageTk.PhotoImage(file="Frames-1/frame0.jpg")
    limg = Label(root2, i=img2)
    limg.pack()
    text = tk.Text(root2, height=4, width=50, foreground='#ffffff', background='black',
                   font=font_2, )
    global ask
    text.place(x=80, y = 500)
    button = tk.Button(root2, text="Enter", background='black', foreground='white', font=font_1
                       ,width=5, height=2, command=lambda: query_process(text.get(1.0, "end-1c")))
    button.place(x=10, y=500)
    button2 = tk.Button(root2, text="Mic", background='black', foreground='white', font=font_1
                       , width=5, height=2, command=lambda: get_speech())
    button2.place(x=10, y=600)
    def query_process(query):
        global ask
        ask += 1
        flag = False
        if ask % 2 == 0 and len(questions) > 0:
            flag = True
            say1 = "Totally random, but Before i answer you, can you answer something for me"
            selection = np.random.randint(0, len(questions))
            say1 = say1  + ", " + questions[selection]
            say2 = [say1]
            threading.Thread(target=animation,args=(0, True, 0, math.floor((words(say1) / 2.5 * 0.88) * 22))).start()
            say(say2)
            r = sr.Recognizer()
            with sr.Microphone() as source:
                data = r.listen(source=source)
            try:
                text1 = r.recognize_google(data)
                file_handling(questions[selection] + "Answer ; " + text1 + " :0")
                questions.pop(selection)
            except:
                pass
        answer = generate_response(query)
        if flag is True:
            answer_ = 'Thank you for answering my question, now answering your question '
            answer = answer_ + answer
        answer2 = [answer]
        #print(len(answer))
        threading.Thread(target=animation, args=(count, True, 0,math.floor((words(answer)/2.5*0.88)*22))).start()
        threading.Thread(target=say, args=(answer2,)).start()
        #animation(count, True, 0, 22)
        #engine.say(answer)
        #engine.runAndWait()
        sentiment, conf = prediction(query)
        print(sentiment, conf)
        if sentiment == 'positive':
            file_handling(query + " :" + str(round(conf*100, 2)))
        elif sentiment == 'negative':
            file_handling(query + " :" + "-"+str(round(conf*100, 2)))
        else:
            file_handling(query + " :0")
    def get_speech():
        global ask
        r = sr.Recognizer()
        with sr.Microphone() as source:
            data = r.listen(source=source)
        try:
            text1 = r.recognize_google(data)
            #print(text1)
            query_process(text1)
        except:
            pass
    root2.mainloop()
#............................................................................................................................................



#start screen
img = ImageTk.PhotoImage(file="Frames-1/frame0.jpg")
canvas.create_image((300, 300), image=img, anchor='center')
font_1 = tkinter.font.Font(weight="bold")
font_2 = tkinter.font.Font(weight='bold', size=28)
button1_text = tk.StringVar()
button1 = tk.Button(root, textvariable=button1_text, background='black', foreground='white',
                    font=font_1, width=25, height=2, command=lambda: get_screen1("Frames-1"))
button1_text.set("Chat")
button1.grid(column=0, row=2)

#------------------------------------------Analysis(DO NOT INTERFERE) --------------------------------------------------------------------------------------------------------------
from tkinter import *
import re
import os
from tkinter import messagebox


def clicked():
    root.destroy()
    window = Tk()
    window.title("Authenthication")
    window.configure(background='Black')

    Button1 = Button(window, text="Sign Up", bg='White', fg='Black', command=lambda : Sign_Up())
    Button2 = Button(window, text="Log In", bg='White', fg='Black', command=lambda : Log())

    # calculate the size of the buttons
    button_width = 100
    button_height = 30

    # function to center the buttons
    def center_buttons():
        # get the window dimensions
        width = window.winfo_width()
        height = window.winfo_height()

        # calculate the center of the window
        center_x = width // 2
        center_y = height // 2

        # calculate the positions of the buttons
        button1_x = center_x - button_width - 10
        button2_x = center_x + 10
        button_y = center_y - button_height // 2

        # place the buttons in their positions
        Button1.place(x=button1_x, y=button_y, width=button_width, height=button_height)
        Button2.place(x=button2_x, y=button_y, width=button_width, height=button_height)

    # center the buttons initially
    center_buttons()

    # bind the center_buttons function to the window resize event
    window.bind("<Configure>", lambda event: center_buttons())

    def Sign_Up():
        window.destroy()
        Sign_up = Tk()
        Sign_up.title("Sign Up")
        Sign_up.configure(background='Black')
        Sign_up.geometry("1200x900")

        # Calculate the center coordinates of the window
        x_center = Sign_up.winfo_width() // 2
        y_center = Sign_up.winfo_height() // 2

        # Create the Entry widgets
        signup_username_label = Label(Sign_up, text="Email ID:", bg='Black', fg='White', font=("Arial", 15))
        signup_username_label.place(relx=0.4, rely=0.4, anchor=CENTER)
        Username = Entry(Sign_up, borderwidth=4, width=30, font=("Arial", 15))
        Username.place(relx=0.6, rely=0.4, anchor=CENTER)




        signup_password_label = Label(Sign_up, text="Password:", bg='Black', fg='White', font=("Arial", 15))
        signup_password_label.place(relx=0.4, rely=0.5, anchor=CENTER)
        Create_a_Password = Entry(Sign_up, borderwidth=2.7, width=30, font=("Arial", 15), show="*")
        Create_a_Password.place(relx=0.6, rely=0.5, anchor=CENTER)

        confirm_password_label = Label(Sign_up, text="Confirm Password:", bg='Black', fg='White', font=("Arial", 15))
        confirm_password_label.place(relx=0.4, rely=0.6, anchor=CENTER)
        Confirm_Password = Entry(Sign_up, borderwidth=2.7, width=30, font=("Arial", 13), show="*")
        Confirm_Password.place(relx=0.6, rely=0.6, anchor=CENTER)
        # Create the function to check if username exists in file

        Show_Password_Var = BooleanVar()
        Show_Password_Checkbox = Checkbutton(Sign_up, text="Show Password", variable=Show_Password_Var,
                                             onvalue=True,
                                             offvalue=False, command= lambda :show_password(), bg='Black', fg='White',
                                             width=20, font=("Arial", 10))
        Show_Password_Checkbox.place(relx=0.56, rely=0.653, anchor=CENTER)
        def show_password():
            if Show_Password_Var.get():
                Create_a_Password.config(show="")
                Confirm_Password.config(show="")
            else:
                Create_a_Password.config(show="*")
                Confirm_Password.config(show="*")

                # Create the "Show Password" checkbox



        button_submit = Button(Sign_up, text="Submit", bg='White', fg='Black', width=20, height=1,
                                   command=lambda: submit())
        button_submit.place(relx=0.56, rely=0.7, anchor=CENTER)


        def username_exists(username):
            if os.path.isfile('user_info.txt'):
                with open('user_info.txt', 'r') as file:
                    for line in file:
                        if username == line.split(':')[0]:
                            return True
            return False

    # Create the function to write the username and password to file

        # Create the function to submit the username and password
        def submit():
            global username, password, confirm_password
            username = Username.get()
            password = Create_a_Password.get()
            confirm_password = Confirm_Password.get()



            # Checking if the passwords match
            if password != confirm_password:

                messagebox.showinfo("Warning", "Passwords do not match!")
            # Checking if the username meets the required criteria
            elif not re.match("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+$", username):

                messagebox.showinfo("Warning", "Invalid Email ID")
            # Checking if the password meets the required criteria
            #elif not re.match("^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$", password):

                messagebox.showinfo("Warning", "Password must be at least 8 characters long and contain at "
                                               "least one lowercase letter, one uppercase letter, one digit, "
                                               "and one special character (@$!%*?&)")

            else:

                # Check if username already exists in file
                if username_exists(username):
                    # Show a label to indicate that the username already exists

                    messagebox.showinfo("Warning", f"Username '{username}' already exists in file.")

                    # Clear the Entry widgets
                    Username.delete(0, END)
                    Create_a_Password.delete(0, END)
                    Confirm_Password.delete(0, END)
                    # Return to exit the function
                    return

                # Open the file in append mode and write the values to the file
                with open('user_info.txt', 'a') as file:
                    file.write(f"{username}:{password}\n")

                # Clear the Entry widgets
                Username.delete(0, END)
                Create_a_Password.delete(0, END)
                Confirm_Password.delete(0, END)

                # Show a label to confirm that the values were written to the file

                messagebox.showinfo("Congratulations", " Sign up Successfully")

                Sign_up.destroy()
                Log()





    def Log():
        #window.destroy()
        Log = Tk()
        Log.title("Log In")
        Log.configure(background='Black')
        Log.geometry("1200x900")

        # Create the Entry widgets
        global Username1
        Username1_label = Label(Log, text="Email ID : ", font=("Arial", 15), fg="white", bg="black")
        Username1 = Entry(Log, borderwidth=2.7, width=50, font=("Arial", 15))

        global Password
        Password_label = Label(Log, text="Password : ", font=("Arial", 15), fg="white", bg="black")
        Password = Entry(Log, borderwidth=2.7, width=50, font=("Arial", 15), show="*")





        # Calculate the center coordinates of the window
        x_center = Log.winfo_width() // 2
        y_center = Log.winfo_height() // 2

        # Place the Username Entry widget and label in the center with some padding on top
        Username1_label.place(relx=0.3, rely=0.4, anchor=E)
        Username1.place(relx=0.4, rely=0.4, anchor=W)

        # Place the Password Entry widget and label below the Username widget with a fixed gap of 10 pixels
        Password_label.place(relx=0.3, rely=0.5, anchor=E)
        Password.place(relx=0.4, rely=0.5, anchor=W)

        # Center the window on the screen
        Log.update_idletasks()
        screen_width = Log.winfo_screenwidth()
        screen_height = Log.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (Log.winfo_width() / 2))
        y_coordinate = int((screen_height / 2) - (Log.winfo_height() / 2))
        Log.geometry("+{}+{}".format(x_coordinate, y_coordinate))

        def show_password():
            if Password['show'] == '*':
                Password.configure(show="")
                show_password_button.configure(text="Hide Password")
            else:
                Password.configure(show="*")
                show_password_button.configure(text="Show Password")

        show_password_button = Button(Log, text="Show Password", font=("Arial", 10), command=show_password, width=15)
        show_password_button.place(relx=0.5, rely=0.56)
        button1=Button(Log, text="Submit", bg='White', fg='Black', command=lambda : button(), width=20, height=1)
        button1.place(relx=0.56, rely=0.66, anchor=CENTER)

        def button():

            with open("user_info.txt", "r") as f:
                user_info = {}
                for line in f:
                    if ":" in line:
                        username, password = line.strip().split(":")
                        user_info[username] = password

            username = Username1.get()
            password = Password.get()
            if username in user_info and password == user_info[username]:
                messagebox.showinfo("Congratulations", " Log In Successfully")
                call()
                Log.destroy()
#...........................................................ADD NEW WINDOW............................................................................................................
            elif username not in user_info:
                messagebox.showinfo("Warning", " Invalid Username ")
            elif password != user_info[username]:
                messagebox.showinfo("Warning", " Invalid Password ")
            else:
                messagebox.showinfo("Warning", " Invalid Username and Invalid Password ")


#root.mainloop()
button2_text = tk.StringVar()
button2 = tk.Button(root, textvariable=button2_text, background='black', foreground='white',
                    font=font_1, width=25, height=2 , command=lambda :clicked())
button2_text.set("Analysis") #analysis button
button2.grid(column=0, row=3)
root.mainloop()