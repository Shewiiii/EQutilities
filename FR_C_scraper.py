from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

driver = webdriver.Firefox()

lien = "https://crinacle.com/graphs/iems/graphtool/?share=Diffuse_Field_Target,Variations&tilt=-0.8&tool=4620".replace("tilt=-0.8","tilt=-1")
average = 1 #0: garde les 2 canaux, 1:fait la moyenne des deux
driver.get(lien)


stop = 0
while stop == 0:
    try:
        driver.execute_script("window.scrollBy(0,2700); \
                      document.getElementById('gdpr-consent-tool-wrapper').remove(); \
                      document.getElementById('AdThrive_Footer_1_desktop').remove()")
        stop = 1
    except:
        pass
stop = 0
driver.switch_to.frame('GraphTool')
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

dBgauche = {}
dBdroite = {}
dBMoy = {}
for frequence in valeurs.keys():
    for g in valeurs[frequence]:
        if "(L)" in g.text:
            dBgauche[frequence] = g.find('g').text
        elif "(R)" in g.text:
            dBdroite[frequence] = g.find('g').text
    if average == 1:
        try:
            dBMoy[frequence] = str((float(dBgauche[frequence])+float(dBdroite[frequence]))/2)
        except:
            pass

print(dBgauche)
print(dBdroite)
print(dBMoy)

if average == 1:
    with open("résultats_scraping/C/FR_moyen.txt", 'w', encoding='UTF-8') as m:
        m.write("\nFrequency	dB	Unweighted\n")
        for i in dBgauche.keys():
            m.write(i + "\t" + dBMoy[i] + "\n")
else:
    with open("résultats_scraping/C/FR_gauche.txt", 'w', encoding='UTF-8') as g:
        with open("résultats_scraping/C/FR_droite.txt", 'w', encoding='UTF-8') as d:
            g.write("\nFrequency	dB	Unweighted\n")
            d.write("\nFrequency	dB	Unweighted\n")
            for i in dBgauche.keys():
                g.write(i + "\t" + dBgauche[i] + "\n")
                d.write(i + "\t" + dBdroite[i] + "\n")
