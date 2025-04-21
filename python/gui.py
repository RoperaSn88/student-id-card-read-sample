#!/usr/bin/env python3
import tkinter
import threading
import os
from sit_idcardlib_py import Reader

FILE_NAME = "ids.txt"
count=0

#def show_geometry(event):

class App(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.id_label = tkinter.Label(
            self,
            text="Not detected",
            padx=5,
            pady=10,
            font=("A P-OTF UD新ゴ Pr6N B", 36),
            background="#fff"
        )
        self.id_label.pack(expand=True)

root = tkinter.Tk()
root.attributes("-fullscreen",True)
root.configure(background="#fff")
root.configure()
root.geometry("1280x720")
box=tkinter.Label(text="学生証リーダー",background="#00b0f0",width=200,height=1,fg="#fff",font=("A P-OTF UD新ゴ Pr6N B",48),anchor="nw")
box.pack(side=tkinter.TOP)
box2=tkinter.Label(text=" ",background="#00a0e0",width=5,height=100,fg="#000",font=("A P-OTF UD新ゴ Pr6N B",48))
box2.pack(side=tkinter.LEFT)
text=tkinter.Label(text="学生証をカードリーダーにかざすと\nあなたの学生番号が表示されます。\n後日、デジクリから入部招待メールが届きます。\nそのメールはご回答いただけなくても\nかまいません。",
                   font=("A P-OTF UD新ゴ Pr6N B",18),
                   fg="#000",bg="#fff",
                   width=50,height=5,
                   anchor="s")
text.pack(side=tkinter.TOP)
text2=tkinter.Label(text="あなたは"+str(count)+"人目の読み込み者です",font=("A P-OTF UD新ゴ Pr6N B",12),
                    fg="#000",bg="#fff")
text2.pack(side=tkinter.TOP)
text3=tkinter.Label(text="Developed by Digicre",fg="#000",bg="#fff",anchor="se")
text3.pack(side=tkinter.BOTTOM)

#root.bind("<Configure>",show_geometry)
app = App(master=root)
check=False

def callback(card):
    global app
    global reader
    global count
    global text2
    global check
    try:
        app.id_label["text"] = "あなたの番号は\n"+card.id
        found = False
        if os.path.isfile(FILE_NAME):
            with open(FILE_NAME) as f:
                while True:
                    student_id = f.readline()
                    if not student_id:
                        check=False
                        break
                    student_id = student_id.strip()
                    if student_id == card.id:
                        found = True
                        if check==False:
                            count+=1
                            check=True
                        #テキストの変更
                        text2["text"]="あなたは"+str(count)+"人目の読み込み者です"
                        break
        if not found:
            with open(FILE_NAME, "a") as f:
                f.write("{}\n".format(card.id))
    except Exception as e:
        print(e)
reader = Reader(callback)

def thread():
    global reader
    while True:
        try:
            reader.read()
        except Exception as e:
            print(e)
threading.Thread(target=thread).start()

app.mainloop()
