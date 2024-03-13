from random import randint
import re

def getValues(file:str): #type 1: IIR, type 2: JSON
    with open(f"input_ParaEQ/{file}.txt", 'r', encoding='UTF-8') as f:
        parametres = f.readlines()[1:]
        paraFiltres = []
        for i in parametres:
            if not "OFF" in i: #filtre les paramètres désactivés
                paraFiltres.append(i)
    valeurs = []
    typesPara = {"PK":3,"LSC":4,"HSC":5}
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

def paraToJSON(file:str,preamp):
    valeurs = getValues(file)
    bandes = [{"type":0,"channels":0,"frequency":90,"q":0,"gain":0.0,"color":0},{"type":1,"channels":0,"frequency":10000,"q":0,"gain":0.0,"color":0}]
    for filtre in valeurs:
        bandes.append({"type":filtre[0],"channels":0,"frequency":int(filtre[1]),"q":float(str(filtre[4])+"."+filtre[5]),"gain":float(str(filtre[6])+str(filtre[2])+"."+filtre[3]),"color": randint(-16711680,0)})
    json_text = str([{"name":file,"preamp":preamp,"parametric": True,"bands": bandes}]).replace("'",'"').replace("True","true")
    print(json_text,"\n")
    open(f"output_JSON/{file}_JSON.json", 'w', encoding='UTF-8').write(json_text)

file = "test"
paraToJSON(file,0.0)