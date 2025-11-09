import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pygame
import time
import os
import signal
from pathlib import Path
import threading
from random import randrange





# --- Globals ---

global playing
global folder
playing = None
folder = None
pygame.mixer.init()

# -----------




# --- Functions ---

def play_music(mp3):
	global playing

	if(playing == mp3):
		pygame.mixer.music.unpause()
	else:
		pygame.mixer.music.load(mp3)
		pygame.mixer.music.play()
		playing = mp3
	L.place(x=20,y=400)

	L.config(text = os.path.basename(mp3)) 


def setVol(num):
	pygame.mixer.music.set_volume(int(num)/10)

def try_playing():
	try: 
		play_music(os.path.join(folder, e.selection_get()))
	except:
		messagebox.showerror("Something went wrong!")
		pass

def on_closing():
    pygame.mixer.music.stop()
    W.destroy()

def try_random():
	try: 
		x = randrange(0, int(e.size()))
		play_music(os.path.join(folder, e.get(x)))
		e.selection_clear(0, tk.END)
		e.selection_set(x)
		e.activate(x)
	except:
		messagebox.showerror("Something went wrong!")
		pass

def select_folder():
    global folder
    folder = filedialog.askdirectory()
    if folder:
        e.delete(0, tk.END)
        for i, file in enumerate(os.listdir(folder)):
            if file.endswith(".mp3"):
                e.insert(i, file)


def playNext():
	for i, file in enumerate(os.listdir(folder)): #Linear search for the previous song that is playing. Not the most efficient, but does not require storing the previous song's index
		if playing == os.path.join(folder, file):
			play_music(     os.path.join(folder,    (os.listdir(folder)[(i + 1)% int(e.size())] )   )       ) #Play the next song, but modulo size. This means that if we are playing the last song, we switch to the first
			break;
	e.selection_clear(0, tk.END)
	e.selection_set((i + 1)% int(e.size()))
	e.activate((i + 1)% int(e.size()))

# -----------




# --- GUI ---

W = tk.Tk()
W.geometry("500x500")
W.title("Yutube 2")
W.configure(bg = "black")
W.protocol("WM_DELETE_WINDOW", on_closing)

RandomPic = tk.PhotoImage(file="Images/Random.png").subsample(10,10)
PlayPic = tk.PhotoImage(file="Images/Play.png").subsample(10,10)
SkipPic = tk.PhotoImage(file="Images/Skip.png").subsample(10,10)
PausePic = tk.PhotoImage(file="Images/Pause.png").subsample(10,10)

tk.Button(W, text = "Play!", image = PlayPic, command = lambda: try_playing(), bd=0, highlightthickness=0).place(x=50,y=50)
tk.Button(W, text = "Pause!", image = PausePic, command = lambda: pygame.mixer.music.pause(), bd=0, highlightthickness=0).place(x=150,y=50)
tk.Button(W, text = "Random!", image = RandomPic, command = lambda: try_random(), bd=0, highlightthickness=0).place(x = 250, y = 50)
tk.Button(W, text = "Find Music!", command = lambda: select_folder()).place(x = 50, y = 150)
tk.Button(W, text = "Skip!", image = SkipPic, command = lambda: playNext(), bd=0, highlightthickness=0).place(x = 350, y = 50)

VolLevelScale = tk.Scale(W, orient = "horizontal", from_ = 0, to = 10, command = setVol)
VolLevelScale.set(10)
VolLevelScale.place(x=50,y=250)

L = tk.Label(W)

e = tk.Listbox(W, selectmode = "single", width = 30, height = 20)
e.place(x = 200, y = 130)

# -----------



W.mainloop()
