from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from fuzzywuzzy import fuzz


voice_list = ['Alloy (female)','Echo (male)','Fable (male)','Onyx (male, deeper voice)','Nova (female, soft)','Shimmer (female)']
current_voice_active_index = 3



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options)


website = r'https://ttsmp3.com/ai'
try :
    driver.get(website)
except :
    print('voice speak web is not available')

Buttonselection = Select(driver.find_element(by=By.ID,value='sprachwahl'))
Buttonselection.select_by_visible_text(voice_list[current_voice_active_index])


voice_text = driver.find_element(By.ID,'voicetext')
vorlesenbutton = driver.find_element(By.ID,value = 'vorlesenbutton')

def speak(text):  
    if text : 
        print('\ntext : '+ text +'\n')
        Data = str(text)
        voice_text.send_keys(Data)
        vorlesenbutton.click()
        while not vorlesenbutton.get_attribute('value') == 'Read' : pass
        voice_text.clear()

# speak('hello')


# this methode is for check how voice work 

def play_allVoices():
    # smaple_text = 'hello there i your voice assistant , would like to chose me '
    for i in voice_list :
        
        Buttonselection = Select(driver.find_element(by=By.ID,value='sprachwahl'))
        smaple_text = 'hello there i am ' + (i.split(' ')[0]) + '! would like to chose me as your Assistant voice'
        Buttonselection.select_by_visible_text(i)
        voice_text.send_keys(smaple_text)
        vorlesenbutton.click()
        while not vorlesenbutton.get_attribute('value') == 'Read' : pass
        voice_text.clear()
        


def change_voice(name) :
    for i in voice_list :
        i_name = i.split(' ')[0]
        if fuzz.ratio(name,i_name) > 60 :
            current_voice_active_index = voice_list.index(i)
            Buttonselection = Select(driver.find_element(by=By.ID,value='sprachwahl'))
            Buttonselection.select_by_visible_text(voice_list[current_voice_active_index])
            speak('voice is  change to %s!' % voice_list[current_voice_active_index])
            return True
    else :
        speak('voice is not changed ')
    
        
# play_allVoices()
# change_voice('aloy')