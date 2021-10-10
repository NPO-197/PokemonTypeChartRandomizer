import mmap, shutil
    #mmap is used to memory-map the .gba file to help handel editing
    #shutil is used to copy files
import GeneralLatinSquare as GL
    #GeneralLatinSquare is used to generate the random typechart
import SpoilerLog
    #SpoilerLog is used to generate the spoiler log.

DEFAULTCHARTGEN6 = [
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

#Each matchup is stored in something called UQ_4_12 format?
#16 bit value with 0x0010 = 1.0 and 0x0008 = 0.5 ect...

def TypeChartToData(TypeChart):
    Hex=[0x10,0x20,0x08,0x00] #the least signifigant byte of the multiplier
    Data = []
    for i in range(len(TypeChart)):
        #insert Mystery Type
        if i == 9:
            for j in range(len(TypeChart)):
                #insert Mystery X Mystery
                if j == 9:
                    Data.extend([0x00,0x10]) #All Mystery type matchups are x1.0 by default
                Data.extend([0x00,0x10])

        for j in range(len(TypeChart)):
            #insert Mystery Type
            if j == 9:
                Data.extend([0x00,0x10])
            Data.extend([0x00,Hex[TypeChart[i][j]]])
    return(Data)

#Returns the inverse TypeChart
def InverseTypeChart(TypeChart):
    Inv = [0,2,1,1]  #Super Effective -> NotVeryEffective NotVery/NoEffect -> SuperEffective
    InvChart = []
    for i in range(len(TypeChart)):
        InvChart.append([])
        for j in range(len(TypeChart)):
            InvChart[i].append(Inv[TypeChart[i][j]])
    return InvChart

def Rando(inputfile,outputfile,mins,maxs,seed):
    # constraint matrix based on given mins and maxs
    cm = [[0,1,2,3],mins,maxs]
    # we generate a random type chart as a general latin square (so it's balanced)
    TypeChart = GL.RandGls(cm,18) # Emerald EX has the Fairy type so 18 types.
    SaveChart(inputfile,outputfile,TypeChart,seed)


#Used to generate a ROM with a custom type chart for Emerald EX.
def SaveChart(inputfile,outputfile,TypeChart,seed):
    TypeChartData = TypeChartToData(TypeChart) #Calc Chart data for EX ROM Format
    InverseData = TypeChartToData(InverseTypeChart(TypeChart)) #Calc Inverse Chart data for EX ROM Format
    TypeChartData.extend(InverseData) #We need to add the inverse chart data imeadiatly afterwards
    HexEdit(inputfile,outputfile,TypeChartData)
    SpoilerLog.Spoiler(6,outputfile[:-4]+'log.csv',TypeChart,seed)


def HexEdit(inputfile,outputfile,NewTypeChartData):
        #first make a copy of the input file so we can edit it without destroying the original file
        shutil.copy(inputfile,outputfile)

        f = open(outputfile, "r+b")

        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(),0)
        #Just go to the offset of the type chart and write in the new one!
        mm.seek(0x37AFC6)
        mm.write(bytearray(NewTypeChartData))
        #Don't forget to close the file when you are done!
        mm.close()
        return
