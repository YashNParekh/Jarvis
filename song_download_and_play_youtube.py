import os
from pytube import YouTube
import pywhatkit
from fuzzywuzzy import fuzz

# path for auto-py-to-exe
# C:\Users\baps\AppData\Roaming\Python\Python311\Scripts



def download_youtube_video(video_name,play_after=False):
    try:
        # Create a YouTube object
        song_name = video_name.replace('song','')
        song_name = song_name.strip(' ')
        song_name = song_name.replace(' ','_')

        filename = 'D:\\Yash\\Final_project_jarvis\\music\\'+ song_name + '.mp4'
        print(filename)
        
        if os.path.exists(filename):
            print('already exists')
            return 'already exists'

        
        get_url =  pywhatkit.playonyt(video_name,open_video=False)
        print(get_url)
        yt = YouTube(get_url)

        # Get the highest resolution stream
      

        

        files = os.listdir('D:\Yash\Final_project_jarvis\music')
        for file_name in files:
        # print(file_name)
            if fuzz.ratio(file_name.replace('_',' ').replace('.mp4',''), song_name) >80 : 
                if play_after:
                    os.startfile( 'D:\\Yash\\Final_project_jarvis\\music\\' + file_name)
                return('already downloaded')
                
        else :
            yt.streams.get_highest_resolution().download(filename=filename)
            print('\n downloading song...... \n')
            print("Video downloaded successfully as", filename)
            
            if play_after:
                os.startfile(filename)
            return 'downloaded successfully'


    except Exception as e:
        print("An error occurred:", str(e))
        return 'not able to download video'

def play_song(name):
    files = os.listdir('D:\Yash\Final_project_jarvis\music')

# Print each file name
    for file_name in files:
        # print(file_name)
        if fuzz.ratio(file_name.replace('_',' ').replace('.mp4',''), name) >60 : 
          os.startfile('D:\\Yash\\Final_project_jarvis\\music\\'+file_name)
          print(file_name)
          return True
    else :
        return False

        

# # Example usage
# if __name__ == "__main__":
# #     # video_url = input("Enter the URL of the YouTube video: ")
#     download_youtube_video('o sanam')
# play_song('ale golmal')
#     pass

download_youtube_video('tu he kaha song',True)
# play_song('ye din bhi kya din the')
