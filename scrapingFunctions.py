from selenium import webdriver
from bs4 import BeautifulSoup
import time
def execute(driver,script):
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

def save(dBlist,path):
    with open(path, 'w', encoding='UTF-8') as e:
        e.write("\nFrequency	dB	Unweighted\n")
        for i in dBlist.keys():
            e.write(i + "\t" + dBlist[i] + "\n")

def getGText(g):
    gElement = g.find('g')
    if gElement != None:
        return gElement.text
    else:
        return None