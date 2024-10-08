"""
ROM information file made by NPO-197
This file contains all rom sepecific info for each pokemon game needed to detect and randomize each rom
File size, offests, ect.
"""
from enum import Enum

class ROMID(Enum):
    Error = 0
    Crystal = 1
    CrystalSpeedChoice = 2
    EmeraldSpeedChoice = 3
    EmeraldEXSpeedChoice = 4
    Emerald = 5
    RedBlue = 6
    RedSpeedChoice = 7
    Yellow = 8
    Ruby = 9
    Sapphire = 10
    GoldSilver =11
    FireRed = 12
    LeafGreen = 13

class TCformat(Enum):
    #2D array Effectivenes format, a custom format that Crystal roms are modifyed to accept.
    MatrixFormatGen2 = 1
    #1D array Attack/Defend/Effecivenes, 3byte forsight break
    ListFormatGen3 = 2
    #2D array 2byte Effectivenes, +Inverse Chart  (Emerald EX)
    MatrixUQ_4_12Gen6 = 3
    #1D array Attack/Defend/Effecivenes no forsight break
    ListFormatGen1 = 4
    #1D array Attack/Defend/Effecivenes, 1byte forsight break
    ListFormatGen2 = 5

DefinedRoms = []

class RomInfo:
    def __init__(self,ROMID,filesize,chartdataoffset,typechartformat,checkdata,newdata,NumberOfTypes=17,optionaldata=[]):
        # ROMID is just a way to enumirate all of the different supported rom types
        self.ROMID = ROMID
        # File size of the Rom
        self.filesize = filesize
        # The location we would like to write in the rando type chart data
        self.chartdataoffset = chartdataoffset
        #What format is the type chart going to be s
        self.typechartformat = typechartformat
        # What data we need to check to detect this rom, and where in rom that data is.
        self.checkdata = checkdata
        # The new data we need to write to rom (other then the rando type chart data) and where to write it
        self.newdata = newdata
        # Number of different types in this ROM default is 17 for Generations 2-5
        self.NumberOfTypes = NumberOfTypes
        # Optional Data that we may want to write into memory (currently only used for gen one Dragon breath)
        self.optionaldata = optionaldata
        DefinedRoms.append(self)

NoRomInfo = RomInfo(ROMID.Error,0,0,0,[],[])

RedBlueInfo = RomInfo(ROMID.RedBlue,0x100000,0x03FBE0, TCformat.ListFormatGen1, NumberOfTypes = 15,
    checkdata = [
        #Pointers to the original type chart data
        [0x03E3F8,bytearray.fromhex('74 64')],  #AdjustDamageForMoveType
        [0x03E459,bytearray.fromhex('74 64')],  #AIGetTypeEffectiveness
        #Dual-type damage misinformation glitch
        [0x03E411, bytearray.fromhex('E680')],      # and a,0x80
        [0x03E417, bytearray.fromhex('80EA5BD0')],  # add b;ld (wDamageMultipliers),a
        [0x03FBC8,bytearray(700)] #We need space for both the patch and new typechart
    ],
    newdata =[
        #Pointers to the original type chart data
        #We want to change them to point to the new type chart at 0F:7BE0
        [0x03E3F8,bytearray.fromhex('E0 7B')],   #AdjustDamageForMoveType
        [0x03E459,bytearray.fromhex('E0 7B')],   #AIGetTypeEffectiveness
        #Fix the Dual-type damage misinformation glitch
        [0x03E411, bytearray.fromhex('E67F')],      # and a,0x7F
        [0x03E417, bytearray.fromhex('00CDC87B')],   #nop:call 7BC8 (our patch)
        #Asm code patch
        [0x03FBC8, bytearray.fromhex('4F78A720014F79B0FE1520020E0A79EA5BD0C9')]

    ],
    optionaldata =[
        [0x381e6,bytearray.fromhex("52243C1AFF14")], #Change DragonRage into a 60bp,20pp, Dragon move w/ 30% chance of para
        [0xB02F6,bytearray.fromhex("8391868D7F81918480938750")] #Change the name of "DRAGON RAGE" to "DRGN BREATH" (13 char limit, also i'm lazy)
    ]
)

YellowInfo = RomInfo(ROMID.Yellow,0x100000,0x03FBE0, TCformat.ListFormatGen1, NumberOfTypes = 15,
#Note yellow offsets are a bit different then red/blue
    checkdata = [
        #Pointers to the original type chart data
        [0x03E56A,bytearray.fromhex('FA 65')],  #AdjustDamageForMoveType
        [0x03E5CB,bytearray.fromhex('FA 65')],  #AIGetTypeEffectiveness
        #Dual-type damage misinformation glitch
        [0x03E583, bytearray.fromhex('E680')],      # and a,0x80
        [0x03E589, bytearray.fromhex('80EA5AD0')],  # add b;ld (wDamageMultipliers),a
        [0x03FBC8,bytearray(700)] #We need space for both the patch and new typechart
    ],
    newdata = [
        #Pointers to the original type chart data
        #We want to change them to point to the new type chart at 0F:7BE0
        [0x03E56A,bytearray.fromhex('E0 7B')],   #AdjustDamageForMoveType
        [0x03E5CB,bytearray.fromhex('E0 7B')],   #AIGetTypeEffectiveness
        #Fix the Dual-type damage misinformation glitch
        [0x03E583, bytearray.fromhex('E67F')],      # and a,0x7F
        [0x03E589, bytearray.fromhex('00CDC87B')],   #nop:call 7BC8 (our patch)
        #Asm code patch
        [0x03FBC8, bytearray.fromhex('4F78A720014F79B0FE1520020E0A79EA5AD0C9')]
    ],
    optionaldata =[
        [0x381E6,bytearray.fromhex("52243C1AFF14")], #Change DragonRage into a 60bp,20pp, Dragon move w/ 30% chance of para
        [0xBC2F6,bytearray.fromhex("8391868D7F81918480938750")] #Change the name of "DRAGON RAGE" to "DRGN BREATH" (13 char limit, also i'm lazy)
    ]

)

GoldSilverInfo = RomInfo(ROMID.GoldSilver,0x200000,0x1C4000,TCformat.ListFormatGen2,
    checkdata=[
        #Is rst18 unused?
        [0x0018,bytearray.fromhex("FF 00 00 00 00 00 00 00")],
        #Is rst20 unused?
        [0x0020,bytearray.fromhex("FF 00 00 00 00 00 00 00")],

        #Type Matchups Pointer BattleCommandSTAB
        [0x34890,bytearray.fromhex("21 01 4D")], #ld hl,4D01
        #.TypesLoop: load AttackingType
        [0x34893,bytearray.fromhex("2A")], #ldi a,[hl]
        #.SkipForesightCheck load DefendingType
        [0x348AA,bytearray.fromhex("7E")], #ld a,[hl]
        #.GotMatchup load Effecivenes
        [0x348BC,bytearray.fromhex("7E")], #ld a,[hl]

        #Type Matchups Pointer CheckTypesMatchup (used by AI)
        [0x34934,bytearray.fromhex("21 01 4D")], #ld hl,4D01
        #.TypesLoop: load AttackingType
        [0x34937,bytearray.fromhex("2A")], #ldi a,[hl]
        #.Next load DefendingType
        [0x3494E,bytearray.fromhex("2A")], #ldi a,[hl]
        #.Yup load Effecivenes
        [0x34962,bytearray.fromhex("2A")], #ldi a,[hl]

        #Unused Section of ROM
        [0x1c4000,bytearray(869)] #Maximum length of typechart data is 3*17^2+2 = 869
    ],
    newdata =[
    #ld a 71;Call GetFarByte; inc hl;ret
    [0x0018,bytearray.fromhex("3E 71 CD 28 31 23 C9 00")],
    #ld a 71;jp GetFarByte
    [0x0020,bytearray.fromhex("3E 71 C3 28 31 00 00 00")],

    #Type Matchups Pointer BattleCommandSTAB
    [0x34890,bytearray.fromhex("21 00 40")], #ld hl,4000
    #.TypesLoop: load AttackingType
    [0x34893,bytearray.fromhex("DF")], #RST 18h
    #.SkipForesightCheck load DefendingType
    [0x348AA,bytearray.fromhex("E7")], #RST 20h
    #.GotMatchup load Effecivenes
    [0x348BC,bytearray.fromhex("E7")], #RST 20h

    #Type Matchups Pointer CheckTypesMatchup (used by AI)
    [0x34934,bytearray.fromhex("21 00 40")], #ld hl,4000
    #.TypesLoop: load AttackingType
    [0x34937,bytearray.fromhex("DF")], #RST 18h
    #.Next load DefendingType
    [0x3494E,bytearray.fromhex("DF")], #RST 18h
    #.Yup load Effecivenes
    [0x34962,bytearray.fromhex("DF")] #RST 18h
    ]
)

CrystalInfo = RomInfo(ROMID.Crystal,0x200000,0x034BB1,TCformat.MatrixFormatGen2,
    checkdata =[
        #TypeMatchup function
        [0x034740,bytearray.fromhex('21 B1 4B 2A FE FF 28 6F FE FE 20 0B 3E 05 CD E1 39 CB 5F 20 62 18 EC B8 20 59 7E BA 28 05 BB 28 02 18 50 E5 C5 23 FA 65 C6 E6 80 47 7E A7 20 05 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD 19 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD 24 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 E1 23 23 18 8C CD C8 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD E1 39 57 46 23 4E 3E 0A EA 65 D2 21 B1 4B 2A FE FF 28 43 FE FE 20 0B 3E 05 CD E1 39 CB 5F 20 36 18 EC BA 20 09 2A B8 28 09 B9 28 06 18 01 23 23 18 DC AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD 19 31 3E 0A E0 B7 C5 06 04 CD 24 31 C1 F0 B6 EA 65 D2 18 B8 C1 D1 E1 C9')],
        #TypeChart itself
        [0x034BB1,bytearray.fromhex('00 05 05 00 09 05 14 14 05 14 15 05 14 16 14 14 19 14 14 07 14 14 05 05 14 1A 05 14 09 14 15 14 14 15 15 05 15 16 05 15 04 14 15 05 14 15 1A 05 17 15 14 17 17 05 17 16 05 17 04 00 17 02 14 17 1A 05 16 14 05 16 15 14 16 16 05 16 03 05 16 04 14 16 02 05 16 07 05 16 05 14 16 1A 05 16 09 05 19 15 05 19 16 14 19 19 05 19 04 14 19 02 14 19 1A 14 19 09 05 19 14 05 01 00 14 01 19 14 01 03 05 01 02 05 01 18 05 01 07 05 01 05 14 01 1B 14 01 09 14 03 16 14 03 03 05 03 04 05 03 05 05 03 08 05 03 09 00 04 14 14 04 17 14 04 16 05 04 03 14 04 02 00 04 07 05 04 05 14 04 09 14 02 17 05 02 16 14 02 01 14 02 07 14 02 05 05 02 09 05 18 01 14 18 03 14 18 18 05 18 1B 00 18 09 05 07 14 05 07 16 14 07 01 05 07 03 05 07 02 05 07 18 14 07 08 05 07 1B 14 07 09 05 05 14 14 05 19 14 05 01 05 05 04 05 05 02 14 05 07 14 05 09 05 08 00 00 08 18 14 08 1B 05 08 09 05 08 08 14 1A 1A 14 1A 09 05 1B 01 05 1B 18 14 1B 08 14 1B 1B 05 1B 09 05 09 14 05 09 15 05 09 17 05 09 19 14 09 05 14 09 09 05 FE 00 08 00 01 08 00 FF')]
        ],
    newdata = [
        #The new asm code to replace the original typematchup function
        [0x034740,bytearray.fromhex('7B 58 47 4A CD DA 4C CD 57 47 78 B9 28 63 41 CD DA 4C CD 57 47 18 5A C5 FA 65 C6 E6 80 47 7E A7 20 11 3E 05 CD E1 39 CB 5F 3E 0A 20 06 AF 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD 19 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD 24 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 C9 CD C8 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 00 00 00 00 00 00 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD E1 39 5F 46 23 4E 3E 0A EA 65 D2 CD DA 4C CD 0D 48 78 B9 28 07 41 CD DA 4C CD 0D 48 FA 65 D2 A7 20 0E 3E 05 CD E1 39 CB 5F 28 05 3E 0A EA 65 D2 C1 D1 E1 C9 AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD 19 31 3E 0A E0 B7 C5 06 04 CD 24 31 C1 F0 B6 EA 65 D2 C9 00 00 00')],
        #Extra asm code to be placed after the new type matchup chart (new format takes up less space but requires more asm code to fit)
        [0x034CD2,bytearray.fromhex('FE 07 D8 3D BA D8 92 C9 D5 C5 16 0A 7B CD D2 4C 5F 78 CD D2 4C 47 16 00 62 6B 29 29 29 29 19 58 19 11 B1 4B 19 C1 D1 C9 00 00 00')]
        ]
)

RubyInfo = RomInfo(ROMID.Ruby,0x1000000,0xAF0000,TCformat.ListFormatGen3,
    checkdata = [
    #Pointers to the original type chart data
        [0x01CDC8,bytearray.fromhex('20 97 1F 08')],   #TypeCalc Pointer 1
        [0x01CF08,bytearray.fromhex('20 97 1F 08')],   #TypeCalc Pointer 2
        [0x01CFE4,bytearray.fromhex('20 97 1F 08')],   #AI trainer switch out
        [0x01D344,bytearray.fromhex('20 97 1F 08')],   #Used in levetate/wonderguard? 1
        [0x01D44C,bytearray.fromhex('20 97 1F 08')],   #Used in levetate/wonderguard? 2
        [0x01D564,bytearray.fromhex('20 97 1F 08')],   #"Good" trainer AI
        [0x02237C,bytearray.fromhex('20 97 1F 08')],   #??? (Something in battle_script_command)
        [0x028120,bytearray.fromhex('20 97 1F 08')],   #Used in conversion 2
        [0x036CD0,bytearray.fromhex('20 97 1F 08')],   #AI trainer switch in?
        #Unused Section of ROM
        [0xAF0000,bytearray([0xFF]*873)] #We need at most 873 ""empty"" bytes
    ],
    newdata =[
    #There are 9 pointers used by various functions that point to the Old Type Chart
    #We want to change them to point to the new type chart at 0x08af0000
        [0x01CDC8,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 1
        [0x01CF08,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 2
        [0x01CFE4,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch out
        [0x01D344,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 1
        [0x01D44C,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 2
        [0x01D564,bytearray.fromhex('00 00 AF 08')],   #"Good" trainer AI
        [0x02237C,bytearray.fromhex('00 00 AF 08')],   #??? (Something in battle_script_command)
        [0x028120,bytearray.fromhex('00 00 AF 08')],   #Used in conversion 2
        [0x036CD0,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch in?
    ]
)

SapphireInfo = RomInfo(ROMID.Sapphire,0x1000000,0xAF0000,TCformat.ListFormatGen3,
checkdata = [
#Same as VanillaRuby but the original type chart is in a slightly different location
#Pointers to the original type chart data
    [0x01CDC8,bytearray.fromhex('B0 96 1F 08')],   #TypeCalc Pointer 1
    [0x01CF08,bytearray.fromhex('B0 96 1F 08')],   #TypeCalc Pointer 2
    [0x01CFE4,bytearray.fromhex('B0 96 1F 08')],   #AI trainer switch out
    [0x01D344,bytearray.fromhex('B0 96 1F 08')],   #Used in levetate/wonderguard? 1
    [0x01D44C,bytearray.fromhex('B0 96 1F 08')],   #Used in levetate/wonderguard? 2
    [0x01D564,bytearray.fromhex('B0 96 1F 08')],   #"Good" trainer AI
    [0x02237C,bytearray.fromhex('B0 96 1F 08')],   #??? (Something in battle_script_command)
    [0x028120,bytearray.fromhex('B0 96 1F 08')],   #Used in conversion 2
    [0x036CD0,bytearray.fromhex('B0 96 1F 08')],   #AI trainer switch in?
    #Unused Section of ROM
    [0xAF0000,bytearray([0xFF]*873)] #We need at most 873 ""empty"" bytes
],
newdata =[
#There are 9 pointers used by various functions that point to the Old Type Chart
#We want to change them to point to the new type chart at 0x08af0000
    [0x01CDC8,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 1
    [0x01CF08,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 2
    [0x01CFE4,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch out
    [0x01D344,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 1
    [0x01D44C,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 2
    [0x01D564,bytearray.fromhex('00 00 AF 08')],   #"Good" trainer AI
    [0x02237C,bytearray.fromhex('00 00 AF 08')],   #??? (Something in battle_script_command)
    [0x028120,bytearray.fromhex('00 00 AF 08')],   #Used in conversion 2
    [0x036CD0,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch in?
]
)

FireRedInfo = RomInfo(ROMID.FireRed,0x1000000,0xAF0000,TCformat.ListFormatGen3,
checkdata =[
#Similar to Ruby/Sapphire but the offsets are different
#Pointers to the original type chart data
    [0x01E958,bytearray.fromhex('C0 F0 24 08')], #TypeCalc Pointer 1
    [0x01EA98,bytearray.fromhex('C0 F0 24 08')], #TypeCalc Pointer 2
    [0x01EB6C,bytearray.fromhex('C0 F0 24 08')], #AI trainer switch out
    [0x01EED0,bytearray.fromhex('C0 F0 24 08')], #Used in levetate/wonderguard? 1
    [0x01EFD4,bytearray.fromhex('C0 F0 24 08')], #Used in levetate/wonderguard? 2
    [0x01F0D4,bytearray.fromhex('C0 F0 24 08')], #"Good" trainer AI
    [0x023CEC,bytearray.fromhex('C0 F0 24 08')], #??? (Something in battle_script_command)
    [0x029FA4,bytearray.fromhex('C0 F0 24 08')], #Used in conversion 2
    [0x039E4C,bytearray.fromhex('C0 F0 24 08')], #AI trainer switch in?
    #Unused Section of ROM
    [0xAF0000,bytearray([0xFF]*873)] #We need at most 873 ""empty"" bytes
],
newdata = [
    #There are 9 pointers used by various functions that point to the Old Type Chart
    #We want to change them to point to the new type chart at 0x08af0000
    [0x01E958,bytearray.fromhex('00 00 AF 08')], #TypeCalc Pointer 1
    [0x01EA98,bytearray.fromhex('00 00 AF 08')], #TypeCalc Pointer 2
    [0x01EB6C,bytearray.fromhex('00 00 AF 08')], #AI trainer switch out
    [0x01EED0,bytearray.fromhex('00 00 AF 08')], #Used in levetate/wonderguard? 1
    [0x01EFD4,bytearray.fromhex('00 00 AF 08')], #Used in levetate/wonderguard? 2
    [0x01F0D4,bytearray.fromhex('00 00 AF 08')], #"Good" trainer AI
    [0x023CEC,bytearray.fromhex('00 00 AF 08')], #??? (Something in battle_script_command)
    [0x029FA4,bytearray.fromhex('00 00 AF 08')], #Used in conversion 2
    [0x039E4C,bytearray.fromhex('00 00 AF 08')], #AI trainer switch in?
]
)

LeafGreenInfo = RomInfo(ROMID.LeafGreen,0x1000000,0xAF0000,TCformat.ListFormatGen3,
checkdata =[
#Same as FireRed but the original type chart is in a slightly different location
#Pointers to the original type chart data
    [0x01E958,bytearray.fromhex('9C F0 24 08')], #TypeCalc Pointer 1
    [0x01EA98,bytearray.fromhex('9C F0 24 08')], #TypeCalc Pointer 2
    [0x01EB6C,bytearray.fromhex('9C F0 24 08')], #AI trainer switch out
    [0x01EED0,bytearray.fromhex('9C F0 24 08')], #Used in levetate/wonderguard? 1
    [0x01EFD4,bytearray.fromhex('9C F0 24 08')], #Used in levetate/wonderguard? 2
    [0x01F0D4,bytearray.fromhex('9C F0 24 08')], #"Good" trainer AI
    [0x023CEC,bytearray.fromhex('9C F0 24 08')], #??? (Something in battle_script_command)
    [0x029FA4,bytearray.fromhex('9C F0 24 08')], #Used in conversion 2
    [0x039E4C,bytearray.fromhex('9C F0 24 08')], #AI trainer switch in?
    #Unused Section of ROM
    [0xAF0000,bytearray([0xFF]*873)] #We need at most 873 ""empty"" bytes
],
newdata = [
    #There are 9 pointers used by various functions that point to the Old Type Chart
    #We want to change them to point to the new type chart at 0x08af0000
    [0x01E958,bytearray.fromhex('00 00 AF 08')], #TypeCalc Pointer 1
    [0x01EA98,bytearray.fromhex('00 00 AF 08')], #TypeCalc Pointer 2
    [0x01EB6C,bytearray.fromhex('00 00 AF 08')], #AI trainer switch out
    [0x01EED0,bytearray.fromhex('00 00 AF 08')], #Used in levetate/wonderguard? 1
    [0x01EFD4,bytearray.fromhex('00 00 AF 08')], #Used in levetate/wonderguard? 2
    [0x01F0D4,bytearray.fromhex('00 00 AF 08')], #"Good" trainer AI
    [0x023CEC,bytearray.fromhex('00 00 AF 08')], #??? (Something in battle_script_command)
    [0x029FA4,bytearray.fromhex('00 00 AF 08')], #Used in conversion 2
    [0x039E4C,bytearray.fromhex('00 00 AF 08')], #AI trainer switch in?
]
)

EmeraldInfo = RomInfo(ROMID.Emerald,0x1000000,0xAF0000,TCformat.ListFormatGen3,
    checkdata = [
    #Same as Ruby/Sapphire but with different offests and one extra pointer used in the Battle Dome.
    #Pointers to the original type chart data
        [0x047134,bytearray.fromhex('E8 AC 31 08')],   #TypeCalc Pointer 1
        [0x047274,bytearray.fromhex('E8 AC 31 08')],   #TypeCalc Pointer 2
        [0x047348,bytearray.fromhex('E8 AC 31 08')],   #AI trainer switch out
        [0x0476AC,bytearray.fromhex('E8 AC 31 08')],   #Used in levetate/wonderguard? 1
        [0x0477B0,bytearray.fromhex('E8 AC 31 08')],   #Used in levetate/wonderguard? 2
        [0x0478B0,bytearray.fromhex('E8 AC 31 08')],   #"Good" trainer AI
        [0x04C694,bytearray.fromhex('E8 AC 31 08')],   #??? (Something in battle_script_command)
        [0x052D18,bytearray.fromhex('E8 AC 31 08')],   #Used in conversion 2
        [0x063A8C,bytearray.fromhex('E8 AC 31 08')],   #AI trainer switch in?
        [0x1900B8,bytearray.fromhex('E8 AC 31 08')],   #Battle Dome
        #Unused Section of ROM
        [0xAF0000,bytearray(873)] #We need at most 873 empty bytes
    ],
    newdata =[
    #There are 10 pointers used by various functions that point to the Old Type Chart
    #We want to change them to point to the new type chart at 0x08af0000
        [0x047134,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 1
        [0x047274,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 2
        [0x047348,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch out
        [0x0476AC,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 1
        [0x0477B0,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 2
        [0x0478B0,bytearray.fromhex('00 00 AF 08')],   #"Good" trainer AI
        [0x04C694,bytearray.fromhex('00 00 AF 08')],   #??? (Something in battle_script_command)
        [0x052D18,bytearray.fromhex('00 00 AF 08')],   #Used in conversion 2
        [0x063A8C,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch in?
        [0x1900B8,bytearray.fromhex('00 00 AF 08')],   #Battle Dome
    ]
)

#"Speedchoice" ROMs

RedSpeedChoiceInfo = RomInfo(ROMID.RedSpeedChoice,0x100000,0xBA569, TCformat.ListFormatGen1, NumberOfTypes = 15,
    checkdata = [
        #The start of each funtion we need to move
        [0x3e444,bytearray.fromhex("2110D02A474E21")], #AdjustDamageForMoveType
        [0x3e4e8,bytearray.fromhex("21DACFF0F3A7FA")], #StatsGetEffectiveness
        [0x3e53e,bytearray.fromhex("FABFCF572110D0")], #AIGetTypeEffectiveness
        #CopiedFunctionSpace
        [0xb8000,bytearray(339)], #Need space to copy the functions over
        [0xba569,bytearray(676)] #Need space for our new typechart data
    ],
    newdata =[
        #Write a far call to the copied functions new location
        [0x3e444,bytearray.fromhex("062E210040C7C9")], #AdjustDamageForMoveType
        [0x3e4e8,bytearray.fromhex("062E21B040C7C9")], #StatsGetEffectiveness
        [0x3e53e,bytearray.fromhex("062E211041C7C9")], #AIGetTypeEffectiveness
        #CopiedFunctions
        [0xb8000,bytearray.fromhex("2110D02A474E21DACF2A575EFAC5CFEA06D1F0F3A7281221DACF2A474E2110D02A575EFABFCFEA06D1FA06D1B82805B92802181A21C0D03A666F444DCB38CB19097CEABFD07DEAC0D02152D0CBFEFA06D1472169652AFEFF2849B820417EBA2805BB28021838E5C523FA52D0E67F477EE09900CD4041AFE09621BFD02AE0973AE098CDEE343E0AE0990604CDF934F0972247F09877B020043CEA56D0C1E1232318B300C900000000000000000000000021DACFF0F3A7FAC5CF28062110D0FABFCF4F2A5E57060A2169652AFEFF2835B9202E7EBA2805BB280218252378FE0A200346181DAFE096E09778E0982AE099CDEE343E0AE0990604CDF934F0984718CA232318C650C900000000000000000000FABFCF572110D046234E3E10EA06D12169652AFEFFC8BA20092AB82809B928061801232318EC7EEA06D1C900000000004F78A720014F79B0FE1520020E0A79EA52D0C9")]
    ],
    optionaldata =[
        [0x381e6,bytearray.fromhex("52243C1AFF14")], #Change DragonRage into a 60bp,20pp, Dragon move w/ 30% chance of para
        [0xB02F6,bytearray.fromhex("8391868D7F81918480938750")] #Change the name of "DRAGON RAGE" to "DRGN BREATH" (13 char limit, also i'm lazy)
    ]
)

CrystalSpeedChoiceInfo = RomInfo(ROMID.CrystalSpeedChoice,0x200000,0x34BBE,TCformat.MatrixFormatGen2,
checkdata =[
#TypeMatchup function
[0x03474D,bytearray.fromhex('21 BE 4B 2A FE FF 28 6F FE FE 20 0B 3E 05 CD C0 39 CB 5F 20 62 18 EC B8 20 59 7E BA 28 05 BB 28 02 18 50 E5 C5 23 FA 65 C6 E6 80 47 7E A7 20 05 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD CA 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD D5 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 E1 23 23 18 8C CD D5 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD C0 39 57 46 23 4E 3E 0A EA 65 D2 21 BE 4B 2A FE FF 28 43 FE FE 20 0B 3E 05 CD C0 39 CB 5F 20 36 18 EC BA 20 09 2A B8 28 09 B9 28 06 18 01 23 23 18 DC AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD CA 31 3E 0A E0 B7 C5 06 04 CD D5 31 C1 F0 B6 EA 65 D2 18 B8 C1 D1 E1 C9')],
#TypeChart itself
[0x034BBE,bytearray.fromhex('00 05 05 00 09 05 14 14 05 14 15 05 14 16 14 14 19 14 14 07 14 14 05 05 14 1A 05 14 09 14 15 14 14 15 15 05 15 16 05 15 04 14 15 05 14 15 1A 05 17 15 14 17 17 05 17 16 05 17 04 00 17 02 14 17 1A 05 16 14 05 16 15 14 16 16 05 16 03 05 16 04 14 16 02 05 16 07 05 16 05 14 16 1A 05 16 09 05 19 15 05 19 16 14 19 19 05 19 04 14 19 02 14 19 1A 14 19 09 05 19 14 05 01 00 14 01 19 14 01 03 05 01 02 05 01 18 05 01 07 05 01 05 14 01 1B 14 01 09 14 03 16 14 03 03 05 03 04 05 03 05 05 03 08 05 03 09 00 04 14 14 04 17 14 04 16 05 04 03 14 04 02 00 04 07 05 04 05 14 04 09 14 02 17 05 02 16 14 02 01 14 02 07 14 02 05 05 02 09 05 18 01 14 18 03 14 18 18 05 18 1B 00 18 09 05 07 14 05 07 16 14 07 01 05 07 03 05 07 02 05 07 18 14 07 08 05 07 1B 14 07 09 05 05 14 14 05 19 14 05 01 05 05 04 05 05 02 14 05 07 14 05 09 05 08 00 00 08 18 14 08 1B 05 08 09 05 08 08 14 1A 1A 14 1A 09 05 1B 01 05 1B 18 14 1B 08 14 1B 1B 05 1B 09 05 09 14 05 09 15 05 09 17 05 09 19 14 09 05 14 09 09 05 FE 00 08 00 01 08 00 FF')]
],
newdata = [
#The new asm code to replace the original typematchup function
[0x03474D,bytearray.fromhex('7B 58 47 4A CD E7 4C CD 64 47 78 B9 28 63 41 CD E7 4C CD 64 47 18 5A C5 FA 65 C6 E6 80 47 7E A7 20 11 3E 05 CD C0 39 CB 5F 3E 0A 20 06 AF 3C EA 67 C6 AF E0 B7 80 EA 65 C6 AF E0 B4 21 56 D2 2A E0 B5 3A E0 B6 CD CA 31 F0 B4 47 F0 B5 B0 47 F0 B6 B0 28 15 3E 0A E0 B7 06 04 CD D5 31 F0 B5 47 F0 B6 B0 20 04 3E 01 E0 B6 F0 B5 22 F0 B6 77 C1 C9 CD D5 47 FA 65 D2 47 FA 65 C6 E6 80 B0 EA 65 C6 C9 00 00 00 00 00 00 21 24 D2 F0 E4 A7 28 03 21 4A C6 E5 D5 C5 3E 0F CD C0 39 5F 46 23 4E 3E 0A EA 65 D2 CD E7 4C CD 1A 48 78 B9 28 07 41 CD E7 4C CD 1A 48 FA 65 D2 A7 20 0E 3E 05 CD C0 39 CB 5F 28 05 3E 0A EA 65 D2 C1 D1 E1 C9 AF E0 B3 E0 B4 E0 B5 2A E0 B6 FA 65 D2 E0 B7 CD CA 31 3E 0A E0 B7 C5 06 04 CD D5 31 C1 F0 B6 EA 65 D2 C9 00 00 00')],
#Extra asm code to be placed after the new type matchup chart (new format takes up less space but requires more asm code to fit)
[0x034CDF,bytearray.fromhex('FE 07 D8 3D BA D8 92 C9 D5 C5 16 0A 7B CD DF 4C 5F 78 CD DF 4C 47 16 00 62 6B 29 29 29 29 19 58 19 11 BE 4B 19 C1 D1 C9 00 00 00')]
]
)

EmeraldSpeedChoiceInfo = RomInfo(ROMID.EmeraldSpeedChoice,0x1000000,0xAF0000,TCformat.ListFormatGen3,
checkdata = [
#Pointers to the original type chart data
[0x0472F0,bytearray.fromhex('70 F4 31 08')],   #TypeCalc Pointer 1
[0x047430,bytearray.fromhex('70 F4 31 08')],   #TypeCalc Pointer 2
[0x047504,bytearray.fromhex('70 F4 31 08')],   #AI trainer switch out
[0x047868,bytearray.fromhex('70 F4 31 08')],   #Used in levetate/wonderguard? 1
[0x04796C,bytearray.fromhex('70 F4 31 08')],   #Used in levetate/wonderguard? 2
[0x047A6C,bytearray.fromhex('70 F4 31 08')],   #"Good" trainer AI
[0x04CB2C,bytearray.fromhex('70 F4 31 08')],   #??? (Something in battle_script_command)
[0x0531D8,bytearray.fromhex('70 F4 31 08')],   #Used in conversion 2
[0x063F7C,bytearray.fromhex('70 F4 31 08')],   #AI trainer switch in?
[0x191498,bytearray.fromhex('70 F4 31 08')],   #Battle Dome
#Unused Section of ROM
[0xAF0000,bytearray(873)] #We need at most 873 empty bytes
],
newdata =[
#There are 10 pointers used by various functions that point to the Old Type Chart
#We want to change them to point to the new type chart at 0x08af0000
[0x0472F0,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 1
[0x047430,bytearray.fromhex('00 00 AF 08')],   #TypeCalc Pointer 2
[0x047504,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch out
[0x047868,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 1
[0x04796C,bytearray.fromhex('00 00 AF 08')],   #Used in levetate/wonderguard? 2
[0x047A6C,bytearray.fromhex('00 00 AF 08')],   #"Good" trainer AI
[0x04CB2C,bytearray.fromhex('00 00 AF 08')],   #??? (Something in battle_script_command)
[0x0531D8,bytearray.fromhex('00 00 AF 08')],   #Used in conversion 2
[0x063F7C,bytearray.fromhex('00 00 AF 08')],   #AI trainer switch in?
[0x191498,bytearray.fromhex('00 00 AF 08')],   #Battle Dome
]
)

EmeraldEXSpeedChoiceInfo = RomInfo(ROMID.EmeraldEXSpeedChoice,0x2000000,0x37b7C6,TCformat.MatrixUQ_4_12Gen6,NumberOfTypes = 18,
    checkdata =[
        # EX was allready designed to make randomizing type chart simpler
        # So no need to change or modify anything other then the type chart data it's self
        #Typechart data
        [0x37B7C6,bytearray([
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x00,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x00,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x08,
        0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x00,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,
        0x00,0x10,0x00,0x10,0x00,0x00,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,
        0x00,0x00,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x20,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x20,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x00,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x00,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x00,
        0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x08,
        0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x20,
        0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,
        0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,
        0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x08,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x08,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x20,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x08,0x00,0x10,0x00,0x10,
        0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,
        0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x20,
        0x00,0x10,0x00,0x08,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x20,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x10,0x00,0x08,0x00,0x08,0x00,0x10])]
    ],
    newdata = [] #No need to change any pointers or any functions with this one :)
)
