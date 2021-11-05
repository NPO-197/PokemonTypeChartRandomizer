"""
Python Code to Hex edit varios pokemon ROMs to allow for randomized Type Charts by NPO-197
"""

import mmap
from shutil import copy
    #mmap is used to memory-map the .gbc file to help handel editing
    #shutil is used to copy files
import GeneralLatinSquare
    #GeneralLatinSquare is used to generate the random typechart
import SpoilerLog
    #SpoilerLog is used to generate the spoiler log.
import PokemonROMInfo


def ToMatrixFormatGen2(TypeChart):
    #Matrix format, AttackingType is the Row, DefendingType is the column, Matchups form the 2d matrix
    #Gen2 ROMs are modifyed to accept this smaller format instead of the default ListFormat,
    #There simply isn't enough free space at the end of the ROM bank to fit list format
    TypeChartData = []
    matchups = [0x0A,0x14,0x05,0x00]
    for row in TypeChart:
        for m in row:
            TypeChartData.append(matchups[m])
    return bytearray(TypeChartData)

def ToListFormatGen3(TypeChart):
    # List Format, Attacking,Defending,Matchup list of every non-neutral matchup
    # This seems to be the general method for storing the type chart in all offical games
    matchups = [0x0A,0x14,0x05,0x00]
    TypeChartList = []
    Imunities = []
    for i in range(len(TypeChart)):
        for j in range(len(TypeChart[0])):
            AtkType = i
            DefType = j
            Matchup = matchups[TypeChart[i][j]]
            #Adjust for TYPE_MYSTERY
            if AtkType>8:
                AtkType+=1
            if DefType>8:
                DefType+=1
            #Put Imunities at the end (after Forsight breakpoint)
            # This means that Forsight ignores all imunities now, not just Ghost's.
            if Matchup == 0x00:
                Imunities.extend([AtkType,DefType,Matchup])
                continue
            #Ignore Neutral Matchups
            if Matchup == 0x0A:
                continue
            #Put NotVerry / Super Effective into the list
            TypeChartList.extend([AtkType,DefType,Matchup])

    TypeChartList.extend([0xFE,0xFE,0x00])#Foresight break point
    TypeChartList.extend(Imunities)
    TypeChartList.extend([0xFF,0xFF,0x00])#End of matchups list
    return bytearray(TypeChartList)

def InverseTypeChart(TypeChart):
    Inv = [0,2,1,1]  #Super Effective -> NotVeryEffective NotVery/NoEffect -> SuperEffective
    InvChart = []
    for i in range(len(TypeChart)):
        InvChart.append([])
        for j in range(len(TypeChart)):
            InvChart[i].append(Inv[TypeChart[i][j]])
    return InvChart

#Pokemon Emerald EX format
def ToMatrixUQ_4_12Gen6(TypeChart):
    # Matrix format, AttackingType is the Row, DefendingType is the column, Matchups form the 2d matrix
    # Each matchup is a 2byte number with the most signifigant byte being zero.
    # Custom Format used in Emerald EX, probably to make randomizing the chart easier, and to make damage calcs simpler
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
    return bytearray(Data)


    #Used to generate a ROM with a random type chart based on the settings


def Rando(inputfile,outputfile,mins,maxs,RomInfo,seed):

    n = RomInfo.NumberOfTypes
    cm = [[0,1,2,3],mins,maxs]
    TypeChart = GeneralLatinSquare.RandGls(cm,n)

    SaveChart(inputfile,outputfile,TypeChart,RomInfo,seed)

#Used to generate a ROM with a given type chart
def SaveChart(inputfile,outputfile,TypeChart,RomInfo,seed):
    #Generate the SpoilerLog
    SpoilerLog.Spoiler(outputfile[:-4]+'log.csv',TypeChart,seed,RomInfo.NumberOfTypes)
    #Generate the typechart data in the format expected by the ROM
    tfc = RomInfo.typechartformat
    if tfc == PokemonROMInfo.TCformat.MatrixFormatGen2:
        NewTypeChartData = ToMatrixFormatGen2(TypeChart)
    elif tfc == PokemonROMInfo.TCformat.ListFormatGen3:
        NewTypeChartData = ToListFormatGen3(TypeChart)
    elif tfc == PokemonROMInfo.TCformat.MatrixUQ_4_12Gen6:
        NewTypeChartData = ToMatrixUQ_4_12Gen6(TypeChart) #Calc Chart data for EX ROM Format
        InverseData = ToMatrixUQ_4_12Gen6(InverseTypeChart(TypeChart)) #Calc Inverse Chart data for EX ROM Format
        NewTypeChartData.extend(InverseData) #We need to add the inverse chart data imeadiatly afterwards
    else:
        print('Error unkown TCformat')

    HexEdit(inputfile,outputfile,NewTypeChartData,RomInfo,seed)



def HexEdit(inputfile,outputfile,NewTypeChartData,RomInfo,seed):

    #first make a copy of the input file so we can edit it without destroying the original file
    copy(inputfile,outputfile)
    f = open(outputfile, "r+b")
    # memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(),0)
    # write in any extra non-random data we need into the ROM
    for datapoint in RomInfo.newdata:
        offset = datapoint[0]
        data = datapoint[1]
        mm.seek(offset)
        mm.write(data)
    # write in the new type chart data at the ofset we want for this ROM
    mm.seek(RomInfo.chartdataoffset)
    mm.write(NewTypeChartData)
    mm.flush()

    #Don't forget to close the file when you are done!
    mm.close()
