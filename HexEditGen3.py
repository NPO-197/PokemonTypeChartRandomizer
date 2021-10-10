import mmap, shutil
    #mmap is used to memory-map the .gbc file to help handel editing
    #shutil is used to copy files
import GeneralLatinSquare as GL
    #GeneralLatinSquare is used to generate the random typechart
import SpoilerLog
    #SpoilerLog is used to generate the spoiler log.


    #Converts a Type Chart from a grid format to a list, for gen 3 type order.
def TypeChartToList(TypeChart):
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
    return(TypeChartList)

#Used to generate a ROM with a random type chart based on the settings
def Rando(ROMType,inputfile,outputfile,mins,maxs,seed):
    # constraint matrix based on given mins and maxs
    cm = [[0,1,2,3],mins,maxs]
    # we generate a random type chart as a general latin square (so it's balanced)
    TypeChart = GL.RandGls(cm,17) #Only 17 types in gen 3
    SaveChart(inputfile,outputfile,TypeChart,seed)

#Used to generate a ROM with a custom type chart for gen 3 ROMS
def SaveChart(ROMType,inputfile,outputfile,TypeChart,seed):
    TypeChartList = TypeChartToList(TypeChart)
    HexEdit(inputfile,outputfile,TypeChartList)
    SpoilerLog.Spoiler(3,outputfile[:-4]+'log.csv',TypeChart,seed)


def HexEdit(inputfile,outputfile,NewTypeChartList):
        #first make a copy of the input file so we can edit it without destroying the original file
        shutil.copy(inputfile,outputfile)

        f = open(outputfile, "r+b")

        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(),0)
        #There are 10 pointers used by various functions that point to the Old Type Chart
        TypeChartPointers =[0x0472F0,   #TypeCalc Pointer 1
                            0x047430,   #TypeCalc Pointer 2
                            0x047504,   #AI trainer switch out
                            0x047868,   #Used in levetate/wonderguard? 1
                            0x04796C,   #Used in levetate/wonderguard? 2
                            0x047A6C,   #"Good" trainer AI
                            0x04CB2C,   #??? (Something in battle_script_command)
                            0x0531D8,   #Used in conversion 2
                            0x063F7C,   #AI trainer switch in?
                            0x191498]   #Battle Dome
        OldTypeChart = [0x70,0xF4,0x31,0x08] #Pointers are stored in reverse order
        CutsomChart = [0x00,0x00,0xAF,0x08] #Pointer to an unused section of ROM

        #First lets update the pointers
        for offset in TypeChartPointers:
            mm.seek(offset)
            mm.write(bytearray(CutsomChart))
        #Now lets write in the new typechart
        mm.seek(0xAF0000)
        mm.write(bytearray(NewTypeChartList))

        #Don't forget to close the file when you are done!
        mm.close()
        return
