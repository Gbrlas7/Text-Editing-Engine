ISCONTINUE=True
OUTPUT = ""
CURSORPOSITION = 0
CURSORONOFF = False
HISTORY = []
COMMANDHISTORY = []
def helpInfo():
    print("? - display this help info")
    print(". - toggle row cursor on and off")
    print("h - move cursor left")
    print("l - move cursor right")
    print("^ - move cursor to beginning of the line")
    print("$ - move cursor to end of the line")
    print("w - move cursor to beginning of next word")
    print("b - move cursor to beginning of previous word")
    print("i - insert <text> before cursor")
    print("a - Append <text> after cursor")
    print("x - delete character at cursor")
    print("dw - delete word and trailing spaces at cursor")
    print("u - undo previous command")
    print("r - repeat last command")
    print("q - quit program")
def showContent():
    global OUTPUT, CURSORPOSITION, CURSORONOFF
    if OUTPUT:
        if CURSORONOFF and CURSORPOSITION < len(OUTPUT):
            print(OUTPUT[:CURSORPOSITION] + "\033[42m" + OUTPUT[CURSORPOSITION] + "\033[0m" + OUTPUT[CURSORPOSITION+1:])
        else:
            print(OUTPUT)
def toggleCursor():
    global CURSORONOFF
    CURSORONOFF = not CURSORONOFF

def cursorLeft():
    global CURSORPOSITION
    if CURSORPOSITION>0:
        CURSORPOSITION-=1
def cursorRight():
    global CURSORPOSITION,OUTPUT
    if CURSORPOSITION<len(OUTPUT):
        CURSORPOSITION+=1
def cursorBeginning():
    global CURSORPOSITION
    CURSORPOSITION = 0
def cursorEnd():
    global CURSORPOSITION,OUTPUT
    CURSORPOSITION=len(OUTPUT)-1
def cursorNext():
    global CURSORPOSITION,OUTPUT
    initial = CURSORPOSITION
    while OUTPUT[CURSORPOSITION]!=" ":
        if CURSORPOSITION<len(OUTPUT)-1:
            CURSORPOSITION+=1
        else: 
            CURSORPOSITION=initial
            break
    while OUTPUT[CURSORPOSITION]==" ":
        if CURSORPOSITION<len(OUTPUT)-1:
            CURSORPOSITION+=1
        else: 
            CURSORPOSITION=initial
            break
def cursorPrevious():
    global CURSORPOSITION,OUTPUT
    while CURSORPOSITION>0 and OUTPUT[CURSORPOSITION-1]==" ":
        CURSORPOSITION-=1
    while CURSORPOSITION>0 and OUTPUT[CURSORPOSITION-1]!=" ":
        CURSORPOSITION-=1
def insertText(text):
    global CURSORPOSITION, OUTPUT
    OUTPUT = OUTPUT[:CURSORPOSITION] + text + OUTPUT[CURSORPOSITION:]
def appendText(text):
    global CURSORPOSITION, OUTPUT
    OUTPUT = OUTPUT[:CURSORPOSITION+1] + text + OUTPUT[CURSORPOSITION+1:]
    if CURSORPOSITION==0:
        CURSORPOSITION += len(text)-1
    else:
        CURSORPOSITION += len(text)
def delete():
    global CURSORPOSITION, OUTPUT
    OUTPUT = OUTPUT[:CURSORPOSITION] + OUTPUT[CURSORPOSITION+1:]
def deleteWord():
    global CURSORPOSITION, OUTPUT
    endpoint = CURSORPOSITION
    while endpoint<len(OUTPUT) and OUTPUT[endpoint]!=" ":
        endpoint+=1
    while endpoint<len(OUTPUT) and OUTPUT[endpoint]==" ":
        endpoint+=1
    OUTPUT = OUTPUT[:CURSORPOSITION] + OUTPUT[endpoint:]
    if CURSORPOSITION>len(OUTPUT)-1:
        CURSORPOSITION=len(OUTPUT)-1
def undo():
    global OUTPUT, CURSORPOSITION, HISTORY, COMMANDHISTORY
    if HISTORY:
        HISTORY.pop()
        if COMMANDHISTORY:
            COMMANDHISTORY.pop()
        if HISTORY:
            OUTPUT, CURSORPOSITION = HISTORY[-1]
        else:
            OUTPUT, CURSORPOSITION = "", 0
def repeat():
    global COMMANDHISTORY
    if COMMANDHISTORY:
        lastCommand = COMMANDHISTORY[-1]
        execute(lastCommand, repeatable=False)        
def save(command):
    global OUTPUT, CURSORPOSITION, HISTORY, COMMANDHISTORY
    HISTORY.append((OUTPUT, CURSORPOSITION))
    COMMANDHISTORY.append(command)
def execute(command, repeatable=True):
    global OUTPUT, CURSORPOSITION, ISCONTINUE
    if command=='?':
        helpInfo()
    elif command=='s':
        showContent()
    elif command=='.':
        toggleCursor()
        showContent()
    elif command=='h':
        cursorLeft()
        showContent()
    elif command=='l':
        cursorRight()
        showContent()
    elif command=='^':
        cursorBeginning()
        showContent()
    elif command=='$':
        cursorEnd()
        showContent()
    elif command=='w':
        cursorNext()
        showContent()
    elif command=='b':
        cursorPrevious()
        showContent()
    elif command.startswith('i'):
        text = command[1:]
        if text:
            insertText(text)
        showContent()
    elif command.startswith('a'):
        text = command[1:]
        if text:
            appendText(text)
        showContent()
    elif command=='x':
        delete()
        showContent()
    elif command=='dw':
        deleteWord()
        showContent()
    elif command=='u':
        undo()
        showContent()
    elif command=='r':
        repeat()
    elif command=='q':
        ISCONTINUE=False
    if (command in ['?','s','.','h','l','^','$','w','b','x','dw'] or command.startswith(('i','a'))) and repeatable:
        save(command)
def main():
    while ISCONTINUE:
        command = input(">")
        if not command:
            continue
        execute(command)
main()