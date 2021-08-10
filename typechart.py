from tkinter import *
import random
from tk_ToolTip_class101 import CreateToolTip
from tkSliderWidget import Slider
from GeneralLatinSquare import RandGls
from tkinter import filedialog
from tkinter import simpledialog
import HexEdit as HE

window = Tk()
window.title('Type Chart Randomizer')

window_leftside = PanedWindow(orient=VERTICAL,height=400)
window_sliders = PanedWindow()
window_rightside = PanedWindow(orient=VERTICAL)
window_MatchupButtonPane = PanedWindow()
window_filebuttons = PanedWindow()

#set up chart canvas with scroll bar
def scrollfunction(event):
    canvas_ChartCanvas.configure(scrollregion=canvas_ChartCanvas.bbox("all"),width=550,height=375)
    canvas_ChartCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
frame_myFrame = Frame(window_rightside,relief=GROOVE,width=50,height=200,bd=1)
canvas_ChartCanvas = Canvas(frame_myFrame)
frame_ChartPane = Frame(canvas_ChartCanvas)
myscrollbar=Scrollbar(frame_myFrame,orient="vertical",command=canvas_ChartCanvas.yview)
canvas_ChartCanvas.configure(yscrollcommand=myscrollbar.set)
myscrollbar.pack(side='right',fill='y')
canvas_ChartCanvas.pack(side='left')
canvas_ChartCanvas.create_window((0,0),window=frame_ChartPane,anchor='nw')
frame_ChartPane.bind("<Configure>",scrollfunction)
canvas_ChartCanvas.bind_all("<MouseWheel>", scrollfunction)


window_rightside.add(window_MatchupButtonPane)
window_rightside.add(frame_myFrame)
window_leftside.add(window_filebuttons)
window_leftside.add(window_sliders)
window_rightside.pack(side = 'right')
window_leftside.pack(side = 'left')


#window.pack()

FONTSIZE = 7
FONT = 'Helvetica'
DEFAULTCHART = [[0,0,0,0,0,2,0,3,2,0,0,0,0,0,0,0,0],
                [1,0,2,2,0,1,2,3,1,0,0,0,0,2,1,0,1],
                [0,1,0,0,0,2,1,0,2,0,0,1,2,0,0,0,0],
                [0,0,0,2,2,2,0,2,3,0,0,1,0,0,0,0,0],
                [0,0,3,1,0,1,2,0,1,1,0,2,1,0,0,0,0],
                [0,2,1,0,2,0,1,0,2,1,0,0,0,0,1,0,0],
                [0,2,2,2,0,0,0,2,2,2,0,1,0,1,0,0,1],
                [3,0,0,0,0,0,0,1,2,0,0,0,0,1,0,0,2],
                [0,0,0,0,0,1,0,0,2,2,2,0,2,0,1,0,0],
                [0,0,0,0,0,2,1,0,1,2,2,1,0,0,1,2,0],
                [0,0,0,0,1,1,0,0,0,1,2,2,0,0,0,2,0],
                [0,0,2,2,1,1,2,0,2,2,1,2,0,0,0,2,0],
                [0,0,1,0,3,0,0,0,0,0,1,2,2,0,0,2,0],
                [0,1,0,1,0,0,0,0,2,0,0,0,0,2,0,0,3],
                [0,0,1,0,1,0,0,0,2,2,2,1,0,0,2,1,0],
                [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0],
                [0,2,0,0,0,0,0,1,2,0,0,0,0,1,0,0,2]]


Buttons = []
ChartButtons = []
ChartLabels = []
TypeLables = []
TypeLables2 = []
MatchupsText = ['1','2','½','0']
MatchupsBgColors = ['white','green','red','black']
MatchupsFgColors = ['Black','Black','Black','White']
TypeNames = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark']
AbrevTypeNames =['NOR','FIG','FLY','POI','GRO','ROC','BUG','GHO','STE','FIR','WAT','GRA','ELE','PSY','ICE','DRA','DAR']
TypeColors = ['#A8A77A','#C22E28','#A98FF3','#A33EA1','#E2BF65','#B6A136','#A6B91A','#735797','#B7B7CE','#EE8130','#6390F0','#7AC74C','#F7D02C','#F95587','#96D9D6','#6F35FC','#705746']
var_buttoncolor = StringVar(window,value='red')
var_matchup = IntVar(window,value = 0)
var_activatesliders = IntVar(window,value = 0)
var_FileName = StringVar(window,value ='')
var_OutputFileName = StringVar(window,value='')
var_Seed = IntVar(window,value = 0)
class MatchupButton(Button):

    def __init__(self,master,matchup,text = '',height = 1,width =3,padx =4 ,pady =6,bd =4,bg = 'white',fg='black',highlightcolor='blue',name=''):
        Button.__init__(self,master,text=text,font = [FONT,FONTSIZE+3,'bold'],height = height,width=width,padx=padx,pady=pady,bd=bd,bg=bg,fg=fg,highlightcolor='blue',command=lambda : MatchupSelect(self))
        self.master = master
        self.defaultcolor = bg
        Buttons.append(self)
        self.name = text
        self.matchup = matchup

def MatchupSelect(button):
    for i in Buttons:
        i.configure(bg=i.defaultcolor)
    if not var_activatesliders.get():
        return
    button.configure(bg='grey')
    var_buttoncolor.set(button.defaultcolor)
    var_matchup.set(button.matchup)

class ChartButton(Button):

    def __init__(self,master,matchup,row,column,text = '',height = 1,width =3,padx =0 ,pady =0,bd =4):
        bg = MatchupsBgColors[matchup]
        fg = MatchupsFgColors[matchup]
        text = MatchupsText[matchup]
        Button.__init__(self,master,text=text,font = [FONT,FONTSIZE,'bold'],height = height,width=width,padx=padx,pady=pady,bd=bd,bg=bg,fg=fg,highlightcolor='blue',command=lambda : ChartSelect(self))
        self.master = master
        self.defaultcolor = bg
        self.matchup = matchup
        self.row = row
        self.column = column

    def NewMatchup(self,matchup):
        bg = MatchupsBgColors[matchup]
        fg = MatchupsFgColors[matchup]
        text = MatchupsText[matchup]
        self.configure(text=text,bg=bg,fg=fg)
        self.matchup = matchup
        i = self.row
        j = self.column
        ChartLabels[i][j].changetext(TypeNames[i]+'=>'+TypeNames[j]+': '+MatchupsText[matchup]+'x')

def ChartSelect(button):
    if not var_activatesliders.get():
        return
    button.NewMatchup(var_matchup.get())

#NOTE ChartButtons[i][j] is stored transposed from how it is displayed....

def UpdateChart(chart):
    for i in range(17):
        for j in range(17):
            ChartButtons[i][j].NewMatchup(chart[i][j])

def test():
    TypeMatchups=[]
    for i in range(17):
        TypeMatchups.append([])
        for j in range(17):
            TypeMatchups[i].append(ChartButtons[i][j].matchup)
    return TypeMatchups

button_100 = MatchupButton(window_MatchupButtonPane, text = '1×',matchup = 0)
button_200 = MatchupButton(window_MatchupButtonPane, text = '2×',bg = 'green',fg='white',matchup =1)
button_050 = MatchupButton(window_MatchupButtonPane, text = '½×', padx =3,bg = 'red',fg='white',matchup =2)
button_000 = MatchupButton(window_MatchupButtonPane, text = '0×',bg='black',fg='white',matchup =3)

button_test = Button(window_MatchupButtonPane, text = 'test',command = test)


label_TableKey = Label(window_MatchupButtonPane,text='Attack⬇ / Defense➡',font=[FONT,11,'bold'])


for i in range(17):
    ChartButtons.append([])
    ChartLabels.append([])
    TypeLables.append(Label(frame_ChartPane,text=AbrevTypeNames[i].upper(),bg=TypeColors[i],fg='white',height = 1,width=3,padx=2,pady =1,bd =4,font=[FONT,FONTSIZE,'bold']))
    TypeLables2.append(Label(frame_ChartPane,text=AbrevTypeNames[i].upper(),bg=TypeColors[i],fg='white',height = 1,width=3,padx=2,pady =1,bd =4,font=[FONT,FONTSIZE,'bold']))
    TypeLables[i].grid(row=i+1,column=0)
    TypeLables2[i].grid(row=0,column=i+1)

    for j in range(17):
        ChartButtons[i].append(ChartButton(frame_ChartPane, row = i,column = j,matchup = DEFAULTCHART[i][j]))
        ChartButtons[i][j].grid(row=i+1,column=j+1)
        ChartLabels[i].append(CreateToolTip(ChartButtons[i][j],TypeNames[i]+'=>'+TypeNames[j]+': '+MatchupsText[DEFAULTCHART[i][j]]+'x'))
for i in range(len(Buttons)):
    Buttons[i].grid(column=i,row=1)

#button_test.grid(column = 4,row =1)
label_TableKey.grid(row = 1,column=6)


def UpdateState():
    for slider in sliders:
        active = not var_activatesliders.get()
        slider.active = active
        slider.show_value = active
        slider.redraw()
    MatchupSelect(button_000)
check_Active = Checkbutton(window_MatchupButtonPane,text = "Edit",variable = var_activatesliders,command = UpdateState)
check_Active.grid(column =4,row = 1)

label_SliderInfo = Label(window_sliders,justify = LEFT,text='Adjust the sliders to set the min/max number of times \neach machup occurs in a given row/collumn. \nPress \"Example=>\" to see an example chart on the side.')

slider_1times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = 17, init_lis = [0,17], show_value = True)
slider_2times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = 17, init_lis = [2,7], show_value = True)
slider_5times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = 17, init_lis = [2,5], show_value = True)
slider_0times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = 17, init_lis = [0,1], show_value = True)
sliders = [slider_1times,slider_2times,slider_5times,slider_0times]
sliderlabels = []
sliderlabeltext = ['1-times','2-times','0.5-times','0-times']

label_SliderInfo.grid(row = 0,column = 1)
for i in range(4):
    sliderlabels.append(Label(window_sliders,text=sliderlabeltext[i]))
    sliderlabels[i].grid(row=i+1,column=0)
    sliders[i].grid(row=i+1,column=1)



def generate():
    mins = []
    maxs = []
    for slider in sliders:
        mins.append(int(slider.getValues()[0]))
        maxs.append(int(slider.getValues()[1]))
    cm = [[0,1,2,3],mins,maxs]
    try:
        chart = RandGls(cm,17)
        UpdateChart(chart)
        lable_Error.configure(text='')
    except ValueError as error:
        if str(error).split('\n')[0] == 'summax < n':
            errorstring = 'Maximum number of matchups is less then 17\nPlease adjust sliders so that a matchup chart is possible'
        else:
            errorstring = 'Minimum number of matchups is greater then 17\nPlease adjust sliders so that a matchup chart is possible'
        lable_Error.configure(text=errorstring)


button_generate=Button(window_sliders,text='Example=>',command = generate)
lable_Error = Label(window_sliders,text='')


button_generate.grid(row = 10,column =1)
lable_Error.grid(row =11,column=1)

def openrom():
    filename = filedialog.askopenfilename(initialdir = './', title = 'Open ROM', filetypes=(('GameBoyColor file','*.gbc'),('all files','*.*')))
    if filename == '':
        button_SaveExample.configure(state=DISABLED)
        button_RandomizeROM.configure(state=DISABLED)
        return
    var_FileName.set(filename)
    filenameshort = filename.split('/')[-1]
    label_RomInfo.configure(text = 'ROM Info: '+filenameshort)
    button_RandomizeROM.configure(state = NORMAL)
    button_SaveExample.configure(state = NORMAL)


def randomize():
    filename = filedialog.asksaveasfilename(initialdir = './',title = 'Save As', filetypes = (('GameBoyColor file','*.gbc'),('all files','*.*')))
    if filename =='':
        return
    if filename.split('.')[-1] != 'gbc':
        filename = filename+'.gbc'
    var_OutputFileName.set(filename)
    answer = simpledialog.askstring("Input", "Enter a Seed, (Leave Blank for random seed)",parent=window)
    if answer !='':
        seed = answer
    else:
        seed = random.randrange(2147483647)
    mins = []
    maxs = []
    for slider in sliders:
        mins.append(int(slider.getValues()[0]))
        maxs.append(int(slider.getValues()[1]))
    HE.Rando(var_FileName.get(),var_OutputFileName.get(),mins,maxs,seed)

def SaveExample():
    filename = filedialog.asksaveasfilename(initialdir = './',title = 'Save As', filetypes = (('GameBoyColor file','*.gbc'),('all files','*.*')))
    if filename =='':
        return
    if filename.split('.')[-1] != 'gbc':
        filename = filename+'.gbc'
    var_OutputFileName.set(filename)
    seed = 'Custom Type Chart'
    TypeChart = test()
    HE.SaveChart(var_FileName.get(),var_OutputFileName.get(),TypeChart,seed)


button_OpenROM=Button(window_filebuttons,text='OpenROM',command = openrom)
label_RomInfo = Label(window_filebuttons,text='ROM Info:')
button_RandomizeROM=Button(window_filebuttons,text='Randomize ROM',command = randomize,state = DISABLED)
button_SaveExample=Button(window_filebuttons,text='Save ROM Using Example Chart',command = SaveExample,state = DISABLED)

button_OpenROM.grid(row = 0,column = 0)
label_RomInfo.grid(row = 0,column = 1)
button_RandomizeROM .grid(row = 1,column = 0)
button_SaveExample.grid(row=2,column=0)












window.mainloop()
