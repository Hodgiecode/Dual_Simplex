import simplex
import sys

from tkinter import Tk, Label, StringVar, Button, Entry, Frame, Text, Toplevel, LEFT, END


class StdoutRedirector(object):

    def __init__(self):
        # clear before get all values
        self.result = ''

    def write(self, text):
        # have to use += because one `print()` executes `sys.stdout` many times
        self.result += text



        
window = Tk()
window.title("Dual Simplex")
window.geometry("600x600+120+120")
window.resizable(False, False)

# empty arrays for your Entrys and StringVars
text_var = []
entries = []

# callback function to get your StringVars
def get_mat():
    rows = int(e1.get()) + 1
    cols = int(e2.get()) + 2

    matrix = []
    for i in range(rows):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(entries[i][j].get())

    matrix[0] = matrix[0][:-2]
    for i in range(1, len(matrix)): matrix[i] = matrix[i][:-2] + [matrix[i][-1]]

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = float(matrix[i][j])

    window2 = Toplevel(window)
    window2.title("Solution")
    window2.geometry("500x500+120+120")
    window2.resizable(False, False)
  
    T = Text(window2, height = 30, width = 60)
    T.place(x=10,y=10)

    old_stdout = sys.stdout
    sys.stdout = StdoutRedirector()
    simplex.run_solution(int(e1.get()), int(e2.get()), matrix, e3.get())
    
    T.insert(END, sys.stdout.result.strip())
    sys.stdout = old_stdout
  

def create_task():
    v1 = int(e1.get()) + 1
    v2 = int(e2.get()) + 2
    generate(v1,v2)
    

def generate(rows, cols):
    x2 = 0
    y2 = 0
    global entries
    entries = []
    global text_var
    text_var = []
    
    for i in range(rows):
        text_var.append([])
        entries.append([])

        for j in range(cols):
            text_var[i].append(StringVar())
            entries[i].append(Entry(frame, textvariable=text_var[i][j], font=("Arial",10), width=5))
            entries[i][j].place(x=60 + x2, y=50 + y2)
            if j == cols - 2:
                if i == 0:
                    entries[i][j].insert(0,"->")
                else:
                    if e3.get() != "min":
                        entries[i][j].insert(0,"<=")
                    else:
                        entries[i][j].insert(0,">=")

            if j == cols - 1 and i == 0:
                    entries[i][j].insert(0,e3.get())
                    
            x2 += 50

        y2 += 50
        x2 = 0


def clean_frame():
    for widget in frame.winfo_children():
       widget.destroy()

    frame.pack_forget()
   

l1=Label(window, text="m:")
l1.place(x=105, y=10)
e1=Entry(window, textvariable="N0", font=("Arial",15), width=3)
e1.place(x=120,y=10)

l2=Label(window, text="n:")
l2.place(x=160, y=10)
e2=Entry(window, textvariable="N1", font=("Arial",15), width=3)
e2.place(x=170,y=10)

e3=Entry(window, textvariable="N2", font=("Arial",15), width=5)
e3.place(x=220,y=10)

button0= Button(window,text="Create",  width=10, command=create_task)
button0.place(x=290,y=10)

button= Button(window,text="Get Solution",  width=10, command=get_mat)
button.place(x=370,y=10)

button2 = Button(window,text="Clean",  width=10, command=clean_frame)
button2.place(x=450,y=10)

frame = Frame(window, width=500, height=600)
frame.place(x=60,y=40)


window.mainloop()
