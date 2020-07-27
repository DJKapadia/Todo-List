import tkinter
from tkinter import *
from tkinter import messagebox
from time import strftime
import datefinder
import datetime
import sqlite3 as sq
import math
import pyaudio
from tkcalendar import DateEntry


root = Tk()
root.title('To-Do List')
root.geometry("500x700")

conn = sq.connect('Dhruv.db')
cur = conn.cursor()
cur.execute('create table if not exists Todolist (Task text,Date Text,Time Text)')

task = []


# ------------------------------- Functions--------------------------------
def ti():
    a = tientry.get()
    # print(a)
    alarm(a)
def alarm(text):
    dTimeA=datefinder.find_dates(text)
    for mat in dTimeA:
        pass
    stringA=str(mat)
    timeA=stringA[11:]
    hourA=timeA[:-6]
    hourA=int(hourA)
    minA=timeA[3:-3]
    minA=int(minA)
    while True:
        if hourA == datetime.datetime.now().hour:
            if minA == datetime.datetime.now().minute:
                BITRATE = 5000  # number of frames per second/frameset.
                FREQUENCY = 10000  # Hz, waves per second, 261.63=C4-note.
                LENGTH = 5  # seconds to play sound
                if FREQUENCY > BITRATE:
                    BITRATE = FREQUENCY + 100
                NUMBEROFFRAMES = int(BITRATE * LENGTH)
                RESTFRAMES = NUMBEROFFRAMES % BITRATE
                WAVEDATA = ''
                # generating waves
                for x in range(NUMBEROFFRAMES):
                    WAVEDATA = WAVEDATA + chr(int(math.sin(x / ((BITRATE / FREQUENCY) / math.pi)) * 127 + 128))
                for x in range(RESTFRAMES):
                    WAVEDATA = WAVEDATA + chr(128)
                print(WAVEDATA)
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(1), channels=2, rate=BITRATE, output=True)
                stream.write(WAVEDATA)
                stream.stop_stream()
                stream.close()
                p.terminate()
            elif minA<datetime.datetime.now().minute:
                break

def addTask():
    word = e1.get()
    g=cal.get()
    m= tientry.get()
    if len(word) == 0:
        messagebox.showinfo('Empty Entry', 'Enter task name')
    else:
        task.append([word,g,m])
        cur.execute('insert into Todolist (Task, Date, Time) VALUES(?, ?, ?)', (str(word),str(g),str(m)))
        listUpdate()
        e1.delete(0, 'end')


def listUpdate():
    clearList()
    for i in task:
        t.insert('end', i)

def deleteAll():
    mb = messagebox.askyesno('Delete All', 'Are you sure?')
    cur.execute('delete from Todolist')
    if mb == True:
        while (len(task) != 0):
            task.pop()
        cur.execute('delete from Todolist')
        listUpdate()


def clearList():
    t.delete(0, 'end')

def retrieveDB():
    while (len(task) != 0):
        task.pop()
    for row in cur.execute('select Task,Date,Time from Todolist'):
        task.append([row[0],row[1],row[2]])


# ------------------------------- Functions--------------------------------

#l1 = ttk.Label(root, text='To-Do List')
l2 = Label(root, text='Enter your task: ')
e1 = Entry(root, width=30)

t = Listbox(root,width=45,height=20, selectmode='SINGLE')
b1 =Button(root, text='Add task',fg="#ffffff", bg='#6186AC', width=9,command=addTask)
b2=Button(root,text='Timer',fg='#ffffff',bg='#6186AC',width=9,command=ti)
b3 =Button(root, text='Delete all',fg="#ffffff", bg='#6186AC', width=9, command=deleteAll)
b4 =Button(root, text='Exit', fg="#ffffff", bg='#EB6464',width=9, command=root.destroy)

retrieveDB()
listUpdate()

# Place geometry
l2.place(x=8, y=70, width=200, height=25)
e1.place(x=60, y=93, width=200, height=25)
b1.place(x='402',y='120')
b2.place(x='402',y='150')
b3.place(x=60, y=140)
b4.place(x='402',y='190')
#l1.place(x=50, y=10)
t.place(x='60',y='218')



tilabel=Label(root,text='Time')
tilabel.place(x=318,y=67)
tientry=Entry(root,width=10)
tientry.place(x='300',y='90')
datelabel=Label(root,text='Date')
datelabel.place(x='421',y='67')
cal = DateEntry(root, width=10, background='darkblue',
                    foreground='white', borderwidth=2)
cal.place(x='392', y='90')

def time():
	string = strftime('%H:%M:%S')
	lbl.config(text = string)
	lbl.after(1000, time)
lbl = Label(root, font = ('calibri', 20, 'bold'),background = '#ECF0F1',foreground = 'black')
lbl.place(x=380,y=5)
time()
tiget=tientry.get()

root.mainloop()
conn.commit()
cur.close()
