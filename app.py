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
from collections import namedtuple
from openpyxl import *
import random
import sys
import copy

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import main_support

# Data containers
"""
struct VocabWord {
  string character;
  string pinyin;
  string definition;
  int accessed;
  int correct;
};

unordered_map<string, vector<VocabWord>> units;

"""
## Ghetto struct
class Struct:
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

# Should have members: character, pinyin, definition, accessed, correct
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

units = {}

activeWord = False
activeUnit = False

hardMode = False
mode = 'character'

# Utility functions
def unitFromXLSX(path):
    global units
    vocab = []
    testUnit = load_workbook(path, read_only=True)
    sheet = testUnit['Sheet1']
    for row in sheet:
        newWord = VocabWord(character=row[0].value,
                            pinyin=row[1].value,
                            definition=row[2].value,
                            accessed=0,
                            correct=0)
        vocab.append(newWord)
        
    return vocab

    
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
    def showPinyin(self, event):
        self.vocabWordLabel.configure(text=activeWord.pinyin)
    
    def showDef(self, event):
        self.vocabWordLabel.configure(text=activeWord.definition)

    def showChar(self, event):
        self.vocabWordLabel.configure(text=activeWord.character)
    
    def nextWord(self,event):
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
            if (hardMode):
                if (rateCorrect > .66):
                    countWordsTooEasy += 1
                else:
                    break
            else:
                break

            if (countWordsTooEasy > 1000):
                messagebox.showinfo("Oops!", "It looks like this unit is too easy for you -- we couldn't find a word with less than 2/3 correct rate!")


        self.vocabWordLabel.configure(foreground=wordColorHexStr)
        self.vocabWordLabel.configure(text=activeWord.character)
        return


    def promptNewUnit(self):
        global activeUnit, activeWord
        unitName = simpledialog.askstring("New Unit!", "What's the name of the new unit?")
        root.withdraw()
        path = filedialog.askopenfilename()
        root.deiconify()
        
        newVocabList = unitFromXLSX(path)
        units[unitName] = newVocabList
        activeUnit = newVocabList
        activeWord = newVocabList[0]

        self.unitList.insert(END, unitName)
        self.vocabWordLabel.configure(text=activeWord.character)

    def markIncorrect(self, event):
        global activeWord
        activeWord.accessed += 1
        self.nextWord(event)
        
    def markCorrect(self, event):
        activeWord.accessed += 1
        activeWord.correct += 1
        self.nextWord(event)

    def toggleHard(self):
        global hardMode
        hardMode = True

    def activateDefMode():
        pass
    
    def activatePinyinMode():
        pass
     
    def __init__(self, top=None):
        # Init all static things (positions, colors) handled by PAGE
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font12 = "-family Georgia -size 12 -weight normal -slant roman"  \
            " -underline 0 -overstrike 0"
        font14 = "-family Georgia -size 9 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

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
        self.unitSelect.configure(font=font12)
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
        self.newUnit.configure(font=font12)
        self.newUnit.configure(foreground="#000000")
        self.newUnit.configure(highlightbackground="#d9d9d9")
        self.newUnit.configure(highlightcolor="black")
        self.newUnit.configure(pady="0")
        self.newUnit.configure(text='''Add New Unit''')
        self.newUnit.configure(width=296)

        self.vocabWordLabel = Label(top)
        self.vocabWordLabel.place(relx=0.46, rely=0.33, height=116, width=352)
        self.vocabWordLabel.configure(activebackground="#000080")
        self.vocabWordLabel.configure(activeforeground="white")
        self.vocabWordLabel.configure(activeforeground="#000000")
        self.vocabWordLabel.configure(background="#d9d9d9")
        self.vocabWordLabel.configure(disabledforeground="#a3a3a3")
        self.vocabWordLabel.configure(font=font12)
        self.vocabWordLabel.configure(foreground="#000000")
        self.vocabWordLabel.configure(highlightbackground="#d9d9d9")
        self.vocabWordLabel.configure(highlightcolor="black")
        self.vocabWordLabel.configure(text='''Select a unit to start''')

        self.toggleHardButton = Button(top)
        self.toggleHardButton.place(relx=0.39, rely=0.87, height=43, width=155)
        self.toggleHardButton.configure(activebackground="#d9d9d9")
        self.toggleHardButton.configure(activeforeground="#000000")
        self.toggleHardButton.configure(background="#d9d9d9")
        self.toggleHardButton.configure(borderwidth="3")
        self.toggleHardButton.configure(disabledforeground="#a3a3a3")
        self.toggleHardButton.configure(font=font14)
        self.toggleHardButton.configure(foreground="#000000")
        self.toggleHardButton.configure(highlightbackground="#d9d9d9")
        self.toggleHardButton.configure(highlightcolor="black")
        self.toggleHardButton.configure(padx="0")
        self.toggleHardButton.configure(pady="0")
        self.toggleHardButton.configure(text='''Toggle Hard Mode!''')
        self.toggleHardButton.configure(width=155)

        self.pinyinModeButton = Button(top)
        self.pinyinModeButton.place(relx=0.59, rely=0.87, height=43, width=155)
        self.pinyinModeButton.configure(activebackground="#d9d9d9")
        self.pinyinModeButton.configure(activeforeground="#000000")
        self.pinyinModeButton.configure(background="#d9d9d9")
        self.pinyinModeButton.configure(borderwidth="3")
        self.pinyinModeButton.configure(disabledforeground="#a3a3a3")
        self.pinyinModeButton.configure(font=font14)
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
        self.defModeButton.configure(font=font14)
        self.defModeButton.configure(foreground="#000000")
        self.defModeButton.configure(highlightbackground="#d9d9d9")
        self.defModeButton.configure(highlightcolor="black")
        self.defModeButton.configure(padx="0")
        self.defModeButton.configure(pady="0")
        self.defModeButton.configure(text='''Definition Mode!''')
        self.defModeButton.configure(width=175)

        
        # Init all programmatic things
        top.bind("n", self.nextWord)
        top.bind("p", self.showPinyin)
        top.bind("d", self.showDef)
        top.bind("c", self.showChar)
        top.bind("<space>", self.markCorrect)
        top.bind("<Return>", self.markIncorrect)
        self.newUnit.configure(command=self.promptNewUnit)
        self.toggleHardButton.configure(command=self.toggleHard)
        self.pinyinModeButton.configure(command=self.activatePinyinMode)
        self.defModeButton.configure(command=self.activateDefMode)

if __name__ == '__main__':
    vp_start_gui()

    


