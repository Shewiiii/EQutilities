from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
#https://github.com/Shewiiii/EQutilities

driver = webdriver.Firefox()
lien = "https://crinacle.com/graphs/iems/graphtool/?share=Diffuse_Field_Target,EA500_Black,EA1000_White&tilt=-0.8&tool=4620".replace("tilt=-0.8","tilt=-1")
average = True #0: garde les 2 canaux, 1:fait la moyenne des deux
dualMode = False
brand = "Simgot"
iem1 = "EA500" #nom des IEM pour distinguer les valeurs lors du scraping (dualMode)
iem2 = "EA1000"
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

execute("window.scrollBy(0,2700)")
execute("document.getElementById('gdpr-consent-tool-wrapper').remove()")
execute("document.getElementById('AdThrive_Footer_1_desktop').remove()")
driver.switch_to.frame('GraphTool')
execute("document.getElementById('expand-collapse').click()")
execute("document.getElementById('inspector').click()")
for i in range(2):
    execute("document.getElementsByClassName('button-baseline')[0].click()")
input("go?")


raws = []
test = 0
source1 = driver.page_source 
t0 = time.time()
temps = 0
print("go")
while temps < 25: #à opti 
    temps = time.time() - t0
    try:
        source = driver.page_source 
        if source1 != source:
            source1 = source
            raws.append(source)
            print(test)
            test += 1
    except:
        pass


print("analyse")
valeurs = {}
for raw in raws:
    try:
        rawBS = BeautifulSoup(raw, features="html.parser")
        valeurs[rawBS.findAll('text',{'class':'insp_dB'})[0].text.replace(" Hz","")] = rawBS.findAll('g',{'class':'lineLabel'}) #[3:6]
    except:
        pass

dBleft = {}
dBright = {}
dBavg = {}
dBavg2 = {}
for frequency in valeurs.keys():
    for g in valeurs[frequency]:
        if dualMode == 1:
            try:
                if iem1 in g.text:
                    dBavg[frequency] = g.find('g').text
                elif iem2 in g.text:
                    dBavg2[frequency] = g.find('g').text
            except Exception as e:
                print(e)
                pass
        else:
            try:
                if "(L)" in g.text:
                    dBleft[frequency] = g.find('g').text
                elif "(R)" in g.text:
                    dBright[frequency] = g.find('g').text
            except Exception as e:
                print(e)
                pass
    if average == True and dualMode == False:
        try:
            dBavg[frequency] = str((float(dBleft[frequency])+float(dBright[frequency]))/2)
        except:
            pass

print(dBleft)
print(dBright)
print(dBavg)
print(dBavg2)

def save(dBlist,path):
    with open(path, 'w', encoding='UTF-8') as e:
        e.write("\nFrequency	dB	Unweighted\n")
        for i in dBlist.keys():
            e.write(i + "\t" + dBlist[i] + "\n")

if dualMode == True:
    save(dBavg,f"résultats_scraping/C/{brand}_{iem1}_AVG.txt")
    save(dBavg2,f"résultats_scraping/C/{brand}_{iem2}_AVG.txt")
elif average == True:
    save(dBavg,f"résultats_scraping/C/{brand}_{iem1}_AVG.txt")
else:
    save(dBleft,f"résultats_scraping/C/{brand}_{iem1}_Left.txt")
    save(dBright,f"résultats_scraping/C/{brand}_{iem1}_Right.txt")



