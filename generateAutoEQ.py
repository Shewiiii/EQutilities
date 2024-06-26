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
from pathlib import Path

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", "C:\\Users\\anhki\\Documents\\Scolaire\\EQutilities\\rename_input")
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

path = "C:\\Users\\anhki\\Documents\\Scolaire\\EQutilities\\frequency_responses\\" #relative path doesnt work wtf
filenames = next(walk(path), (None, None, []))[2]
redo = ['Sennheiser IE200 (AVG).txt']

def adddir(dir):
    try:
            mkdir(dir)
    except:
        print('Dossier preset déjà existant')

def iemiemEQ(path,filenames,targetname,redo=redo):
    erreurs = []
    filenames = [filenames[0]] + filenames
    dir = f'./presets/IEM_to_IEM/{targetname}'
    adddir(dir)
    for type in ['Parametric','IIR','Poweramp','Wavelet']:
        adddir(f'{dir}/{type}')
    driver.find_element(By.CLASS_NAME,'upload-fr').click()
    file_input = driver.find_element(By.ID, 'file-fr')
    file_input.send_keys(path+targetname+'.txt')
    driver.find_element(By.CLASS_NAME,'upload-target').click()
    for file in filenames:

        renamepath = "./rename_input"
        newname = f"EQ to {file}"
        newpath = f'{renamepath}/{newname}'
        final = f'{dir}/Parametric/{newname}'

        if targetname != file.replace('.txt','') and not Path(final).is_file() and file not in redo:
            try:
                file_input.send_keys(path+file)
                driver.find_element(By.CLASS_NAME,'autoeq').click()
                driver.find_element(By.CLASS_NAME,'export-filters').click()
                try:
                    time.sleep(0.3)
                    driver._switch_to.alert.dismiss()
                    driver.find_element(By.CLASS_NAME,'export-filters').click()
                except:
                    pass
                filename = next(walk(renamepath), (None, None, []))[2][0]
                rename(f'{renamepath}/{filename}',newpath)
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
        else:
            print('skipped:',file)
    return erreurs

def getTarget(driver):
    return driver.find_element(By.CLASS_NAME,'lineLabel').text.replace('/','').replace(':','')

def betterAutoEQ(path=path,filenames=filenames, redo=redo,manual=True):
    if manual == True:
        input('Choose a target on the tool')
    target = getTarget(driver)
    erreurs = []
    filenames = [filenames[0]] + filenames
    dir = f'./presets/betterAutoEQ/{target}'
    adddir(dir)
    for type in ['Parametric','IIR','Poweramp','Wavelet']:
        adddir(f'{dir}/{type}')
    driver.find_element(By.CLASS_NAME,'upload-fr').click()
    file_input = driver.find_element(By.ID, 'file-fr')
    for file in filenames:

        renamepath = "./rename_input"
        newname = f"{file.replace('.txt','')} [{target}].txt"
        newpath = f'{renamepath}/{newname}'
        final = f'{dir}/Parametric/{newname}'

        if not Path(final).is_file() and file not in redo:
            try:
                file_input.send_keys(path+file)
                driver.find_element(By.CLASS_NAME,'autoeq').click()
                driver.find_element(By.CLASS_NAME,'export-filters').click()
                try:
                    time.sleep(0.3)
                    driver._switch_to.alert.dismiss()
                    driver.find_element(By.CLASS_NAME,'export-filters').click()
                except:
                    pass
                filename = next(walk(renamepath), (None, None, []))[2][0]
                rename(f'{renamepath}/{filename}',newpath)
                shutil.move(newpath,final)

                driver.find_element(By.CLASS_NAME,'export-graphic-filters').click()
                rename(f'{renamepath}/{filename.replace('Filters','Graphic Filters')}',newpath)
                shutil.move(newpath,f'{dir}/Wavelet/{newname}')

                paraToJSON(newname.replace('.txt',''),f'{dir}/Parametric',f'{dir}/Poweramp')
                paraToIIR(newname.replace('.txt',''),f'{dir}/Parametric',f'{dir}/IIR')

                for i in range(2):
                    execute(driver,'document.getElementsByClassName("remove")[2].click()')
            except:
                print(traceback.format_exc())
                input('')
                erreurs.append(file)
        else:
            print('skipped:',file)
    return erreurs
erreurs = {}
num = 0
for filename in filenames:
    print(f'{num}. {filename}')
    num +=1

def autoiemiemEQ():
    for iem in filenames:
        erreurs[iem] = iemiemEQ(path,filenames,iem.replace('.txt',''))
        try:
            for _ in range(2):
                driver.execute_script('document.getElementsByClassName("remove")[2].click()')
        except:
            pass

def autoAutoEQ():
    targets = {'5128 DF':(-1,0,0,0),'5128 DF':(-1,0,0,-3),'JM-1 (IEM)':(-1,0,0,0),'JM-1 (IEM)':(-0.8,0,0,0),'SoundGuys':(0,0,0,0)} #tuple: tilt, ear gain in dB, first one will always will be -1dB tilt DF HRTF
    supported = ['5128 DF','JM-1 (IEM)']
    for target,adjustmentsValues in targets.items():
        betterAutoEQ(manual=False)
        if not target in driver.find_element(By.CLASS_NAME,'lineLabel').text:
            driver.find_element(By.XPATH,(f"//*[contains(text(),'{target}')]")).click()
        adjustments = ['cusdf-tilt','cusdf-bass','cusdf-treb','cusdf-ear']
        if target in supported:
            for i in range(4):
                file_input = driver.find_element(By.ID, adjustments[i])
                file_input.clear()
                file_input.send_keys(str(adjustmentsValues[i]))
    betterAutoEQ(manual=False)

def all():
    autoiemiemEQ()
    driver.find_element(By.XPATH,(f"//*[contains(text(),'5128 DF')]")).click()
    autoAutoEQ()

def showAllFR(limit=9999): #useful to show the resonance peak
    driver.find_element(By.CLASS_NAME,'upload-fr').click()
    n = 0
    for FR in filenames:
        file_input = driver.find_element(By.ID, 'file-fr')
        file_input.send_keys(path+FR)
        n +=1
        if n >= limit:
            return