from typing import List
from tkinter import Label, Tk
from threading import Thread
from random import randrange, choice
from time import sleep

class geigerSector:
    flashColor: str = None
    obj: Label = None
    def __init__(self, color: str) -> None:
        self.flashColor = color
        self.obj = Label(text = "       ", bg = "black", font = ("Arial", 25))
        self.obj.pack(pady = 5)

    def turnOn(self) -> None: self.obj.configure(bg = self.flashColor)
    def turnOff(self) -> None: self.obj.configure(bg = "black")

def increaseSectorCount() -> None:
    global sectorCounter
    while appIsRunning:
        sleep(randrange(1,2))
        if choice((True, False)): sectorCounter -= 1
        else: sectorCounter += 1
        if sectorCounter < 1: sectorCounter = 1
        if sectorCounter > 10: sectorCounter = 10
        countLabel.configure(text = str(91 + sectorCounter) + "CPM")

def flashSectors() -> None:
    while appIsRunning:
        for i in range(sectorCounter, 10): sectors[i].turnOn()
        for i in range(0, sectorCounter): sectors[i].turnOff()

def closeWindow() -> None:
    global appIsRunning
    appIsRunning = False
    [geiger.destroy(), exit()]


appIsRunning: bool = True
sectorCounter: int = 5
geiger: Tk = Tk()
geiger.title("geiger app")
geiger.resizable(width = False, height = False)
geiger.geometry("100x600")
geiger.configure(bg = "black")
geiger.protocol("WM_DELETE_WINDOW", closeWindow)
sectors: List[geigerSector] = [geigerSector("red") for i in range(3)]
for i in range(4): sectors.append(geigerSector("orange"))
for i in range(4): sectors.append(geigerSector("green"))
Thread(target = increaseSectorCount).start()
Thread(target = flashSectors).start()
countLabel: Label = Label(text = "91 CPM", bg = "black", font = ("Arial", 15))
countLabel.place(x = 10, y = 10)

geiger.mainloop()