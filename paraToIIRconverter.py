import re

def getValues(fichier:str): #type 1: IIR, type 2: JSON
    with open(f"input_ParaEQ/{fichier}.txt", 'r', encoding='UTF-8') as f:
        parametres = f.readlines()[1:]
        paraFiltres = []
        for i in parametres:
            if not "OFF" in i: #filtre les paramètres désactivés
                paraFiltres.append(i)
    valeurs = []
    typesPara = {"PK":"peak","LSC":"lshelf","HSC":"hshelf"}
    typePara = ""
    for i in paraFiltres:
        negatif = ""
        if "-" in i: #indique si gain négatif ou non
            negatif = "-"
        for j in typesPara.keys(): #indique le type de paramètre (peak, low shelf etc)
            if j in i:
                typePara = typesPara[j]
        valeurs.append([typePara] + re.findall(r'\d+', i)[1:] + [negatif])
    return valeurs

def paraToIIR(fichier:str):
    valeurs = getValues(fichier)
    print(valeurs)
    string = ""
    for filtre in valeurs:
        print(filtre)
        string = string + f"iir:type={filtre[0]};f={filtre[1]};g={filtre[6]+filtre[2]+"."+filtre[3]};q={filtre[4]+"."+filtre[5]},"
    print(string,"\n")
    open(f"output_IIR/{fichier}_IIR.txt", 'w', encoding='UTF-8').write(string)



fichier = "monarch_to_variations"
paraToIIR(fichier)