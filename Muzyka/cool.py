import os
import pickle
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from PIL import Image, ImageTk, ImageSequence


def playGIF():
    global img
    img = Image.open('pngs/DDv.gif')
    lbl = Label(win)

    for img in ImageSequence.Iterator(img):
        img = ImageTk.PhotoImage((img))
        lbl.config(image=img)
        win.update()

    win.after(0, 0)


class odtw(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        mixer.init()
        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist=[]

        self.current = 0
        self.paused = True
        self.played = False

        self.stwOkn()
        self.widgets()
        self.contrWidgets()
        self.tracklistWidgets()

    def stwOkn(self):
        self.track = tk.LabelFrame(self, text='♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ♥  ',
                                   font=("helvetica", 13, "bold"),
                                   fg="#708090", bd=5, relief=tk.FLAT)
        self.track.config(width=100, height=100, bg = "white")
        self.track.grid(row=0, column=0, sticky  =  "NSEW")

        self.track12 = tk.LabelFrame(self, text='',
                                    font=("helvetica", 13, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track12.config(height=10, bg = "white")
        self.track12.grid(row=0, column=1,sticky  =  "NSEW")
        
        self.track0 = tk.LabelFrame(self, text='',
                                    font=("helvetica", 13, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track0.config(height=10, bg = "white")
        self.track0.grid(row=1, column=0,sticky  =  "NSEW")

        self.track01 = tk.LabelFrame(self, text='',
                                    font=("helvetica", 13, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track01.config(height=10, bg = "white")
        self.track01.grid(row=1, column=1,sticky  =  "NSEW")
        
        self.track1 = tk.LabelFrame(self, text='PLAYLISTA ♥ ',
                                    font=("helvetica", 13, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track1.config(width=10, height=100,  bg = "white")
        self.track1.grid(row=2, column=0, sticky  =  "NSEW")
        
        self.track15 = tk.LabelFrame(self, text='',
                                    font=("helvetica", 13, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track15.config(width=10, height=100,  bg = "white")
        self.track15.grid(row=2, column=1, sticky  =  "NSEW")

        self.track2 = tk.LabelFrame(self, text='',
                                    font=("helvetica", 9, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track2.config(width=10, height=50,  bg = "white")
        self.track2.grid(row=3, column=0, sticky  =  "NSEW")
        
        self.track25 = tk.LabelFrame(self, text='',
                                    font=("helvetica", 13, "bold"),
                                    fg="#708090", bd=5, relief=tk.FLAT)
        self.track25.config(width=10, height=100,  bg = "white")
        self.track25.grid(row=3, column=1, sticky  =  "NSEW")
        
    def widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=300, height=400)
        self.canvas.grid(row=0, column=0, padx= 35)

        self.songtrack = tk.Label(self.track, font=(
            "helvetica", 9, "bold"), bg="white", fg="#708090",)
        self.songtrack['text'] = "♥ NIE WYBRANO PIOSENKI ♥ "
        self.songtrack.configure(width=30, height=2)
        self.songtrack.grid(row=1, column=0, sticky  =  "NSEW")

    def contrWidgets(self):
        self.loads = tk.Button(self.track2, text="DODAJ PIOSENKI", font=(
            "helvetica", 9, "bold"), fg="#708090")
        self.loads['command'] = self.retrieveSongs
        self.loads.configure(width=29, height=2, bg = "white")
        self.loads.grid(row=0, column=3, sticky  =  "NSEW")

        self.prev = tk.Button(self.track2, image=prev)
        self.prev['command'] = self.prevSong
        self.prev.configure(width=50, height=50, bg = "white")
        self.prev.grid(row=0, column=0, sticky  =  "NSEW")

        self.pause = tk.Button(self.track2, image=pause)
        self.pause['command'] = self.pauseSong
        self.pause.configure(width=50, height=50, bg = "white")
        self.pause.grid(row=0, column=1, sticky  =  "NSEW")

        self.nextsong = tk.Button(self.track2, image=nextsong)
        self.nextsong['command'] = self.nextSong
        self.nextsong.configure(width=50, height=50, bg = "white")
        self.nextsong.grid(row=0, column=2, sticky  =  "NSEW")

        self.volume = tk.DoubleVar()
        self.suw = tk.Scale(self.track0, from_=0, to=100,
                            orient=tk.HORIZONTAL, length=365)
        self.suw['variable'] = self.volume
        self.suw['command'] = self.changeVol
        self.suw.set(50)
        mixer.music.set_volume(0.50)
        self.suw.grid(row=2, column=1, padx=3, sticky  =  "NSEW")

    def tracklistWidgets(self):
        self.scrollbar = tk.Scrollbar(self.track1, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.listbox = tk.Listbox(self.track1, selectmode=tk.SINGLE,
                                  yscrollcommand=self.scrollbar.set, selectbackground="white")
        self.enSongs()
        self.listbox.config(height=12, width=60)
        self.listbox.bind('<Double-1>', self.playSong)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.grid(row=0, column=0, rowspan= 5, sticky  =  "NSEW")

    def enSongs(self):
        for index, song in enumerate(self.playlist):
            self.listbox.insert(index, os.path.basename(song))

    def retrieveSongs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for win_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (win_ + '/' + file).replace('\\', '/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.track1['text'] = f'Liczba piosenek: {str(len(self.playlist))}'
        self.listbox.delete(0, tk.END)
        self.enSongs()

    def playSong(self, event=None):
        if event is not None:
            self.current = self.listbox.curselection()[0]
            for i in range(len(self.playlist)):
                self.listbox.itemconfigure(i, bg="white")
		
        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w' 
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])
        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.listbox.activate(self.current) 
        self.listbox.itemconfigure(self.current, bg='pink')
        mixer.music.play()


    def prevSong(self):
        if self.current > 0:
            self.current -= 1 
        else:
            self.current = 0 
            
        self.list.itemconfigure(self.current, bg="white")
        self.playSong()

    def nextSong(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1 
        else:
            self.current = 0 
            
        self.listbox.itemconfigure(self.current, bg="white")
        self.playSong()

    def pauseSong(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def changeVol(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v/100)

win = tk.Tk()
win.geometry('390x807')
win.configure(bg='white')
win.wm_title('Muzyka')

prev = PhotoImage(file='pngs/271220.gif')
play = PhotoImage(file='pngs/3669483.gif')
pause = PhotoImage(file= 'pngs/5577228.gif')
nextsong = PhotoImage(file='pngs/2722998.gif')
img = PhotoImage(file='pngs/DDv.gif')

app = odtw(master=win)
app.mainloop()
