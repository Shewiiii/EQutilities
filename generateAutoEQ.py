from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import traceback
from os import walk,rename,mkdir
import shutil
from scrapingFunctions import * 
from paraToIIRconverter import paraToIIR
from paraToJSONconverterPoweramp import paraToJSON
import time

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", "C:\\Users\\anhki\\Documents\\Scolaire\\FR_Scraper\\rename_input")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
driver = webdriver.Firefox(options=options)

link = "https://listener800.github.io/5128"

driver.get(link)
execute(driver,'document.getElementsByClassName("extra")[0].click()')
execute(driver,'document.getElementsByClassName("remove")[2].click()')
execute(driver,'document.getElementsByClassName("extra-eq-overlay")[0].style.width = "0"')
execute(driver,'document.getElementsByClassName("extra-eq-overlay")[0].style.padding = "0"')

for i in range(11):
    driver.find_element(By.CLASS_NAME,'add-filter').click()
file_input = driver.find_element(By.NAME, 'autoeq-to')
file_input.clear()
file_input.send_keys('20000')
file_input = driver.find_element(By.NAME, 'autoeq-q-to')
file_input.clear()
file_input.send_keys('10')

path = "C:\\Users\\anhki\\Documents\\Scolaire\\FR_Scraper\\frequency_responses\\" #relative path doesnt work wtf
filenames = next(walk(path), (None, None, []))[2]

def adddir(dir):
    try:
            mkdir(dir)
    except:
        print('Dossier preset déjà existant')

def batchAutoEQ(path,filenames,targetname):
    '''AutoEQ tous les IEMs désignés.
    mode=1: EQ tous les IEMs à une target donnée
    mode=2: EQ un IEM à toutes les targets données
    '''
    erreurs = []
    filenames = [filenames[0]] + filenames
    dir = f'./presets/{targetname}'
    adddir(f'./presets/{targetname}')
    for type in ['Parametric','IIR','Poweramp','Wavelet']:
        adddir(f'{dir}/{type}')
    driver.find_element(By.CLASS_NAME,'upload-fr').click()
    file_input = driver.find_element(By.ID, 'file-fr')
    file_input.send_keys(path+targetname+'.txt')
    driver.find_element(By.CLASS_NAME,'upload-target').click()
    for file in filenames:
        if targetname != file.replace('.txt',''):
            try:
                file_input.send_keys(path+file)
                driver.find_element(By.CLASS_NAME,'autoeq').click()
                time.sleep(2.5)
                try:
                    driver.find_element(By.CLASS_NAME,'export-filters').click()
                except:
                    time.sleep(2)
                    driver.find_element(By.CLASS_NAME,'export-filters').click()
                renamepath = "./rename_input"

                filename = next(walk(renamepath), (None, None, []))[2][0]
                newname = f"EQ to {file}"
                newpath = f'{renamepath}/{newname}'
                rename(f'{renamepath}/{filename}',newpath)
                final = f'{dir}/Parametric/{newname}'
                shutil.move(newpath,final)

                driver.find_element(By.CLASS_NAME,'export-graphic-filters').click()
                rename(f'{renamepath}/{filename.replace('Filters','Graphic Filters')}',newpath)
                shutil.move(newpath,f'{dir}/Wavelet/{newname}')

                paraToJSON(newname.replace('.txt',''),f'{dir}/Parametric',f'{dir}/Poweramp')
                paraToIIR(newname.replace('.txt',''),f'{dir}/Parametric',f'{dir}/IIR')
                execute(driver,'document.getElementsByClassName("remove")[1].click()')
            except:
                print(traceback.format_exc())
                input('')
                erreurs.append(file)
    return erreurs

erreurs = {}
for iem in filenames[0:]:
    erreurs[iem] = batchAutoEQ(path,filenames,iem.replace('.txt',''))
    for _ in range(2):
        execute(driver,'document.getElementsByClassName("remove")[2].click()')


