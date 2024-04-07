import sounddevice as sd
import numpy as np
import time
import speech_recognition as sr
from threading import Thread
from googletrans import Translator 
import wikipedia
import threading
import pyttsx4
import speak_with_seleniume

# import speake_jarvis

# print(sd.query_devices())
# print(sd.default.device)

# outp_D_i = 5

# sd.default.device = [1,outp_D_i]



sample_rate = 44100  # Hz
num_channels = 1  # mono
dtype = 'int16'  # data type of audio samples




# for main all loop and full program 
main_status = True
 
#  hello jarvis status 
hello_jarvis_status = False


# main text make after say hello jarvis 
main_text = ''





recognizer = sr.Recognizer()

count_taking_text = 0

stream = sd.RawStream(samplerate=sample_rate, channels=num_channels, dtype=dtype)
stream.start()
    

def second_level_test():
     
# Open a raw input stream
    global stream
    # stream.start()
    
    
    first_start = False
    
    try:
        last_chunk,_ = stream.read(2000)
    except :
        print('error')

    count_voice = 0


    global main_text
    global hello_jarvis_status
    global main_status  
    global count_taking_text
    
    print('start taking speech')
    
    while main_status:

            try :
                data_chunk,_ = stream.read(2000)
            except : print('error')

            
            last_chunk = np.concatenate((last_chunk,data_chunk))


            indata = np.frombuffer(data_chunk, dtype=dtype)
            indata.shape = -1, 1
            amplitude = np.max(np.abs(indata[:, 0]))
            # print(amplitude , '  ')


            if  amplitude>25000 :
                if not first_start:
                    first_start = True
                    print('start')
                    
                # print(len(last_chunk))
                # if len(last_chunk)>200000: 
                #     Thread(target=speech_to_text, args=[last_chunk]).start()
                #     last_chunk = last_chunk[-8000:]
                #     print(threading.active_count())
                
                count_voice = 0
                count_taking_text = 0

            else : 
                count_voice+=1
                if hello_jarvis_status :
                    count_taking_text+=1
                    if count_taking_text == 20:
                        print('stop taking text')
                        main_text=main_text.strip()
                        if ('hello jarvis' == main_text) or 'hey jarvis' == main_text or ('hey buddy' == main_text) or 'jarvis' == main_text or 'hi jarvis' == main_text:
                            print('recording')
                            speak_text('hello!  yash how can i help you ')
                            main_text = ''
                            hello_jarvis_status = False
                        else :
                            print('in else ')
                            main_text = main_text[main_text.find('jarvis')+len('jarvis'):]
                            print('main text : '+ main_text)
                            main_text = ''
                            hello_jarvis_status = False

                        count_taking_text = 0
                            
                            
                if count_voice==30 and first_start:
                    # print(len(last_chunk))
                    print('send speech to text')
                    Thread(target=speech_to_text, args=[last_chunk]).start()
                    count_voice = 0

                    first_start = False


            if not first_start : 
                 if len(last_chunk)>=8000 :
                    # print(len(last_chunk))
                    last_chunk= last_chunk[-7000:]


def translate_text(text, target_language):
    translator = Translator()
    text_to_replace = ['જર્જ','જાર્વિસ્વિસ','જાળવીશ','જાર']
    for i in text_to_replace:
        if i in text :
            text = text.replace(i, 'jarvis')


    print(text)
        
        
    translated_text = translator.translate(text, dest=target_language)
    
    return translated_text.text


# def speak_text(text):
#     pass


#  for print text and get text in a order way 
last_text_printed = True

def speech_to_text(last_chunk):
    
    global main_text
    global last_text_printed
    global count_taking_text
    global hello_jarvis_status
    global main_status
    global stream
    
    


    al = sr.AudioData(last_chunk,sample_rate=sample_rate, sample_width=2)
    try :
        # print('here')
        text = recognizer.recognize_google(al,language='en')
        
        print(text)
        text = translate_text(text,'en')

        if 'exit' in text.lower():
                main_status = False
                print(text)
                return
        
        while not last_text_printed :
            time.sleep(0.0)
            pass
        last_text_printed = False
        

        
        print(text)
        

        
        text = text.lower()

        
        if (not hello_jarvis_status) and ( 'hello jarvis' in text or 'hey jarvis' in text or 'hey buddy' in text or 'jarvis' in text or 'hi jarvis' == main_text): 
            print('start recording')
    
            hello_jarvis_status = True
        if hello_jarvis_status :
            #  if text is black then it is not add 
            if text : 
                main_text += text+' '
        

        # last_text = text 
    except :
        print('not wrok')
        pass
    last_text_printed = True

def speak_text(text):
    global main_status 
    global stream
 
    try :
        # speake_jarvis.speake(text)
        print('text')
        main_status = False
        # stream.abort()
        # time.sleep(0.00)
        # # text = wikipedia.WikipediaPage('Intel').summary[:1000]
        # # print(text)
        # print(text)
        pyttsx4.speak(text)
        # # print('done to say ')

        # stream = sd.RawStream(samplerate=sample_rate, channels=num_channels, dtype=dtype)
        # stream.start()
        # print('done')

        speak_with_seleniume.speake(text)
        main_status = True

        Thread(target=(second_level_test)).start()
        
        
    except :
        pass

                

def main():
    try :
        Thread(target=(second_level_test)).start()
    except :
        exit(0)

if __name__ == "__main__":
    main()
