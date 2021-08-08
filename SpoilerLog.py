#function to generate a spoiler log for the randomizer
def Spoiler(FileName,RandomTypeChart,seed):
    TypeNames = ['Normal','Fighting','Flying','Poison','Ground','Rock','Bug','Ghost','Steel','Fire','Water','Grass','Electric','Psychic','Ice','Dragon','Dark']
    f = open(FileName,'w+')
    f.write("RNG Seed:"+str(seed)+'\r')
    f.write("Defending >>\r")
    #Abreviate each type's name so it dosen't take up too much space
    f.write("Attacking VV\t|NOR|FIG|FLY|POI|GRO|ROC|BUG|GHO|STE|FIR|WAT|GRA|ELE|PSY|ICE|DRA|DAR|\r\n")
    for i in range(17):
        f.write(TypeNames[i]+"\t")
        #if the typename is too short add an extra 'tab' character so it all lines up
        if len(TypeNames[i]) < 8:
                f.write("\t")
        #the type effectiveness is stored in hexadecimal as 10*(effectiveness) so we convert to an int and divide by 10
        for j in range(17):
            f.write('|'+str(int(RandomTypeChart[i][j],16)/10))
        f.write("|\r")

    f.close()
