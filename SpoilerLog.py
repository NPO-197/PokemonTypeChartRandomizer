"""
function to generate a spoiler log for the randomizer by NPO-197
"""

def Spoiler(FileName,RandomTypeChart,seed,NumberOfTypes):
    TypeNamesGen1 = ['Bug', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Water']
    AbvrNamesGen1 = ",BUG,DRA,ELE,FIG,FIR,FLY,GHO,GRA,GRO,ICE,NOR,POI,PSY,ROC,WAT\n"
    TypeIndexGen1 = [6, 14, 11, 1, 8, 2, 7, 10, 4, 13, 0, 3, 12, 5, 9]
    TypeNamesGen2 = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    AbvrNamesGen2 = ",BUG,DAR,DRA,ELE,FIG,FIR,FLY,GHO,GRA,GRO,ICE,NOR,POI,PSY,ROC,STE,WAT\n"
    TypeIndexGen2 = [6, 16, 15, 12, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]
    TypeNamesGen6 = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    AbvrNamesGen6 = ",BUG,DAR,DRA,ELE,FAI,FIG,FIR,FLY,GHO,GRA,GRO,ICE,NOR,POI,PSY,ROC,STE,WAT\n"
    TypeIndexGen6 = [6, 16, 15, 12, 17, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]
    if NumberOfTypes==15:
        TypeNames = TypeNamesGen1
        AbvrNames = AbvrNamesGen1
        TypeIndex = TypeIndexGen1
    elif NumberOfTypes == 17:
        TypeNames = TypeNamesGen2
        AbvrNames = AbvrNamesGen2
        TypeIndex = TypeIndexGen2
    elif NumberOfTypes == 18:
        TypeNames = TypeNamesGen6
        AbvrNames = AbvrNamesGen6
        TypeIndex = TypeIndexGen6
    matchups = ['1.0','2.0','0.5','0.0']
    f = open(FileName,'w+')
    #Abreviate each type's name so it dosen't take up too much space
    f.write("Seed:"+str(seed)+AbvrNames)
    for i in range(NumberOfTypes):
        f.write(TypeNames[i])
        #The chart is stored in index format so we need to swap it into alphabetical format for the Tracker.
        for j in range(NumberOfTypes):
            try:
                f.write(','+matchups[RandomTypeChart[TypeIndex[i]][TypeIndex[j]]])
            except:
                print(NumberOfTypes)
                print(RandomTypeChart)
                raise
        f.write("\n")

    f.close()
