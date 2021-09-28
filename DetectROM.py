import mmap
    #mmap is used to memory-map the rom files to help handel editing

def TestROM(inputfile):

    f = open(inputfile,"r+b")

    # memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(),0)
    #first try to detect if it's a known gbc file, else detect if it's a known gba file
    GBCTest = TestGBC(mm,inputfile)
    if GBCTest[1]==0:
        return TestGBA(mm)
    return GBCTest

def TestGBC(mm,filename):

    #the location of the TypeMatchup function in the ROM
    TypeMatchupOffsetVanilla = 0x034740
    #the location of the TypeChart itself in the ROM
    TypeChartOffsetVanilla = 0x034BB1
    # The asm code related to the typemachup function as is in ROM
    TypeMatchupHexVanilla = bytearray.fromhex('21 B1 4B 2A FE FF 28 6F FE FE 20 0B 3E 05 CD E1 39 CB 5F 20 62 18 EC B8 20 59 7E BA 28 05 BB 28 02 18 50 E5 C5 23 FA 65 C6 E6 80 47 7E A7 20 05 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD 19 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD 24 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 E1 23 23 18 8C CD C8 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD E1 39 57 46 23 4E 3E 0A EA 65 D2 21 B1 4B 2A FE FF 28 43 FE FE 20 0B 3E 05 CD E1 39 CB 5F 20 36 18 EC BA 20 09 2A B8 28 09 B9 28 06 18 01 23 23 18 DC AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD 19 31 3E 0A E0 B7 C5 06 04 CD 24 31 C1 F0 B6 EA 65 D2 18 B8 C1 D1 E1 C9')
    TypeChartHex = bytearray.fromhex('00 05 05 00 09 05 14 14 05 14 15 05 14 16 14 14 19 14 14 07 14 14 05 05 14 1A 05 14 09 14 15 14 14 15 15 05 15 16 05 15 04 14 15 05 14 15 1A 05 17 15 14 17 17 05 17 16 05 17 04 00 17 02 14 17 1A 05 16 14 05 16 15 14 16 16 05 16 03 05 16 04 14 16 02 05 16 07 05 16 05 14 16 1A 05 16 09 05 19 15 05 19 16 14 19 19 05 19 04 14 19 02 14 19 1A 14 19 09 05 19 14 05 01 00 14 01 19 14 01 03 05 01 02 05 01 18 05 01 07 05 01 05 14 01 1B 14 01 09 14 03 16 14 03 03 05 03 04 05 03 05 05 03 08 05 03 09 00 04 14 14 04 17 14 04 16 05 04 03 14 04 02 00 04 07 05 04 05 14 04 09 14 02 17 05 02 16 14 02 01 14 02 07 14 02 05 05 02 09 05 18 01 14 18 03 14 18 18 05 18 1B 00 18 09 05 07 14 05 07 16 14 07 01 05 07 03 05 07 02 05 07 18 14 07 08 05 07 1B 14 07 09 05 05 14 14 05 19 14 05 01 05 05 04 05 05 02 14 05 07 14 05 09 05 08 00 00 08 18 14 08 1B 05 08 09 05 08 08 14 1A 1A 14 1A 09 05 1B 01 05 1B 18 14 1B 08 14 1B 1B 05 1B 09 05 09 14 05 09 15 05 09 17 05 09 19 14 09 05 14 09 09 05 FE 00 08 00 01 08 00 FF')
    TypeMatchupOffsetSpeedChoice = 0x03474D
    TypeChartOffsetSpeedChoice = 0x34BBE
    TypeMatchupHexSpeedChoice = bytearray.fromhex('21 BE 4B 2A FE FF 28 6F FE FE 20 0B 3E 05 CD C0 39 CB 5F 20 62 18 EC B8 20 59 7E BA 28 05 BB 28 02 18 50 E5 C5 23 FA 65 C6 E6 80 47 7E A7 20 05 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD CA 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD D5 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 E1 23 23 18 8C CD D5 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD C0 39 57 46 23 4E 3E 0A EA 65 D2 21 BE 4B 2A FE FF 28 43 FE FE 20 0B 3E 05 CD C0 39 CB 5F 20 36 18 EC BA 20 09 2A B8 28 09 B9 28 06 18 01 23 23 18 DC AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD CA 31 3E 0A E0 B7 C5 06 04 CD D5 31 C1 F0 B6 EA 65 D2 18 B8 C1 D1 E1 C9')

    mm.seek(TypeMatchupOffsetVanilla)
    test1 = (mm.read(len(TypeMatchupHexVanilla))==TypeMatchupHexVanilla)
    mm.seek(TypeChartOffsetVanilla)
    test2 = (mm.read(len(TypeChartHex))==TypeChartHex)
    if (test1 and test2):
        return ['Crystal Detected!',1]

    mm.seek(TypeMatchupOffsetSpeedChoice)
    test1 = (mm.read(len(TypeMatchupHexSpeedChoice))==TypeMatchupHexSpeedChoice)
    mm.seek(TypeChartOffsetSpeedChoice)
    test2 = (mm.read(len(TypeChartHex))==TypeChartHex)

    if (test1 and test2):
        return ['CrystalSpeedChoice Detected!',2]

    return ['Error.',0]

def TestGBA(mm):
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

    #First Verfy the pointers are in the locations we expect.
    for offset in TypeChartPointers:
        mm.seek(offset)
        if list(mm.read(4))!=OldTypeChart:
            return ['Error Couldn\'t detect ROM',0]

    #Test if the free ROM is free... (in case of some ROM hack or smthing)
    mm.seek(0xAF0000)
    if mm.read(873)!=bytearray(873): #873 bytes is the largest our typechart can get with 17 types...
        return ['Error Free ROM is not free???',0] #this *could* happen if someone is trying to use this on a ROM hack
    return ['EmeraldSpeedChoice Detected!',3]
