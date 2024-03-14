from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import traceback
#https://github.com/Shewiiii/EQutilities

driver = webdriver.Firefox()
lien = "https://listener800.github.io/5128?share=Custom_Tilt,U6t,ScarletMini,Crimson,Helios,Hexa,Nova&bass=0&tilt=-1&treble=0&ear=0".replace("tilt=-0.8","tilt=-1")
average = True #0: garde les 2 canaux, 1:fait la moyenne des deux
multiMode = True
brand = ["FATFreq","Symphonium","Truthear","Truthear","Symphonium","64 audio"]
iems = ["Scarlet Mini","Crimson (Azla Sedna Tips)","Hexa","Nova (AET07 Tips)","Helios (Azla Sedna Tips)","U6t (m20)"] 
temps_scraping = 35
####################################

print(lien)
driver.get(lien)

def execute(script):
    tries = 0
    stop = 0
    while stop == 0:
        try:
            driver.execute_script(script)
            stop = 1
        except:
            time.sleep(0.1)
            tries += 1
            if tries >= 100:
                stop = 1
            pass

execute("document.getElementById('expand-collapse').click()")
execute("document.getElementById('inspector').click()")
for i in range(2):
    execute("document.getElementsByClassName('button-baseline')[0].click()")
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


print("analyse")
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

def getGText():
    gElement = g.find('g')
    if gElement != None:
        return gElement.text
    else:
        return None

if multiMode == True:
    for iem in iems:
        dBavg = {}
        for frequency in values.keys():
            for g in values[frequency]:
                try:
                    gtext = getGText()
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
                gtext = getGText()
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

