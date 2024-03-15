from selenium import webdriver
import time
from bs4 import BeautifulSoup
import traceback
from scrapingFunctions import *
#https://github.com/Shewiiii/EQutilities

driver = webdriver.Firefox()
lien = "https://listener800.github.io/5128?share=Custom_Tilt,RED,LCD2,Utopia2022AVG,DT770,580,HD600,HD650,HD660S2,HD800S,IE200&bass=0&tilt=-1&treble=0&ear=0".replace("tilt=-0.8","tilt=-1")
average = True #0: garde les 2 canaux, 1:fait la moyenne des deux
multiMode = True
brand = ["Audeze","Truthear","Beyerdynamic","Focal","Sennheiser","Sennheiser","Sennheiser","Sennheiser","Sennheiser","Sennheiser"]
iems = ["LCD-2.0","RED","DT770 Pro","Utopia 2022","HD 580 Precision","HD 600","HD 650","HD 660S2","HD 800S","IE 200"] 
temps_scraping = 60
####################################

print(lien)
driver.get(lien)

execute(driver,"document.getElementById('expand-collapse').click()")
execute(driver,"document.getElementById('inspector').click()")
for i in range(2):
    execute(driver,"document.getElementsByClassName('button-baseline')[0].click()")
input("go?")


raws = []
test = 0
source1 = driver.page_source 
stop = 0
t0 = time.time()
temps = 0
print("go")
while temps < temps_scraping: #à opti 
    temps = time.time() - t0
    try:
        source = driver.page_source 
        if source1 != source:
            source1 = source
            raws.append(source)
            print(test,temps,end="\r")
            test += 1
    except:
        pass


print("analyse                 ")
values = {}
for raw in raws:
    try:
        rawBS = BeautifulSoup(raw, features="html.parser")
        values[rawBS.findAll('text',{'class':'insp_dB'})[0].text.replace(" Hz","")] = rawBS.findAll('g',{'class':'lineLabel'})
    except:
        pass

dBleft = {}
dBright = {}
dBavg = {}
iemsdB = {}

if multiMode == True:
    for iem in iems:
        dBavg = {}
        for frequency in values.keys():
            for g in values[frequency]:
                try:
                    gtext = getGText(g)
                    if iem in g.text and gtext != None:
                        dBavg[frequency] = gtext
                        break
                except:
                    print(traceback.format_exc())
                    pass
        iemsdB[iem] = dBavg
else:
    for frequency in values.keys():
        for g in values[frequency]:
            try:
                gtext = getGText(g)
                if getGText != None:
                    if iems[0] in g.text:
                        dBavg[frequency] = gtext
                        break
                    elif "(L)" in g.text:
                        dBleft[frequency] = gtext
                    elif "(R)" in g.text:
                        dBright[frequency] = gtext
            except:
                print(traceback.format_exc())
                pass
    if average == True and multiMode == False:
        try:
            dBavg[frequency] = str((float(dBleft[frequency])+float(dBright[frequency]))/2)
        except:
            print(traceback.format_exc())
            pass

print("left:",dBleft)
print("right:",dBright)
print("average:",dBavg)

def save(dBlist,path):
    with open(path, 'w', encoding='UTF-8') as e:
        e.write("\nFrequency	dB	Unweighted\n")
        for i in dBlist.keys():
            e.write(i + "\t" + dBlist[i] + "\n")
if multiMode == True:
    num = 0
    for iem,dB in iemsdB.items():
        save(dB,f"résultats_scraping/L/{brand[num]} {iem} (AVG).txt")
        num+=1
elif average == True:
    save(dBavg,dBright)
else:
    save(dBleft,f"résultats_scraping/L/{brand[0]} {iems[0]} (L).txt")
    save(dBright,f"résultats_scraping/L/{brand[0]} {iems[0]} (R).txt")

