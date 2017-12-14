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
VocabWord = namedtuple('VocabWord', ['character', 'pinyin', 'definition'])
units = {}
activeVocabList = []
activeWord = 0

testWord = VocabWord(character='我', pinyin="wo", definition="I");
activeVocabList = [testWord]
activeWord = testWord

units["test"] = copy.deepcopy(activeVocabList)

# Utility functions
def unitFromXLSX(path):
    global units
    vocab = []
    testUnit = load_workbook(path, read_only=True)
    sheet = testUnit['Sheet1']
    for row in sheet:
        newWord = VocabWord(character=row[0].value,
                            pinyin=row[1].value,
                            definition=row[2].value)
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
        self.notecardButton.configure(text=activeWord.pinyin)
    
    def showDef(self, event):
        self.notecardButton.configure(text=activeWord.definition)
    
    def nextWord(self,event):
        global activeWord, activeVocabList
        activeWord = random.choice(activeVocabList)
        print(activeWord)
        self.notecardButton.configure(text=activeWord.character)
        
    def promptNewUnit(self):
        global activeVocabList, activeWord
        unitName = simpledialog.askstring("New Unit!", "What's the name of the new unit?")
        root.withdraw()
        path = filedialog.askopenfilename()
        root.deiconify()
        
        newVocabList = unitFromXLSX(path)
        units[unitName] = newVocabList
        activeVocabList = newVocabList
        activeWord = newVocabList[0]

        self.unitList.insert(END, unitName)
        self.notecardButton.configure(text=activeWord.character)
        self.notecardButton.configure(command=self.showDef)
    

    def __init__(self, top=None):
        # Init all static things (positions, colors) handled by PAGE
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font10 = "-family {Segoe UI} -size 24 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("901x450+511+97")
        top.title("Chinese")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")



        self.notecardButton = Button(top)
        self.notecardButton.place(relx=0.52, rely=0.24, height=203, width=266)
        self.notecardButton.configure(activebackground="#d9d9d9")
        self.notecardButton.configure(activeforeground="#000000")
        self.notecardButton.configure(background="#d9d9d9")
        self.notecardButton.configure(disabledforeground="#a3a3a3")
        self.notecardButton.configure(font=font10)
        self.notecardButton.configure(foreground="#000000")
        self.notecardButton.configure(highlightbackground="#d9d9d9")
        self.notecardButton.configure(highlightcolor="black")
        self.notecardButton.configure(pady="0")
        self.notecardButton.configure(text='''Button''')
        self.notecardButton.configure(width=266)

        self.unitList = Listbox(top)
        self.unitList.place(relx=0.01, rely=0.11, relheight=0.73, relwidth=0.33)
        self.unitList.configure(background="white")
        self.unitList.configure(disabledforeground="#a3a3a3")
        self.unitList.configure(font="TkFixedFont")
        self.unitList.configure(foreground="#000000")
        self.unitList.configure(width=294)

        self.unitSelect = Label(top)
        self.unitSelect.place(relx=0.11, rely=0.02, height=26, width=102)
        self.unitSelect.configure(background="#d9d9d9")
        self.unitSelect.configure(disabledforeground="#a3a3a3")
        self.unitSelect.configure(foreground="#000000")
        self.unitSelect.configure(text='''Select Unit''')
        self.unitSelect.configure(width=102)

        self.newUnit = Button(top)
        self.newUnit.place(relx=0.01, rely=0.89, height=33, width=296)
        self.newUnit.configure(activebackground="#d9d9d9")
        self.newUnit.configure(activeforeground="#000000")
        self.newUnit.configure(background="#d9d9d9")
        self.newUnit.configure(disabledforeground="#a3a3a3")
        self.newUnit.configure(foreground="#000000")
        self.newUnit.configure(highlightbackground="#d9d9d9")
        self.newUnit.configure(highlightcolor="black")
        self.newUnit.configure(pady="0")
        self.newUnit.configure(text='''Add New Unit''')
        self.newUnit.configure(width=296)
        
        # Init all programmatic things
        top.bind("n", self.nextWord)
        top.bind("p", self.showPinyin)
        top.bind("d", self.showDef)
        self.newUnit.configure(command=self.promptNewUnit)

if __name__ == '__main__':
    vp_start_gui()

    


