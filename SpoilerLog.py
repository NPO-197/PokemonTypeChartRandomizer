#function to generate a spoiler log for the randomizer
def Spoiler(FileName,RandomTypeChart,seed):
    TypeNames = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    TypeIndex = [6, 16, 15, 12, 1, 9, 2, 7, 11, 4, 14, 0, 3, 13, 5, 8, 10]
    f = open(FileName,'w+')
    #Abreviate each type's name so it dosen't take up too much space
    f.write("Seed:"+str(seed)+",BUG,DAR,DRA,ELE,FIG,FIR,FLY,GHO,GRA,GRO,ICE,NOR,POI,PSY,ROC,STE,WAT\n")
    for i in range(17):
        f.write(TypeNames[i])
        #the type effectiveness is stored in hexadecimal as 10*(effectiveness) so we convert to an int and divide by 10
        for j in range(17):
            f.write(','+str(int(RandomTypeChart[TypeIndex[i]][TypeIndex[j]],16)/10))
        f.write("\n")

    f.close()
