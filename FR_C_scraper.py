from selenium import webdriver
import time
from bs4 import BeautifulSoup
import traceback
from scrapingFunctions import *
#https://github.com/Shewiiii/EQutilities

driver = webdriver.Firefox()
lien = "https://crinacle.com/graphs/iems/graphtool/?share=Diffuse_Field_Target,EA500_Black&tilt=-1&tool=4620".replace("tilt=-0.8","tilt=-1")
temps_scraping = 25
average = False #0: garde les 2 canaux, 1:fait la moyenne des deux, ignoré si dualMode
dualMode = False #Si False, mettre la FR pour L et R
brand = "Simgot"
iem1 = "EA500" #nom des IEM pour distinguer les values lors du scraping (dualMode)
iem2 = "EA1000"
####################################
driver.get(lien)

execute(driver,"window.scrollBy(0,2700)")
execute(driver,"document.getElementById('gdpr-consent-tool-wrapper').remove()")
execute(driver,"document.getElementById('AdThrive_Footer_1_desktop').remove()")
driver.switch_to.frame('GraphTool')
execute(driver,"document.getElementById('expand-collapse').click()")
execute(driver,"document.getElementById('inspector').click()")
for i in range(2):
    execute(driver,"document.getElementsByClassName('button-baseline')[0].click()")
input("go?")


raws = []
test = 0
source1 = driver.page_source 
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
        values[rawBS.findAll('text',{'class':'insp_dB'})[0].text.replace(" Hz","")] = rawBS.findAll('g',{'class':'lineLabel'}) #[3:6]
    except:
        pass

dBleft = {}
dBright = {}
dBavg = {}
dBavg2 = {}

for frequency in values.keys():
    if dualMode == True:
        for g in values[frequency]:
            try:
                gtext = getGText(g)
                if gtext != None:
                    if iem1 in g.text:
                        dBavg[frequency] = gtext
                    elif iem2 in g.text:
                        dBavg2[frequency] = gtext
            except:
                print(traceback.format_exc())
                pass
    else:
        for g in values[frequency]:
            try:
                gtext = getGText(g)
                if gtext != None:
                    if "(L)" in g.text:
                        dBleft[frequency] = gtext
                    elif "(R)" in g.text:
                        dBright[frequency] = gtext
            except:
                print(traceback.format_exc())
                pass

if average == True and dualMode == False: #séparer pour opti un peu
    for frequency in values.keys():
        try:
            dBavg[frequency] = str((float(dBleft[frequency])+float(dBright[frequency]))/2)
        except:
            print(traceback.format_exc())
            pass

print("left:",dBleft)
print("right:",dBright)
print("average:",dBavg)
print("average2:",dBavg2)

def save(dBlist,path):
    with open(path, 'w', encoding='UTF-8') as e:
        e.write("\nFrequency	dB	Unweighted\n")
        for i in dBlist.keys():
            e.write(i + "\t" + dBlist[i] + "\n")

if dualMode == True:
    save(dBavg,f"résultats_scraping/C/{brand} {iem1} (AVG).txt")
    save(dBavg2,f"résultats_scraping/C/{brand} {iem2} (AVG).txt")
elif average == True:
    save(dBavg,f"résultats_scraping/C/{brand} {iem1}_(AVG).txt")
else:
    save(dBleft,f"résultats_scraping/C/{brand} {iem1} (L).txt")
    save(dBright,f"résultats_scraping/C/{brand} {iem1} (R).txt")



