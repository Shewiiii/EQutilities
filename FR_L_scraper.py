from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

driver = webdriver.Firefox()

lien = "https://listener800.github.io/5128?share=Custom_Tilt,Sundara&bass=0&tilt=-1&treble=0&ear=0".replace("tilt=-0.8","tilt=-1")
average = 1 #0: garde les 2 canaux, 1:fait la moyenne des deux
discriminant = "moyen" #texte présent dans le label, pour le différencier des autres valeurs spl (à utiliser si une seule courbe) 
temps_scraping = 20
####################################
if discriminant != "":
    average = 1

driver.get(lien)

stop = 0
while stop == 0:
    try:
        driver.execute_script("document.getElementById('expand-collapse').click(); \
                        document.getElementById('inspector').click()")
        stop = 1
    except:
        pass

stop = 0
while stop == 0:
    try:
        for i in range(2):
            driver.execute_script("document.getElementsByClassName('button-baseline')[0].click()")
        stop = 1
    except:
        pass
stop = 0

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
            print(test)
            test += 1
    except:
        pass


print("analyse")
valeurs = {}
for raw in raws:
    try:
        rawBS = BeautifulSoup(raw, features="html.parser")
        valeurs[rawBS.findAll('text',{'class':'insp_dB'})[0].text.replace(" Hz","")] = rawBS.findAll('g',{'class':'lineLabel'})
    except:
        pass

dBleft = {}
dBright = {}
dBavg = {}
for frequency in valeurs.keys():
    for g in valeurs[frequency]:
        try:
            if discriminant != "" and discriminant in g.text:
                dBavg[frequency] = g.find('g').text
                print(dBavg)
            elif "(L)" in g.text:
                dBleft[frequency] = g.find('g').text
            elif "(R)" in g.text:
                dBright[frequency] = g.find('g').text

        except Exception as e:
            print(e)
            pass

if average == 1 and discriminant == "": #split pour opti un peu
    for frequency in valeurs.keys():
        try:
            dBavg[frequency] = str((float(dBleft[frequency])+float(dBright[frequency]))/2)
        except:
            pass
        else:
            break

print(dBleft)
print(dBright)
print(dBavg)

if average == 1:
    with open("résultats_scraping/L/FR_AVG.txt", 'w', encoding='UTF-8') as m:
        m.write("\nFrequency	dB	Unweighted\n")
        for i in dBavg.keys():
            m.write(i + "\t" + dBavg[i] + "\n")
else:
    with open("résultats_scraping/L/FR_left.txt", 'w', encoding='UTF-8') as g:
        with open("résultats_scraping/L/FR_right.txt", 'w', encoding='UTF-8') as d:
            g.write("\nFrequency	dB	Unweighted\n")
            d.write("\nFrequency	dB	Unweighted\n")
            for i in dBleft.keys():
                g.write(i + "\t" + dBleft[i] + "\n")
                d.write(i + "\t" + dBright[i] + "\n")
