# for making thread
import datetime
import os
import threading 
from threading import Thread
import webbrowser

# for use microphone of device 
from scipy.fft import fft
import sounddevice as sd 

# for make speech to text 
import speech_recognition as sr 

# for translate my text to onther laguage 
from googletrans import Translator

# for wikipedia
import wikipedia

# for some give some time limitations
import time

# import the speake fiel from directory
import speak_with_seleniume
import speak_with_pyttsx4
# numpy 
import numpy as np

# for play song that download
import song_download_and_play_youtube

# file for asking using selenium
import What_is_meaning

# for better mathing text
from fuzzywuzzy import fuzz

# hand gesture
import Hand_gestcure


# for play vdeio on youtube 
import pywhatkit 



# microphone voice peramters 



sample_rate = 44100  # Hz
num_channels = 1  # mono
dtype = 'int16'  # data type of audio samples


# control parameters


#  ->  for main all loop and full program 
main_status = True


# user Name 

user_name = 'Yash'

#  -> jarvis call status 
hello_jarvis_status = False


# make list of laguage and their sort name for use 
language_data = dict()
with open(r'D:\Yash\Final_project_jarvis\FInal Jarvis\FINAL JARVIS\Language_and_code','r') as temp_laguage_data:
    language_data =  {  i.split(':')[1].strip().lower() : i.split(':')[0].strip().lower()    for i in temp_laguage_data.read().split('\n')}
print(language_data)

    

current_input_laguage_type = 'en'
current_output_laguage_type = 'en'
    


#  main text after call jarvis
main_text = ''

# recognizer for text 
recognizer = sr.Recognizer()

# stream for input voice 
stream = sd.RawStream(samplerate=sample_rate, channels=num_channels, dtype=dtype)
stream.start()
# count for  take text and add main text 

count_add_text = 0 

# store last printed text
last_text_printed = True


#  traine jarvis for what say and what ans to give

message = ['hello jarvis'] 

# for close input when exicuting the speech work 
temp_stop_to_take_speech = False 


first_start = False

#  take voice 

def take_voice():
    global stream 
    global main_status
    global main_text
    global hello_jarvis_status
    global temp_stop_to_take_speech
    global first_start
    
    
    # max frequency and amplitude
    # max_amplitude = 17000
    # second_max_amplitude = 15000
    max_amplitude = 12000
    second_max_amplitude = 12000


    # max count_for down amplitude 
    max_count_for_down_cuttof = 30
    
    
    # start sign to conert voice into text and add 
    # this is use for how much time and how voice chunk we 
    # concatenate and then send to text convertor 
    first_start = False
    
    # frame read 
    read_frame = 2000
    
    # insial read voice for starting 
    last_chunk = stream.read(read_frame)[0]
    
    # count for add voice in chunk
    # if it is reach maximum then stop 
    count_voice = 0

    
    print('start recording')
    while main_status:

        if temp_stop_to_take_speech : continue
        
        
        
        try :
            data_chunk,_ = stream.read(read_frame)
        except :
            # here the read  methode not raised error 
            # this is raised when this method is take some data 
            # and at that time we stop the stream and the read is give error  
            continue
        
        # adding chunk to last chunk 
        last_chunk = np.concatenate((last_chunk,data_chunk))
        
        # now for find amplitude 
        
        indata = np.frombuffer(data_chunk, dtype=dtype)
        indata.shape = -1, 1
        amplitude = np.max(np.abs(indata[:, 0]))
        # print(amplitude ,end =' ')

        fft_result = fft(indata[:, 0])
        
        # Find the maximum frequency component in the FFT result
        max_freq_index = np.argmax(np.abs(fft_result))
        
        # The frequency corresponding to the maximum component
        max_frequency = max_freq_index * sample_rate / len(indata)
        
        # Print the frequency
        # print("Maximum Frequency:", max_frequency, "Hz")
        # continue


        #  if first start is not toogle then clear data chunk every time
        if (not first_start) and len(last_chunk)>=12000 :
            # print(len(last_chunk))
            last_chunk = last_chunk[-10000:]
            

       
        # if   amplitude>max_amplitude:
        if max_frequency >200 and 600<max_frequency and amplitude>max_amplitude:
            if not first_start:


                first_start = True
                
                # reset the value 
                count_voice = 0
                print('start')

                
       

            # if the voice data is higher then this lenght then we send the data to convert text
            # and then store some last data 
            # to avoid some text not recognized 
                
            # if len(last_chunk)>200000: 
            #         Thread(target=speech_to_text, args=[last_chunk]).start()
            #         last_chunk = last_chunk[-10000:]
            #         print(threading.activeCount())

        elif max_frequency >220 and 700<max_frequency  and amplitude>second_max_amplitude:
                count_voice = 0
        else :
            count_voice+=1
            if hello_jarvis_status :
                max_count_for_down_cuttof = 80
            else :
                max_count_for_down_cuttof = 80

            if count_voice==max_count_for_down_cuttof  :
                if first_start :
                    print(len(last_chunk))
                    Thread(target=speech_to_text, args=[last_chunk]).start()
                    last_chunk = last_chunk[-7000:]
                    print('send voice command')
                    first_start = False
            elif count_voice==120 and hello_jarvis_status : 
                    hello_jarvis_status = False
                    first_start = False
                    print('hello jarvis toggle close')
            else :
                if count_voice>140 :
                    count_voice=0

def speech_to_text(temp_chunk) :
    global last_text_printed    
    global main_text
    global hello_jarvis_status
    global temp_stop_to_take_speech
    global main_status
    global current_output_laguage_type
    global current_input_laguage_type
    global first_start


    al = sr.AudioData(temp_chunk,sample_rate=sample_rate, sample_width=2)
    try:
    # if True :
        text = recognizer.recognize_google(al,language=current_input_laguage_type)
        print(text)
        if current_input_laguage_type != 'en' and text:
            text = translate_text(text,'en').lower()
        else :
            text = text.lower()
            
        print('here',hello_jarvis_status)

        if (not hello_jarvis_status) :
            if ('hello jarvis' in text or 'hey jarvis' in text or 'hi jarvis' in text or 'jarvis' in text):
                temp_stop_to_take_speech = True
                if('hello jarvis' == text or 'hey jarvis' == text or 'hi jarvis' == text or 'jarvis' == text):
                    print('hello trigger')
                    hello_jarvis_status = True
                    main_text = ''
                    
                    speake_msg('hello yash how can i halp you today')
                    print('hello trigger')
                    first_start = True
              
                else : 
                    main_text = text
                    print( 'main text : ', main_text)
                    command_to_do(text)

                temp_stop_to_take_speech = False


        else :
            temp_stop_to_take_speech = True

            main_text = text
            command_to_do(text)
            print( 'main text : ', main_text)
            hello_jarvis_status = False
            temp_stop_to_take_speech = False

        


    except Exception as e :
        print(e)
        pass
        # print('speech not convert to text')
        
        
def speake_msg(speak_msg,not_translat_text=''):
    global current_output_laguage_type 
    global current_input_laguage_type
    global temp_stop_to_take_speech
    
    
    if temp_stop_to_take_speech:
        temp_stop_to_take_speech = False
    speak_msg = translate_text(speak_msg,current_output_laguage_type)
    speak_with_seleniume.speak(speak_msg+not_translat_text)
    temp_stop_to_take_speech = True


def translate_text(temp_text,language):
    
    try : 
        translator = Translator()

        if current_input_laguage_type=='gu':
            text_to_replace = ['જર્જ','જાર્વિસ્વિસ','જાળવીશ','જાર']
            for i in text_to_replace:
                if i in temp_text :
                    temp_text = temp_text.replace(i, 'jarvis')
        
        
        translated_text = translator.translate(temp_text, dest=language)

        return translated_text.text


    except Exception as e :
        print(e)
        print('error in translet_text')
        return ''








def command_to_do(text):
    global main_status
    global current_input_laguage_type
    global current_output_laguage_type
    global temp_stop_to_take_speech



    if not text : return

    print('in command_to_do')

    print(text)

    
    
    if 'exit' in text : 
        main_status = False
        if Hand_gestcure.main_status:
            Hand_gestcure.main_status = False
        print('exit')
        return
    

    elif 'play' in text  and 'song' in text :
        
        print('play from song')
        song_name = ''
        try :
            if 'song' in text :
                song_name = text[text.find('play') + 4 :text.find('song')]

            speake_msg('playing ',song_name)
            print('song name',song_name)
            song_download_and_play_youtube.play_song(song_name.strip())

            
        except Exception as e :
            print( 'error', e)

    elif 'open youtube' in text:
            webbrowser.Chrome("C:\Program Files\Google\Chrome\Application\chrome.exe").open_new_tab("https://www.youtube.com/")
    elif 'open google' in text:
            webbrowser.open("google.com")
    # elif 'search' in text and ('on' in text or 'in' in text) and 'chrome' in text:
    #         webbrowser.Chrome("C:\Program Files\Google\Chrome\Application\chrome.exe").open_new_tab("https://www.youtube.com/")

    elif 'what is the time' in text:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speake_msg(f" the time is {strTime}")

    elif 'play' in text and ('on' in text or 'in' in text) and 'youtube' in text:
            vedio_name = text.strip()[text.find('play')+4 : text.find('on' if 'on' in text else 'in')]
            pywhatkit.playonyt(vedio_name)

    elif 'download' in text and ('song' in text) and 'music folder' in text :

        song_name = text[text.rfind('download') + 8 :text.rfind('song') ]
        print('download song name',song_name)
        temp_stop_to_take_speech = True


        speake_msg(song_download_and_play_youtube.download_youtube_video(song_name.strip()))   
        if 'play it' in text :
            song_download_and_play_youtube.play_song(song_name.strip())
        return
            

    elif ('change' in text or 'need' in text or 'convert' in text)  and 'language' in text and 'input' in text:

        if 'language in' in text :
            new_language = text[text.rfind('language in')+11:]
        elif 'language as' in text :
            new_language = text[text.rfind('language as')+11:]
        else :
            new_language = text[text.rfind('to')+2:]
        print(current_input_laguage_type)
        current_input_laguage_type = language_data[new_language.strip().replace('.','')]
        speake_msg('laguage is changed successfully')
        print(current_input_laguage_type)
        return

    
    elif ('change' in text or 'need' in text or 'convert' in text)  and 'language' in text and 'output' in text: 
        if 'language in' in text :
            new_language = text[text.rfind('language in')+11:]
        elif 'language as' in text :
            new_language = text[text.rfind('language as')+11:]
        else :
            new_language = text[text.rfind('to')+2:]
        print(current_output_laguage_type)
        current_output_laguage_type = language_data[new_language.strip().replace('.','')]
        speake_msg('laguage is changed successfully')
        print(current_output_laguage_type)
        return
        
    elif ('what' in text or 'the' in text or 'tell me' in text or 'give me information'  ) and ('meaning' in text or 'about' in text)  :
        print('in tell me ...')
        text = text[text.find('jarvis')+6:]
        text = What_is_meaning.tell_me_about(text)
        print(text)
        speake_msg(text)
        return

    elif 'turn' in text and 'on' in text and 'gesture' in text :
        print(Hand_gestcure.main_status)
        if not Hand_gestcure.main_status:
            Hand_gestcure.main()
        return

    elif 'turn' in text and 'off' in text and 'gesture' in text :
        # if Hand_gestcure.main_status:
            Hand_gestcure.main_status = False
            Hand_gestcure.main_mouse_cursor_status = False
            Hand_gestcure.results = None
            
    elif 'change ' in text and 'gesture' in text  and 'mode' in text and 'to' in text :
        new_mode = text[text.find('to')+2:]
        print(new_mode)
        for i in Hand_gestcure.two_finger_mode :
            if fuzz.ratio(i,new_mode.strip()) >50 :
                Hand_gestcure.mode_list_index = Hand_gestcure.two_finger_mode.find(i) 
                speake_msg('mode changed to '+ new_mode)
                break
        else :
            speake_msg('mode not found')
        return



def main():
    try :
        Thread(target=(take_voice)).start()
    except :
        exit(0)

if __name__ == "__main__":
    main()


