from threading import Thread
from time import sleep
from tkinter import *
from datetime import datetime

class ValueToHighError(Exception): pass

seconds: int = 0
minutes: int = 0
hours: int = 0

def createErrorMessage(message: str) -> None:
    errorLabel: Label = Label(text = message, fg = "red", font = ("Terminal", 25), bg = "black")
    [errorLabel.place(x = 10, y = 450), sleep(1.5), errorLabel.destroy()]

def adjustTimeToSystemTime() -> None:
    global seconds, minutes, hours
    timeSplit: List[str] = (datetime.now()).strftime('%H:%M:%S')
    timeSplit = timeSplit.split(':')
    seconds = int(timeSplit[2])
    minutes = int(timeSplit[1])
    hours = int(timeSplit[0])

def adjustTime(time: str) -> None:
    global seconds, minutes, hours
    def validateEachTime(index: int, maxTime: int) -> None:
        try:
            timeStore: int = int(timeSplit[index])
            if timeStore > maxTime: raise ValueToHighError()
        except ValueToHighError: return
        else: return timeStore
        
    if len(time) != 8: 
        Thread(target = createErrorMessage, args = ("time is too long or short to be valid",)).start()
        return
    for char in time:
        if char not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':'):
            Thread(target = createErrorMessage, args = ("time contains illegal characters",)).start()
            return
    timeSplit: List[str | int] = time.split(':')
    secondsTime: int = validateEachTime(2, 59)
    minutesTime: int = validateEachTime(1, 59)
    hoursTime: int = validateEachTime(0, 23)
    if isinstance(secondsTime, int) and isinstance(minutesTime, int) and isinstance(hoursTime, int): print(secondsTime, minutesTime, hoursTime)
    else: Thread(target = createErrorMessage, args = ("value isn't within range",)).start()

def clock() -> None:
    global seconds, minutes, hours
    def addTimeToStr(digit: int, extraChar: chr) -> str:
        if len(str(digit)) == 1: return '0' + str(digit) + extraChar
        else: return str(digit) + extraChar

    while appIsRunning:
        sleep(1)
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 24: hours = 0
        timeString: str = ""
        timeString += addTimeToStr(hours, ':')
        timeString += addTimeToStr(minutes, ':')
        timeString += addTimeToStr(seconds, '')
        timeLabel.configure(text = timeString)
        del timeString
    
appIsRunning: bool = True
app: Tk = Tk()
app.title("clock app")
app.resizable(width = False, height = False)
app.geometry("600x250")
app.configure(bg = "black")
timeLabel: Label = Label(text = "00:00:00", fg = "DarkOrange2", bg = "black", font = ("Terminal", 35))
timeLabel.place(x = 20, y = 20)
entryBorder: Frame = Frame(background = "DarkOrange2")
entryBorder.place(x = 20, y = 120)
timeEntry: Entry = Entry(entryBorder, font = ("Terminal", 15), bg = "black", fg = "DarkOrange2", borderwidth = 3, relief = "solid", width = 8)
timeEntry.pack(padx = 1, pady = 1)
buttonBorder: Frame = Frame(background = "DarkOrange2")
buttonBorder.place(x = 130, y = 115)
submitButton: Button = Button(buttonBorder, text = "adjust time", font = ("Terminal", 15), bg = "black", fg = "DarkOrange", borderwidth = 3, relief = "solid", command = lambda: adjustTime(timeEntry.get()))
submitButton.pack(padx = 1, pady = 1)
getSystemTimeBorder: Frame = Frame(background = "orange")
getSystemTimeBorder.place(x = 35, y = 175)
systemTimeButton: Button = Button(getSystemTimeBorder, text = "assign system time", fg = "DarkOrange2", font = ("Terminal", 15), bg = "black", borderwidth = 3, relief = "solid", command = adjustTimeToSystemTime)
systemTimeButton.pack(padx = 1, pady = 1)

Thread(target = clock).start()

app.mainloop()