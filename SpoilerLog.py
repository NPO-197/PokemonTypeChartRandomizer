"""
function to generate a spoiler log for the randomizer by NPO-197
"""

def Spoiler(FileName,RandomTypeChart,seed,NumberOfTypes):
    if NumberOfTypes==18:
        spoilergen6(FileName,RandomTypeChart,seed)
        return
    TypeNames = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    TypeIndex = [6, 16, 15, 12, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]
    matchups = ['1.0','2.0','0.5','0.0']
    f = open(FileName,'w+')
    #Abreviate each type's name so it dosen't take up too much space
    f.write("Seed:"+str(seed)+",BUG,DAR,DRA,ELE,FIG,FIR,FLY,GHO,GRA,GRO,ICE,NOR,POI,PSY,ROC,STE,WAT\n")
    for i in range(17):
        f.write(TypeNames[i])
        #The chart is stored in index format so we need to swap it into alphabetical format for the Tracker.
        for j in range(17):
            try:
                f.write(','+matchups[RandomTypeChart[TypeIndex[i]][TypeIndex[j]]])
            except:
                print(RandomTypeChart)
                raise
        f.write("\n")

    f.close()


def spoilergen6(FileName,RandomTypeChart,seed):
    TypeNames = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    TypeIndex = [6, 16, 15, 12, 17, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]
    matchups = ['1.0','2.0','0.5','0.0']
    f = open(FileName,'w+')
    #Abreviate each type's name so it dosen't take up too much space
    f.write("Seed:"+str(seed)+",BUG,DAR,DRA,ELE,FAI,FIG,FIR,FLY,GHO,GRA,GRO,ICE,NOR,POI,PSY,ROC,STE,WAT\n")
    for i in range(18):
        f.write(TypeNames[i])
        #The chart is stored in index format so we need to swap it into alphabetical format for the Tracker.
        for j in range(18):
            try:
                f.write(','+matchups[RandomTypeChart[TypeIndex[i]][TypeIndex[j]]])
            except:
                print(RandomTypeChart)
                raise
        f.write("\n")

    f.close()
