import mmap, shutil
    #mmap is used to memory-map the .gbc file to help handel editing
    #shutil is used to copy files
import GeneralLatinSquare as GL
    #GeneralLatinSquare is used to generate the random typechart
import SpoilerLog as Sl
    #SpoilerLog is used to generate tje spoiler log.

    #Used to generate a ROM with a custom type chart
def SaveChart(inputfile,outputfile,TypeChart,seed):
    mins =[]
    maxs = []
    matchups = ['0A','14','05','00']
    RandomTypeChartMatrix = []
    for i in range(len(TypeChart)):
        RandomTypeChartMatrix.append([])
        for j in range(len(TypeChart[0])):
            RandomTypeChartMatrix[i].append(matchups[TypeChart[i][j]])
    HexEdit(inputfile,outputfile,mins,maxs,RandomTypeChartMatrix,seed)

    #Used to generate a ROM with a random type chart based on the settings
    #could probably re-write this whole .py file to be a bit more streamlined....
def Rando(inputfile,outputfile,mins,maxs,seed):
    RandomTypeChartMatrix = []
    HexEdit(inputfile,outputfile,mins,maxs,RandomTypeChartMatrix,seed)


def HexEdit(inputfile,outputfile,mins,maxs,RandomTypeChartMatrix,seed):

    #first make a copy of the input file so we can edit it without destroying the original file
    shutil.copy(inputfile,outputfile)

    f = open(outputfile, "r+b")

    # memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(),0)
    #the location of the TypeMatchup function in the ROM
    TypeMatchupOffsetVanilla = 214848
    #the location of the TypeChart itself in the ROM
    TypeChartOffsetVanilla = 215985
    # The asm code related to the typemachup function as is in ROM
    TypeMatchupHexVanilla = bytearray.fromhex('21 B1 4B 2A FE FF 28 6F FE FE 20 0B 3E 05 CD E1 39 CB 5F 20 62 18 EC B8 20 59 7E BA 28 05 BB 28 02 18 50 E5 C5 23 FA 65 C6 E6 80 47 7E A7 20 05 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD 19 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD 24 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 E1 23 23 18 8C CD C8 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD E1 39 57 46 23 4E 3E 0A EA 65 D2 21 B1 4B 2A FE FF 28 43 FE FE 20 0B 3E 05 CD E1 39 CB 5F 20 36 18 EC BA 20 09 2A B8 28 09 B9 28 06 18 01 23 23 18 DC AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD 19 31 3E 0A E0 B7 C5 06 04 CD 24 31 C1 F0 B6 EA 65 D2 18 B8 C1 D1 E1 C9')
    # The data corispoding to the type chart itself as it appears in the ROM
    TypeChartHex = bytearray.fromhex('00 05 05 00 09 05 14 14 05 14 15 05 14 16 14 14 19 14 14 07 14 14 05 05 14 1A 05 14 09 14 15 14 14 15 15 05 15 16 05 15 04 14 15 05 14 15 1A 05 17 15 14 17 17 05 17 16 05 17 04 00 17 02 14 17 1A 05 16 14 05 16 15 14 16 16 05 16 03 05 16 04 14 16 02 05 16 07 05 16 05 14 16 1A 05 16 09 05 19 15 05 19 16 14 19 19 05 19 04 14 19 02 14 19 1A 14 19 09 05 19 14 05 01 00 14 01 19 14 01 03 05 01 02 05 01 18 05 01 07 05 01 05 14 01 1B 14 01 09 14 03 16 14 03 03 05 03 04 05 03 05 05 03 08 05 03 09 00 04 14 14 04 17 14 04 16 05 04 03 14 04 02 00 04 07 05 04 05 14 04 09 14 02 17 05 02 16 14 02 01 14 02 07 14 02 05 05 02 09 05 18 01 14 18 03 14 18 18 05 18 1B 00 18 09 05 07 14 05 07 16 14 07 01 05 07 03 05 07 02 05 07 18 14 07 08 05 07 1B 14 07 09 05 05 14 14 05 19 14 05 01 05 05 04 05 05 02 14 05 07 14 05 09 05 08 00 00 08 18 14 08 1B 05 08 09 05 08 08 14 1A 1A 14 1A 09 05 1B 01 05 1B 18 14 1B 08 14 1B 1B 05 1B 09 05 09 14 05 09 15 05 09 17 05 09 19 14 09 05 14 09 09 05 FE 00 08 00 01 08 00 FF')
    #The new asm code to replace the original typematchup function
    NewTypeMatchupHexVanilla = bytearray.fromhex('7B 58 47 4A CD DA 4C CD 57 47 78 B9 28 63 41 CD DA 4C CD 57 47 18 5A C5 FA 65 C6 E6 80 47 7E A7 20 11 3E 05 CD E1 39 CB 5F 3E 0A 20 06 AF 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD 19 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD 24 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 C9 CD C8 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 00 00 00 00 00 00 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD E1 39 5F 46 23 4E 3E 0A EA 65 D2 CD DA 4C CD 0D 48 78 B9 28 07 41 CD DA 4C CD 0D 48 FA 65 D2 A7 20 0E 3E 05 CD E1 39 CB 5F 28 05 3E 0A EA 65 D2 C1 D1 E1 C9 AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD 19 31 3E 0A E0 B7 C5 06 04 CD 24 31 C1 F0 B6 EA 65 D2 C9 00 00 00')
    #Extra asm code to be placed after the new type matchup chart (new format takes up less space but requires more asm code to fit)
    TypeChartCodeVanilla = bytearray.fromhex('FE 07 D8 3D BA D8 92 C9 D5 C5 16 0A 7B CD D2 4C 5F 78 CD D2 4C 47 16 00 62 6B 29 29 29 29 19 58 19 11 B1 4B 19 C1 D1 C9 00 00 00')

    #same as before but now specific to the speedchoice ROM
    TypeMatchupOffsetSpeedChoice = 214861
    TypeChartOffsetSpeedChoice = 215998
    TypeMatchupHexSpeedChoice = bytearray.fromhex('21 BE 4B 2A FE FF 28 6F FE FE 20 0B 3E 05 CD C0 39 CB 5F 20 62 18 EC B8 20 59 7E BA 28 05 BB 28 02 18 50 E5 C5 23 FA 65 C6 E6 80 47 7E A7 20 05 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD CA 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD D5 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 E1 23 23 18 8C CD D5 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD C0 39 57 46 23 4E 3E 0A EA 65 D2 21 BE 4B 2A FE FF 28 43 FE FE 20 0B 3E 05 CD C0 39 CB 5F 20 36 18 EC BA 20 09 2A B8 28 09 B9 28 06 18 01 23 23 18 DC AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD CA 31 3E 0A E0 B7 C5 06 04 CD D5 31 C1 F0 B6 EA 65 D2 18 B8 C1 D1 E1 C9')

    NewTypeMatchupHexSpeedChoice = bytearray.fromhex('7B 58 47 4A CD E7 4C CD 64 47 78 B9 28 63 41 CD E7 4C CD 64 47 18 5A C5 FA 65 C6 E6 80 47 7E A7 20 11 3E 05 CD C0 39 CB 5F 3E 0A 20 06 AF 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD CA 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD D5 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 C9 CD D5 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 00 00 00 00 00 00 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD C0 39 5F 46 23 4E 3E 0A EA 65 D2 CD E7 4C CD 1A 48 78 B9 28 07 41 CD E7 4C CD 1A 48 FA 65 D2 A7 20 0E 3E 05 CD C0 39 CB 5F 28 05 3E 0A EA 65 D2 C1 D1 E1 C9 AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD CA 31 3E 0A E0 B7 C5 06 04 CD D5 31 C1 F0 B6 EA 65 D2 C9 00 00 00')

    TypeChartCodeSpeedChoice = bytearray.fromhex('FE 07 D8 3D BA D8 92 C9 D5 C5 16 0A 7B CD DF 4C 5F 78 CD DF 4C 47 16 00 62 6B 29 29 29 29 19 58 19 11 BE 4B 19 C1 D1 C9 00 00 00')

    # 17 types in pokemon crystal
    n = 17
    if mins != []:
        # constraint matrix based on given mins and maxs
        cm = [['0A','14','05','00'],mins,maxs]
        # we generate a random type chart as a general latin square (so it's balanced)
        RandomTypeChartMatrix = GL.RandGls(cm,n)
    RandomTypeChart = GL._to_text(RandomTypeChartMatrix)

    NewTypeChartHex = bytearray.fromhex(RandomTypeChart)

    Sl.Spoiler(outputfile[:-4]+'log.txt',RandomTypeChartMatrix,seed)

    # First seek to the location of the 'typematchup function' used by the game's code
    mm.seek(TypeMatchupOffsetVanilla)
    # Test to see if the asm code exist exactly in the location we expect it to in the ROM
    test1 = (mm.read(len(TypeMatchupHexVanilla))==TypeMatchupHexVanilla)
    # Do the same for the TypeChart
    mm.seek(TypeChartOffsetVanilla)
    test2 = (mm.read(len(TypeChartHex))==TypeChartHex)
    if not(test1 and test2):
        #print('not vanilla')
        mm.seek(TypeMatchupOffsetSpeedChoice)
        test1 = (mm.read(len(TypeMatchupHexSpeedChoice))==TypeMatchupHexSpeedChoice)
        mm.seek(TypeChartOffsetSpeedChoice)
        test2 = (mm.read(len(TypeChartHex))==TypeChartHex)
        if not(test1 and test2):
            print(test1)
            print(test2)
            print('Error Couldn\'t detect ROM')
            #will need to move error handling to when we LOAD the file instead of when we try to randomize it
        else:
            #will need to write a full function for this to make supporting other ROMS more simpler
            print('SpeedChoice ROM detected')
            mm.seek(TypeMatchupOffsetSpeedChoice)
            mm.write(NewTypeMatchupHexSpeedChoice)
            mm.seek(TypeChartOffsetSpeedChoice)
            mm.write(NewTypeChartHex)
            mm.write(TypeChartCodeSpeedChoice)
            mm.flush()
    else:
        #same function as for speed choice just slightly different offsets and hexcode
        print('Vanilla ROM detected')
        mm.seek(TypeMatchupOffsetVanilla)
        mm.write(NewTypeMatchupHexVanilla)
        mm.seek(TypeChartOffsetVanilla)
        mm.write(NewTypeChartHex)
        mm.write(TypeChartCodeVanilla)
        mm.flush()

    #Don't forget to close the file when you are done!
    mm.close()
