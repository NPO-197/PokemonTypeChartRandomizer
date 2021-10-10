"""
typechart.py GUI for pokemon type chart randomizer made by NPO-119

"""

from tkinter import *
import random
from tk_ToolTip_class101 import CreateToolTip
from tkSliderWidget import Slider
from GeneralLatinSquare import RandGls
from tkinter import filedialog
from tkinter import simpledialog
import HexEdit as HE
import DetectROM
import HexEditGen3,HexEditGen3EX

window = Tk()
window.title('Type Chart Randomizer')

window_leftside = PanedWindow(orient=VERTICAL,height=400)
window_sliders = PanedWindow()
window_rightside = PanedWindow(orient=VERTICAL)
window_MatchupButtonPane = PanedWindow()
window_filebuttons = PanedWindow()

#set up chart canvas with scroll bar
def scrollfunction(event):
    canvas_ChartCanvas.configure(scrollregion=canvas_ChartCanvas.bbox("all"),width=570,height=400)
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
DEFAULTCHARTU = [[0,0,0,0,0,2,0,3,2,0,0,0,0,0,0,0,0],
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
DEFAULTCHART = [
                [0,0,0,0,0,2,0,3,2,0,0,0,0,0,0,0,0,0],
                [1,0,2,2,0,1,2,3,1,0,0,0,0,2,1,0,1,2],
                [0,1,0,0,0,2,1,0,2,0,0,1,2,0,0,0,0,0],
                [0,0,0,2,2,2,0,2,3,0,0,1,0,0,0,0,0,1],
                [0,0,3,1,0,1,2,0,1,1,0,2,1,0,0,0,0,0],
                [0,2,1,0,2,0,1,0,2,1,0,0,0,0,1,0,0,0],
                [0,2,2,2,0,0,0,2,2,2,0,1,0,1,0,0,1,2],
                [3,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,2,0],
                [0,0,0,0,0,1,0,0,2,2,2,0,2,0,1,0,0,1],
                [0,0,0,0,0,2,1,0,1,2,2,1,0,0,1,2,0,0],
                [0,0,0,0,1,1,0,0,0,1,2,2,0,0,0,2,0,0],
                [0,0,2,2,1,1,2,0,2,2,1,2,0,0,0,2,0,0],
                [0,0,1,0,3,0,0,0,0,0,1,2,2,0,0,2,0,0],
                [0,1,0,1,0,0,0,0,2,0,0,0,0,2,0,0,3,0],
                [0,0,1,0,1,0,0,0,2,2,2,1,0,0,2,1,0,0],
                [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,3],
                [0,2,0,0,0,0,0,1,0,0,0,0,0,1,0,0,2,2],
                [0,1,0,2,0,0,0,0,2,2,0,0,0,0,0,1,1,0]]



Buttons = []
global ChartButtons
ChartButtons= []
ChartLabels = []
TypeLables = []
TypeLables2 = []
MatchupsText = ['1','2','½','0']
MatchupsBgColors = ['white','#26a426','#fa2424','black']
MatchupsFgColors = ['Black','Black','Black','White']

TypeNamesU =     ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark','Fairy']
AbrevTypeNamesU =['NOR','FIG','FLY','POI','GRO','ROC','BUG','GHO','STE','FIR','WAT','GRA','ELE','PSY','ICE','DRA','DAR','FAI']
TypeColorsU =    ['#A8A77A','#C22E28','#A98FF3','#A33EA1','#E2BF65','#B6A136','#A6B91A','#735797','#B7B7CE','#EE8130','#6390F0','#7AC74C','#F7D02C','#F95587','#96D9D6','#6F35FC','#705746','#D685AD']

TypeNamesGen6 = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
AbrevTypeNamesGen6= ['BUG', 'DAR', 'DRA', 'ELE', 'FAI', 'FIG', 'FIR', 'FLY', 'GHO', 'GRA', 'GRO', 'ICE', 'NOR', 'POI', 'PSY', 'ROC', 'STE', 'WAT']
TypeColorsGen6= ['#A6B91A', '#705746', '#6F35FC','#F7D02C','#D685AD', '#C22E28', '#EE8130', '#A98FF3', '#735797', '#7AC74C', '#E2BF65', '#96D9D6', '#A8A77A', '#A33EA1', '#F95587', '#B6A136', '#B7B7CE', '#6390F0']
TypeIndexGen6 = [6, 16, 15, 12, 17, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]

TypeNamesGen2 = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
AbrevTypeNamesGen2= ['BUG', 'DAR', 'DRA', 'ELE', 'FIG', 'FIR', 'FLY', 'GHO', 'GRA', 'GRO', 'ICE', 'NOR', 'POI', 'PSY', 'ROC', 'STE', 'WAT']
TypeColorsGen2= ['#A6B91A', '#705746', '#6F35FC','#F7D02C', '#C22E28', '#EE8130', '#A98FF3', '#735797', '#7AC74C', '#E2BF65', '#96D9D6', '#A8A77A', '#A33EA1', '#F95587', '#B6A136', '#B7B7CE', '#6390F0']
TypeIndexGen2 = [6, 16, 15, 12, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]

TypeNamesGen1 = ['Bug', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Water']
AbrevTypeNamesGen1= ['BUG', 'DRA', 'ELE', 'FIG', 'FIR', 'FLY', 'GHO', 'GRA', 'GRO', 'ICE', 'NOR', 'POI', 'PSY', 'ROC', 'WAT']
TypeColorsGen1= ['#A6B91A', '#6F35FC','#F7D02C', '#C22E28', '#EE8130', '#A98FF3', '#735797', '#7AC74C', '#E2BF65', '#96D9D6', '#A8A77A', '#A33EA1', '#F95587', '#B6A136', '#6390F0']
TypeIndexGen1 = [6, 14, 11, 1, 8, 2, 7, 10, 4, 13, 0, 3, 12, 5, 9]



var_buttoncolor = StringVar(window,value='red')
var_matchup = IntVar(window,value = 0)
var_activatesliders = IntVar(window,value = 0)
var_Gen = IntVar(window,value = 2)
var_FileName = StringVar(window,value ='')
var_ROMType = IntVar(window,value=0)
var_OutputFileName = StringVar(window,value='')
var_Seed = IntVar(window,value = 0)
var_NumTypes = IntVar(window,value=18)
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
        TypeNames = TypeNamesGen6
        if var_Gen.get()==0:
            TypeNames = TypeNamesGen1
        if var_Gen.get()==1:
            TypeNames = TypeNamesGen2
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
    TypeIndex = TypeIndexGen6
    if var_Gen.get() == 0:
        TypeIndex = TypeIndexGen1
    if var_Gen.get() == 1:
        TypeIndex = TypeIndexGen2
    for i in range(var_NumTypes.get()):
        for j in range(var_NumTypes.get()):
            ChartButtons[i][j].NewMatchup(chart[TypeIndex[i]][TypeIndex[j]])



def test():
    TypeIndex = TypeIndexGen6
    if var_Gen.get() == 0:
        TypeIndex = TypeIndexGen1
    if var_Gen.get() == 1:
        TypeIndex = TypeIndexGen2
    TypeMatchups=[[0 for x in range(var_NumTypes.get())] for i in range(var_NumTypes.get())]
    for i in range(var_NumTypes.get()):
        for j in range(var_NumTypes.get()):
            TypeMatchups[TypeIndex[i]][TypeIndex[j]]=ChartButtons[i][j].matchup
    return TypeMatchups

button_100 = MatchupButton(window_MatchupButtonPane, text = '1×',matchup = 0)
button_200 = MatchupButton(window_MatchupButtonPane, text = '2×',bg = '#26a426',fg='white',matchup =1)
button_050 = MatchupButton(window_MatchupButtonPane, text = '½×', padx =3,bg = '#fa2424',fg='white',matchup =2)
button_000 = MatchupButton(window_MatchupButtonPane, text = '0×',bg='black',fg='white',matchup =3)

button_test = Button(window_MatchupButtonPane, text = 'test',command = test)


label_TableKey = Label(window_MatchupButtonPane,text='Attack⬇ / Defense➡',font=[FONT,11,'bold'])


def InitChartPane():
    global ChartButton
    global ChartLabels
    global TypeLables
    global TypeLables2

    TypeColors = TypeColorsGen6
    TypeNames = TypeNamesGen6
    AbrevTypeNames = AbrevTypeNamesGen6
    TypeIndex = TypeIndexGen6

    if var_Gen.get()==0:
        TypeColors = TypeColorsGen1
        TypeNames = TypeNamesGen1
        AbrevTypeNames = AbrevTypeNamesGen1
        TypeIndex = TypeIndexGen1
    if var_Gen.get()==1:
        TypeColors = TypeColorsGen2
        TypeColors = TypeColorsGen2
        TypeNames = TypeNamesGen2
        AbrevTypeNames = AbrevTypeNamesGen2
        TypeIndex = TypeIndexGen2

    for i in range(var_NumTypes.get()):
        AtkTypeName = TypeNames[i]
        ChartButtons.append([])
        ChartLabels.append([])
        TypeLables.append(Label(frame_ChartPane,text=AbrevTypeNames[i].upper(),bg=TypeColors[i],fg='white',height = 1,width=3,padx=2,pady =1,bd =4,font=[FONT,FONTSIZE,'bold']))
        TypeLables2.append(Label(frame_ChartPane,text=AbrevTypeNames[i].upper(),bg=TypeColors[i],fg='white',height = 1,width=3,padx=2,pady =1,bd =4,font=[FONT,FONTSIZE,'bold']))
        TypeLables[i].grid(row=i+1,column=0)
        TypeLables2[i].grid(row=0,column=i+1)

        for j in range(var_NumTypes.get()):
            DefTypeName = TypeNames[j]
            ChartButtons[i].append(ChartButton(frame_ChartPane, row = i,column = j,matchup = DEFAULTCHART[TypeIndex[i]][TypeIndex[j]]))
            ChartButtons[i][j].grid(row=i+1,column=j+1)
            ChartLabels[i].append(CreateToolTip(ChartButtons[i][j],TypeNames[i]+'=>'+TypeNames[j]+': '+MatchupsText[DEFAULTCHART[TypeIndex[i]][TypeIndex[j]]]+'x'))



#Initiate the Chart Pane
InitChartPane()

for i in range(len(Buttons)):
    Buttons[i].grid(column=i,row=1)





label_TableKey.grid(row = 1,column=8)

#sliders
def UpdateState():
    for slider in sliders:
        active = not var_activatesliders.get()
        slider.active = active
        slider.show_value = active
        slider.redraw()
    MatchupSelect(button_000)



def SwapGens():
    global ChartButtons
    global ChartLabels
    global TypeLables
    global TypeLables2
    for i in range(len(ChartButtons)):
        TypeLables[i].destroy()
        TypeLables2[i].destroy()
        for j in range(len(ChartButtons[i])):
            ChartButtons[i][j].destroy()
            ChartLabels[i][j].destroy()
    ChartButtons = []
    ChartLabels = []
    TypeLables = []
    TypeLables2 = []
    TypesPerGen=[15,17,18]
    var_NumTypes.set(TypesPerGen[var_Gen.get()])
    for slider in sliders:
        slider.max_val = var_NumTypes.get()
        slider.redraw()
    InitChartPane()

check_Active = Checkbutton(window_MatchupButtonPane,text = "Edit",variable = var_activatesliders,command = UpdateState)
check_Active.grid(column =4,row = 1)
radio_Gen1 = Radiobutton(window_MatchupButtonPane,text = "Gen1",variable=var_Gen,value=0,command = SwapGens,state=DISABLED)
radio_Gen2p=Radiobutton(window_MatchupButtonPane,text="Gen2+",variable=var_Gen,value=1,command = SwapGens)
radio_Gen6p=Radiobutton(window_MatchupButtonPane,text="Gen6+",variable=var_Gen,value=2,command=SwapGens)
radio_Gen1.grid(column = 5, row =1)
radio_Gen2p.grid(column = 6,row =1)
radio_Gen6p.grid(column =7,row=1)
ttp_radio_Gen1 = CreateToolTip(radio_Gen1,'Gen 1 ROMs not supported yet.')


label_SliderInfo = Label(window_sliders,justify = LEFT,text='Adjust the sliders to set the min/max number of times \neach machup occurs in a given row/collumn. \nPress \"Example=>\" to see an example chart on the side.')

slider_1times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = var_NumTypes.get(), init_lis = [0,var_NumTypes.get()], show_value = True)
slider_2times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = var_NumTypes.get(), init_lis = [2,7], show_value = True)
slider_5times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = var_NumTypes.get(), init_lis = [2,5], show_value = True)
slider_0times = Slider(window_sliders, width = 300, height = 40, min_val = 0, max_val = var_NumTypes.get(), init_lis = [0,1], show_value = True)
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
        chart = RandGls(cm,var_NumTypes.get())
        UpdateChart(chart)
        lable_Error.configure(text='')
    except ValueError as error:
        if str(error).split('\n')[0] == 'summax < n':
            errorstring = 'Maximum number of matchups is less then number of types\nPlease adjust sliders so that a matchup chart is possible'
        else:
            errorstring = 'Minimum number of matchups is greater then number of types\nPlease adjust sliders so that a matchup chart is possible'
        lable_Error.configure(text=errorstring)


button_generate=Button(window_sliders,text='Example=>',command = generate)
lable_Error = Label(window_sliders,text='')


button_generate.grid(row = 10,column =1)
lable_Error.grid(row =11,column=1)

def openrom():
    filename = filedialog.askopenfilename(initialdir = './', title = 'Open ROM', filetypes=(('gbc/gba file','*.gb*'),('all files','*.*')))
    if filename == '':
        button_SaveExample.configure(state=DISABLED)
        button_RandomizeROM.configure(state=DISABLED)
        var_FileName.set('')
        return
    Detect = DetectROM.TestROM(filename)
    var_ROMType.set(Detect[1])
    if Detect[1] == 0:
        button_SaveExample.configure(state=DISABLED)
        button_RandomizeROM.configure(state=DISABLED)
        label_RomInfo.configure(text = 'ROM Info:'+Detect[0])
        var_FileName.set('')
        return
    if var_Gen.get()!=1 and (Detect[1]in [1,2,3]):
        var_Gen.set(1)
        SwapGens()
    if var_Gen.get()!=2 and (Detect[1]==4):
        var_Gen.set(2)
        SwapGens()

    var_FileName.set(filename)
    filenameshort = filename.split('/')[-1]
    label_RomInfo.configure(text = 'ROM Info:'+Detect[0])
    button_RandomizeROM.configure(state = NORMAL)
    button_SaveExample.configure(state = NORMAL)


def randomize():
    if var_FileName.get().split('.')[-1]=='gba':
        filename = filedialog.asksaveasfilename(initialdir = './',title = 'Save As', filetypes = (('GameBoyAdvance file','*.gba'),('all files','*.*')))
        if filename =='':
            return
        if filename[-4:] !='.gba':
            filename = filename+'.gba'
    else:
        filename = filedialog.asksaveasfilename(initialdir = './',title = 'Save As', filetypes = (('GameBoyColor file','*.gbc'),('all files','*.*')))
        if filename =='':
            return
        if filename[-4:] !='.gbc':
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
    if var_ROMType.get() <= 2:
        HE.Rando(var_FileName.get(),var_OutputFileName.get(),mins,maxs,seed)
    if var_ROMType.get() == 3:
        HexEditGen3.Rando(var_FileName.get(),var_OutputFileName.get(),mins,maxs,seed)
    if var_ROMType.get() == 4:
        HexEditGen3EX.Rando(var_FileName.get(),var_OutputFileName.get(),mins,maxs,seed)


def SaveExample():
    if var_FileName.get().split('.')[-1]=='gba':
        filename = filedialog.asksaveasfilename(initialdir = './',title = 'Save As', filetypes = (('GameBoyAdvance file','*.gba'),('all files','*.*')))
        if filename =='':
            return
        if filename[-4:] !='.gba':
            filename = filename+'.gba'
    else:
        filename = filedialog.asksaveasfilename(initialdir = './',title = 'Save As', filetypes = (('GameBoyColor file','*.gbc'),('all files','*.*')))
        if filename =='':
            return
        if filename[-4:] !='.gbc':
            filename = filename+'.gbc'
    var_OutputFileName.set(filename)
    seed = 'Custom Type Chart'
    TypeChart = test()
    if var_ROMType.get()<=2:
        HE.SaveChart(var_FileName.get(),var_OutputFileName.get(),TypeChart,seed)
    if var_ROMType.get()==3:
        HexEditGen3.SaveChart(var_FileName.get(),var_OutputFileName.get(),TypeChart,seed)
    if var_ROMType.get()==4:
        HexEditGen3EX.SaveChart(var_FileName.get(),var_OutputFileName.get(),TypeChart,seed)

button_OpenROM=Button(window_filebuttons,text='OpenROM',command = openrom)
label_RomInfo = Label(window_filebuttons,text='ROM Info:')
button_RandomizeROM=Button(window_filebuttons,text='Randomize ROM',command = randomize,state = DISABLED)
button_SaveExample=Button(window_filebuttons,text='Save ROM Using Example Chart',command = SaveExample,state = DISABLED)

button_OpenROM.grid(row = 0,column = 0)
label_RomInfo.grid(row = 1,column = 0)
button_RandomizeROM .grid(row = 2,column = 0)
button_SaveExample.grid(row=3,column=0)

window.mainloop()
