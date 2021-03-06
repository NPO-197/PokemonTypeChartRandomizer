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
    # Includes a 3 byte "forsight break" that seperates matchups that forsight ignores
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
    NewTypeChartData = MatrixUQ_4_12Gen6(TypeChart) #Calc Chart data for EX ROM Format
    InverseData = MatrixUQ_4_12Gen6(InverseTypeChart(TypeChart)) #Calc Inverse Chart data for EX ROM Format
    NewTypeChartData.extend(InverseData) #We need to add the inverse chart data imeadiatly afterwards
    return NewTypeChartData

def MatrixUQ_4_12Gen6(TypeChart):
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

def ToListFormatGen1(TypeChart):
    # List Format, Attacking,Defending,Matchup list of every non-neutral matchup
    #Gen 1 types, only 15 of them, no need to "sort" the list
    matchups = [0x0A,0x14,0x05,0x00]
    #Convert from type chart index to gen 1 index "BIRD type lol"
    Gen1Index = [0x00,0x01,0x02,0x03,0x04,0x05,0x07,0x08,0x14,0x15,0x16,0x17,0x18,0x19,0x1A]
    TypeChartList = []
    for i in range(len(TypeChart)):
        for j in range(len(TypeChart[0])):
            AtkType = Gen1Index[i]
            DefType = Gen1Index[j]
            Matchup = matchups[TypeChart[i][j]]
            #Ignore neutral matchups
            if Matchup == 0x0A:
                continue
            #Put non-neutral matchups into the list
            TypeChartList.extend([AtkType,DefType,Matchup])
    #Add 0xFF to the end of the list
    TypeChartList.append(0xFF)
    return bytearray(TypeChartList)

def ToListFormatGen2(TypeChart):
    # List Format, Attacking,Defending,Matchup list of every non-neutral matchup
    # Includes a 1 byte "forsight break" that seperates matchups that forsight ignores
    # This seems to be the general method for storing the type chart in all offical games
    matchups = [0x0A,0x14,0x05,0x00]
    #Convert from type chart index to gen 1 index "BIRD type lol"
    Gen2Index = [0x00,0x01,0x02,0x03,0x04,0x05,0x07,0x08,0x09,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B]
    TypeChartList = []
    Imunities = []
    for i in range(len(TypeChart)):
        for j in range(len(TypeChart[0])):
            AtkType = Gen2Index[i]
            DefType = Gen2Index[j]
            Matchup = matchups[TypeChart[i][j]]
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

    TypeChartList.extend([0xFE])#Foresight break point
    TypeChartList.extend(Imunities)
    TypeChartList.extend([0xFF])#End of matchups list
    return bytearray(TypeChartList)



def Rando(inputfile,outputfile,mins,maxs,RomInfo,seed):

    n = RomInfo.NumberOfTypes
    cm = [[0,1,2,3],mins,maxs]
    TypeChart = GeneralLatinSquare.RandGls(cm,n)

    SaveChart(inputfile,outputfile,TypeChart,RomInfo,seed)

#Used to generate a ROM with a given type chart
def SaveChart(inputfile,outputfile,TypeChart,RomInfo,seed):
    #Dictonary of defined format functions
    FormatFunctions = {
    PokemonROMInfo.TCformat.MatrixFormatGen2:ToMatrixFormatGen2,
    PokemonROMInfo.TCformat.ListFormatGen3:ToListFormatGen3,
    PokemonROMInfo.TCformat.MatrixUQ_4_12Gen6:ToMatrixUQ_4_12Gen6,
    PokemonROMInfo.TCformat.ListFormatGen1:ToListFormatGen1,
    PokemonROMInfo.TCformat.ListFormatGen2:ToListFormatGen2
    }
    #Generate the SpoilerLog
    SpoilerLog.Spoiler(outputfile[:-4]+'log.csv',TypeChart,seed,RomInfo.NumberOfTypes)
    #Generate the typechart data in the format expected by the ROM
    NewTypeChartData = FormatFunctions.get(RomInfo.typechartformat,None)(TypeChart)
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

def OptionalEdits(outputfile,Data):
    f = open(outputfile,"r+b")
    mm = mmap.mmap(f.fileno(),0)
    # write in any optional data we need into the ROM
    for datapoint in Data:
        offset = datapoint[0]
        data = datapoint[1]
        mm.seek(offset)
        mm.write(data)
    mm.flush()
    mm.close()
