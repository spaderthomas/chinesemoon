# """
# Workflow:
# Create a new unit
# Load character data from CSV, XLSX, whatever
# Save unit
# Select unit to practice
# Spam notecards until done.

# Features:
# """

# Imports
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import IntVar
from collections import namedtuple
from openpyxl import *
import random
import sys
import copy
import pickle

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import main_support

# Data containers
## Ghetto struct
class Struct:
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

## Should have members: character, pinyin, definition, accessed, correct
class VocabWord(Struct):
    def __str__(self):
        if (self.accessed == 0):
            ratio = 0
        else:
            ratio = float(self.correct) / self.accessed
                
        return('character = ' + self.character + ","
               + 'pinyin = ' + self.pinyin + ","
               + 'definition = ' + self.definition + ","
               + 'ratio = ' + str(ratio))

## Globals
units = {} # Maps strings to lists of VocabWords

activeWord = False
activeUnit = False
activeDisplay = 'character' # Marks which part of the active word should be displayed

hardMode = 0
displayMode = 'character' # Marks which part of the next word should be displayed

# GUI 
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = Chinese(root)
    main_support.init(root, top)
    root.mainloop()


w = None
def create_Chinese(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = Chinese (w)
    main_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Chinese():
    global w
    w.destroy()
    w = None


class Chinese:
    # Flash card functions
    def showPinyin(self, event=None):
        global activeDisplay, activeWord
        activeDisplay = 'pinyin'
        if (activeWord):
            self.vocabWordLabel.configure(text=activeWord.pinyin)
    
    def showDef(self, event=None):
        global activeDisplay, activeWord
        activeDisplay = 'definition'
        if (activeWord):
            self.vocabWordLabel.configure(text=activeWord.definition)

    def showChar(self, event=None):
        global activeDisplay, activeWord
        activeDisplay = 'character'
        if (activeWord):
            self.vocabWordLabel.configure(text=activeWord.character)

    def cycleDisplay(self, event=None):
        global activeDisplay
        if (activeDisplay == 'character'):
            self.showPinyin()
        elif (activeDisplay == 'pinyin'):
            self.showDef()
        elif (activeDisplay == 'definition'):
            self.showChar()
        return 'break' 
        
    def nextWord(self, event=None ):
        global activeWord, activeUnit
        print(activeWord)
        countWordsTooEasy = 0
        while True:
            activeWord = random.choice(activeUnit)
        
            # Change word color based on how correct it is
            if (activeWord.accessed == 0):
                rateCorrect = 0
                wordColorHexStr = '#000000'
            else:
                rateCorrect = float(activeWord.correct) / activeWord.accessed
                rateIncorrect = 1 - rateCorrect
                wordColorHexStr = '#%02x%02x%02x' % (int(rateIncorrect * 255), # red
                                                     int(rateCorrect * 255),   # green
                                                     0)                        # blue
            # Reject words we get right >2/3 of the time in hard mode
            # Yeah, it's ghetto to just break if after a few hundred random tries you dont find a good word. 
            if (hardMode.get()):
                if (rateCorrect > .66):
                    countWordsTooEasy += 1
                else:
                    break
            else:
                break

            if (countWordsTooEasy > 1000):
                messagebox.showinfo("Get it girl!", "It looks like this unit is too easy for you -- we couldn't find a word with less than 2/3 correct rate!")
                root.mainloop()

        self.vocabWordLabel.configure(foreground=wordColorHexStr)
        if (displayMode == 'character'):
            self.showChar()
        elif (displayMode == 'pinyin'):
            self.showPinyin()
        elif (displayMode == 'definition'):
            self.showDef()
        return

    
    ## Unit handling
    def unitFromXLSX(self, path):
        global units
        vocab = []
        unit = load_workbook(path, read_only=True)
        sheet = unit['Sheet1']
        for row in sheet:
            newWord = VocabWord(character=row[0].value,
                                pinyin=row[1].value,
                                definition=row[2].value,
                                accessed=0,
                                correct=0)
            vocab.append(newWord)

        return vocab

    def makeUnitActive(self, name=None):
        global units, activeUnit, activeWord
        if (name == None):
            activeUnit = list(units.values())[0]
            activeWord = activeUnit[0]
            self.nextWord()
        else:
            activeUnit = units[name]
            activeWord = activeUnit[0]
            self.nextWord()
            
    def promptNewUnit(self):
        global units, activeUnit, activeWord
        unitName = simpledialog.askstring("New Unit!", "What's the name of the new unit?")
        root.withdraw()
        path = filedialog.askopenfilename()
        root.deiconify()

        newVocabList = self.unitFromXLSX(path)
        units[unitName] = newVocabList
        activeUnit = newVocabList
        activeWord = newVocabList[0]

        self.unitList.insert(END, unitName)
        self.vocabWordLabel.configure(text=activeWord.character)

    ## Marking
    def markIncorrect(self, event):
        global activeWord
        activeWord.accessed += 1
        self.nextWord(event)
        
    def markCorrect(self, event):
        activeWord.accessed += 1
        activeWord.correct += 1
        self.nextWord(event)


    ## Mode changing
    def activateDefMode(self):
        global displayMode
        self.pinyinModeButton.configure(relief=RAISED)
        self.charModeButton.configure(relief=RAISED)
        displayMode = 'definition'
        self.defModeButton.configure(relief=SUNKEN)
        self.showDef()
    
    def activatePinyinMode(self):
        global displayMode
        self.defModeButton.configure(relief=RAISED)
        self.charModeButton.configure(relief=RAISED)
        displayMode = 'pinyin'
        self.pinyinModeButton.configure(relief=SUNKEN)
        self.showPinyin()

    def activateCharMode(self):
        global displayMode
        self.pinyinModeButton.configure(relief=RAISED)
        self.defModeButton.configure(relief=RAISED)
        displayMode = 'character'
        self.charModeButton.configure(relief=SUNKEN)
        self.showChar()

    ## Persistence functions
    def serialize(self):
        global units, activeDisplay, hardMode, displayMode
        state = {'units' : units,
                 'activeDisplay' : activeDisplay,
                 'displayMode' : displayMode}
        pickle.dump(state, open("state.cm", "wb"))

    def deserialize(self):
        return pickle.load(open("state.cm", "rb"))

    def onClose(self):
        if messagebox.askokcancel("Quit", "Nice sesh! You sure you wanna quit?"):
            self.serialize()
            root.destroy()
            
    def __init__(self, top=None):
        global hardMode, units 
        # Init all static things (positions, colors) handled by PAGE
        font10 = "-family Georgia -size 9 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font9 = "-family Georgia -size 12 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        vocabFont = "-family Georgia -size 48 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 

        top.geometry("901x450+511+97")
        top.title("Chinese")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")


        self.unitList = Listbox(top)
        self.unitList.place(relx=0.01, rely=0.11, relheight=0.73, relwidth=0.33)
        self.unitList.configure(background="white")
        self.unitList.configure(disabledforeground="#a3a3a3")
        self.unitList.configure(font="TkFixedFont")
        self.unitList.configure(foreground="#000000")
        self.unitList.configure(highlightbackground="#d9d9d9")
        self.unitList.configure(highlightcolor="black")
        self.unitList.configure(selectbackground="#c4c4c4")
        self.unitList.configure(selectforeground="black")
        self.unitList.configure(width=294)

        self.unitSelect = Label(top)
        self.unitSelect.place(relx=0.11, rely=0.02, height=26, width=102)
        self.unitSelect.configure(activebackground="#f9f9f9")
        self.unitSelect.configure(activeforeground="black")
        self.unitSelect.configure(background="#d9d9d9")
        self.unitSelect.configure(disabledforeground="#a3a3a3")
        self.unitSelect.configure(font=font9)
        self.unitSelect.configure(foreground="#000000")
        self.unitSelect.configure(highlightbackground="#d9d9d9")
        self.unitSelect.configure(highlightcolor="black")
        self.unitSelect.configure(text='''Select Unit''')

        self.newUnit = Button(top)
        self.newUnit.place(relx=0.01, rely=0.87, height=43, width=296)
        self.newUnit.configure(activebackground="#d9d9d9")
        self.newUnit.configure(activeforeground="#000000")
        self.newUnit.configure(background="#d9d9d9")
        self.newUnit.configure(borderwidth="3")
        self.newUnit.configure(disabledforeground="#a3a3a3")
        self.newUnit.configure(font=font9)
        self.newUnit.configure(foreground="#000000")
        self.newUnit.configure(highlightbackground="#d9d9d9")
        self.newUnit.configure(highlightcolor="black")
        self.newUnit.configure(pady="0")
        self.newUnit.configure(text='''Add New Unit''')

        self.vocabWordLabel = Label(top)
        self.vocabWordLabel.place(relx=0.46, rely=0.33, height=116, width=352)
        self.vocabWordLabel.configure(activebackground="#000080")
        self.vocabWordLabel.configure(activeforeground="white")
        self.vocabWordLabel.configure(activeforeground="#000000")
        self.vocabWordLabel.configure(background="#d9d9d9")
        self.vocabWordLabel.configure(disabledforeground="#a3a3a3")
        self.vocabWordLabel.configure(font=vocabFont)
        self.vocabWordLabel.configure(foreground="#000000")
        self.vocabWordLabel.configure(highlightbackground="#d9d9d9")
        self.vocabWordLabel.configure(highlightcolor="black")
 
        self.pinyinModeButton = Button(top)
        self.pinyinModeButton.place(relx=0.59, rely=0.87, height=43, width=155)
        self.pinyinModeButton.configure(activebackground="#d9d9d9")
        self.pinyinModeButton.configure(activeforeground="#000000")
        self.pinyinModeButton.configure(background="#d9d9d9")
        self.pinyinModeButton.configure(borderwidth="3")
        self.pinyinModeButton.configure(disabledforeground="#a3a3a3")
        self.pinyinModeButton.configure(font=font10)
        self.pinyinModeButton.configure(foreground="#000000")
        self.pinyinModeButton.configure(highlightbackground="#d9d9d9")
        self.pinyinModeButton.configure(highlightcolor="black")
        self.pinyinModeButton.configure(padx="0")
        self.pinyinModeButton.configure(pady="0")
        self.pinyinModeButton.configure(text='''Pinyin Mode!''')

        self.defModeButton = Button(top)
        self.defModeButton.place(relx=0.79, rely=0.87, height=43, width=175)
        self.defModeButton.configure(activebackground="#d9d9d9")
        self.defModeButton.configure(activeforeground="#000000")
        self.defModeButton.configure(background="#d9d9d9")
        self.defModeButton.configure(borderwidth="3")
        self.defModeButton.configure(disabledforeground="#a3a3a3")
        self.defModeButton.configure(font=font10)
        self.defModeButton.configure(foreground="#000000")
        self.defModeButton.configure(highlightbackground="#d9d9d9")
        self.defModeButton.configure(highlightcolor="black")
        self.defModeButton.configure(padx="0")
        self.defModeButton.configure(pady="0")
        self.defModeButton.configure(text='''Definition Mode!''')

        self.charModeButton = Button(top)
        self.charModeButton.place(relx=0.39, rely=0.87, height=43, width=155)
        self.charModeButton.configure(activebackground="#d9d9d9")
        self.charModeButton.configure(activeforeground="#000000")
        self.charModeButton.configure(background="#d9d9d9")
        self.charModeButton.configure(borderwidth="3")
        self.charModeButton.configure(disabledforeground="#a3a3a3")
        self.charModeButton.configure(font=font10)
        self.charModeButton.configure(foreground="#000000")
        self.charModeButton.configure(highlightbackground="#d9d9d9")
        self.charModeButton.configure(highlightcolor="black")
        self.charModeButton.configure(padx="0")
        self.charModeButton.configure(pady="0")
        self.charModeButton.configure(text='''Character Mode!''')

        hardMode = IntVar(root)
        hardMode.set(0)
        self.toggleHardButton = Checkbutton(top)
        self.toggleHardButton.place(relx=0.88, rely=0.02, relheight=0.06, relwidth=0.12)
        self.toggleHardButton.configure(activebackground="#d9d9d9")
        self.toggleHardButton.configure(activeforeground="#000000")
        self.toggleHardButton.configure(background="#d9d9d9")
        self.toggleHardButton.configure(disabledforeground="#a3a3a3")
        self.toggleHardButton.configure(font=font10)
        self.toggleHardButton.configure(foreground="#000000")
        self.toggleHardButton.configure(highlightbackground="#d9d9d9")
        self.toggleHardButton.configure(highlightcolor="black")
        self.toggleHardButton.configure(justify=LEFT)
        self.toggleHardButton.configure(text='''Hard Mode''')
        self.toggleHardButton.configure(variable=hardMode)
        
        # Init all programmatic things
        top.bind("n", self.nextWord)
        top.bind("p", self.showPinyin)
        top.bind("d", self.showDef)
        top.bind("c", self.showChar)
        top.bind("<Return>", self.markCorrect)
        top.bind("<Shift_R>", self.markIncorrect)
        top.bind("<space>", self.cycleDisplay)
        
        self.newUnit.configure(command=self.promptNewUnit)
        self.charModeButton.configure(command=self.activateCharMode)
        self.pinyinModeButton.configure(command=self.activatePinyinMode)
        self.defModeButton.configure(command=self.activateDefMode)

        # Default show characters first
        self.activateCharMode()

        root.protocol("WM_DELETE_WINDOW", self.onClose)

        try:
            state = self.deserialize()
            units = copy.deepcopy(state['units'])
            for name in units:
                self.unitList.insert(END, name)
            self.makeUnitActive()
        except:
            pass

if __name__ == '__main__':
    vp_start_gui()

    


