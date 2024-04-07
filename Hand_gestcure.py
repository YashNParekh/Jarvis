import math

import time

import mediapipe as mp 

import cv2

import numpy as np 

import pyautogui

from threading import Thread


print('done')

#  set up for hand detact objects 
# record for camera 
cap  = cv2.VideoCapture(0)

mpHands = mp.solutions.hands

# set confidence acording required
# here the model complexity is use to chose for perfomence or ecuracy  
hands = mpHands.Hands(min_detection_confidence=0.4,model_complexity=1,min_tracking_confidence=0.3)

# draw lines 
mpdraw = mp.solutions.drawing_utils

screen_width ,screen_height =pyautogui.getInfo()[4].width,pyautogui.getInfo()[4].height


#  here i use both same beacuse take same value for both axis  x , y 
frame_width,frame_height = int(screen_width*0.8),int(screen_height*0.8)


# main_switch for all 
main_status = False

# main mouse cursor hande switch
main_mouse_cursor_status = False

# 
final_distance_hand =0

# result

hand_finger_status =[0,0,0,0,0]
hand_side = 'None'

results = None
frame = None

cap = cv2.VideoCapture(0)

distance = lambda x1,y1,x2,y2 : math.sqrt((y2-y1)**2 + (x2-x1)**2)


mode_list = [ 'volume','scroll','application switch']
mode_list_index = 0
two_finger_mode = mode_list[mode_list_index]



def find_hand():
    global results
    global frame
    global main_status
    
    q,m = ord('q'),ord('m')
    

    
    while main_status:
        
        frame = cv2.flip(cv2.resize(cap.read()[1],(frame_width,frame_height)),1) 
        
        # break
        imag_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = hands.process(imag_rgb)
        # time.sleep(0.0)
        # time.sleep(0.0)
        # time.sleep(0.0)
        
        balck_canvas = np.zeros_like(frame)
        cv2.rectangle(balck_canvas,(100,100),(frame_width-100,frame_height-100),color=(255,0,0))
        cv2.imshow('hand',balck_canvas)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks :
                mpdraw.draw_landmarks(balck_canvas,handLms,mpHands.HAND_CONNECTIONS)

                cv2.imshow('hand',balck_canvas)
                break
        cv2.imshow('hand',balck_canvas)
        if cv2.waitKey(1) & 0xFF == q:
            stop_programe()


            
        # time.sleep(0.008)
        time.sleep(0.00)
        time.sleep(0.00)
        time.sleep(0.00)

        


        
        
        
        # time.sleep(0.05)
      





    

def check_finger_status():
    global results
    global main_status
    # global final_distance_hand
    global hand_finger_status 
    global main_mouse_cursor_status
    global distance

    
    

    
    all_f_up =  False
    count_fing = 0
    count_down = 0
    
    switch = False
    

    
    while main_status :
        # break
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks :
  
                p0 = handLms.landmark[0]
                p6 = handLms.landmark[6]
                p5 = handLms.landmark[5]
                p3 = handLms.landmark[3]

    
                p8 = handLms.landmark[8]
                p12 = handLms.landmark[12]
                p16 = handLms.landmark[16]
                p17 = handLms.landmark[17]
                p20 = handLms.landmark[20]

                x = (handLms.landmark[12].x - handLms.landmark[0].x)*1000
                y = (handLms.landmark[12].y - handLms.landmark[0].y)*1000
                if abs(x)>abs(y):
                     hand_side = 'left' if x<0 else 'right'
                else :
                     hand_side = 'up' if y<0 else 'down'


                p_d_17_0 = distance(p17.x,p17.y,p0.x,p0.y)*1.2


                hand_finger_status[0] = True if  distance(p5.x,p5.y,p6.x,p6.y)*0.8<distance(p5.x,p5.y,p3.x,p3.y) else False
                hand_finger_status[1] = True if  p_d_17_0<distance(p8.x,p8.y,p0.x,p0.y) else False
                hand_finger_status[2] = True if  p_d_17_0<distance(p0.x,p0.y,p12.x,p12.y) else False
                hand_finger_status[3] = True if  p_d_17_0<distance(p0.x,p0.y,p16.x,p16.y) else False
                hand_finger_status[4] = True if  p_d_17_0<distance(p0.x,p0.y,p20.x,p20.y) else False

          

               
                # print(hand_finger_status , '  ---   ',hand_side)





                if count_fing>0 :
                    count_down+=1
                    if  switch and main_mouse_cursor_status  :
                        main_mouse_cursor_status = False
                    if count_down==120:
                        count_down = 0
                        count_fing = 0  
                        if switch and (not main_mouse_cursor_status) :
                            main_mouse_cursor_status = True
                        all_f_up = False
                        # print('down')
                

                if hand_finger_status[1:].count(1)==4 and not all_f_up :
                    # print('alll are open ')
                    all_f_up = True
                elif hand_finger_status[1:].count(1)==0 and  all_f_up  :
                    count_down=0
                    count_fing+=1
                    print(count_fing)
                    all_f_up = False
                    # print('alll are closed ')
                    

                if count_fing ==2 and count_down>70 :
                        if not switch:
                            main_mouse_cursor_status = True
                            switch = True
                            print("mouse control is on now ")
                        else :
                            main_mouse_cursor_status = False
                            switch = False
                            print("mouse control is off now ")
                        count_fing = 0
                

                         
                if count_fing ==3 and count_down>70 :
                        pyautogui.keyDown('win')
                        pyautogui.keyDown('tab')
                        
                        pyautogui.keyUp('win')
                        pyautogui.keyUp('tab')
                        count_fing = 0

                if count_fing >=4 and count_down>60:
                    stop_programe()
                
                break  # remove this for two hands 

            time.sleep(0.01)

        else : 
            time.sleep(0.05)
                



stop_mouse_cursor_status = True

def click_functio():
    global results 
    global main_status
    global final_distance_hand
    global main_mouse_cursor_status
    global hand_finger_status
    global distance

    global mode_list_index
    global mode_list
    global two_finger_mode

    global stop_mouse_cursor_status
    
    
    mouse_click_satus = False
    
    
    
    count_cliked = 0
    
    # and main_mouse_cursor_status
    while main_status :
        if results.multi_hand_landmarks  and main_mouse_cursor_status :
            for hl in results.multi_hand_landmarks :
                
                

                p4 = hl.landmark[4] 
                p8 = hl.landmark[8]
                p7 = hl.landmark[7]
                p12 = hl.landmark[12]
                
       
                
                
                   
                if  distance(p8.x,p8.y,p7.x,p7.y)*1.8 > (distance(p8.x,p8.y,p4.x,p4.y)) and  all(hand_finger_status[1:])  : 
                    # print('click')
                    count_cliked =0
                    if not mouse_click_satus :
                        stop_mouse_cursor_status = False
                        pyautogui.mouseDown()
                        time.sleep(0.00)
                        stop_mouse_cursor_status = True
                        mouse_click_satus = True
                elif all(hand_finger_status[1:3]) and not all(hand_finger_status[3:]) : 
                    pyautogui.mouseUp()
                    mouse_click_satus = False
                    
                    
                    if distance(p8.x,p8.y,p7.x,p7.y)*1.2>distance(p8.x,p8.y,p4.x,p4.y) :
                        
                        print('up')
                        if two_finger_mode == mode_list[0]:
                            pyautogui.press('volumeup')
                        if two_finger_mode == mode_list[1]:
                            pyautogui.scroll(-100)
                        if two_finger_mode == mode_list[2]:
                            pyautogui.keyDown('alt')
                            pyautogui.press('tab')
                            pyautogui.press('left')
                            pyautogui.press('left')
                            pyautogui.keyUp('alt')

                     
                        
                    elif  distance(p8.x,p8.y,p7.x,p7.y)*1.2>distance(p4.x,p4.y,p12.x,p12.y) : 
                        if two_finger_mode == mode_list[0]:
                            pyautogui.press('volumedown')
                        if two_finger_mode == mode_list[1]:
                            pyautogui.scroll(100)
                        if two_finger_mode == mode_list[2]:
                            pyautogui.keyDown('alt')
                            pyautogui.press('tab')
                            pyautogui.press('right')
                            pyautogui.press('right')
                            pyautogui.keyUp('alt')

                     
                else :                            
                    if count_cliked>=100 :
                        if mouse_click_satus :
                            stop_mouse_cursor_status = False
                            pyautogui.mouseUp()
                            time.sleep(0.0)
                            stop_mouse_cursor_status = True
                            mouse_click_satus = False
                            print('non')
                    else :
                        count_cliked+=1
                        # print('ciked')



                    time.sleep(0.00)
                time.sleep(0.0)
                time.sleep(0.0)
                time.sleep(0.0)
                    
                break
        else : 
            time.sleep(1)




# function for move cursor potion 
def mouse_potion_set():
    global main_status
    global main_mouse_cursor_status
    global hand_finger_status
    global results
    

    # change mouse cursor boundry for better perfomance 
    

    
    clocx ,clocy ,plocx ,plocy = 0,0,0,0
    
    smoothing  = 5
    

    while main_status:
        
        if results.multi_hand_landmarks and main_mouse_cursor_status and all(hand_finger_status[1:]) :
                hl = results.multi_hand_landmarks[0] 
                # set_ratio = (final_distance_hand/100)
                # set_ratio = 1
                
                fing1 = [((hl.landmark[8].x)*screen_width) ,(hl.landmark[8].y)*screen_height]
                cx = np.interp(fing1[0],(100,screen_width-400),(0,screen_width))
                cy = np.interp(fing1[1],(100,screen_height-400),(0,screen_height))

                
                # fing1 = [((hl.landmark[8].x*screen_width) +hl.landmark[8].x*screen_width*.50) ,((hl.landmark[8].y*screen_height)+hl.landmark[8].y*screen_height*0.50)]
                # cx =  0 if fing1[0]<5 else screen_width if fing1[0]>screen_width else fing1[0]
                # cy =  0 if fing1[1]<3 else screen_height-7 if fing1[1]>screen_height-5 else fing1[1]
                
                 
                # print(fing1)

                clocx = plocx + (cx-plocx)/smoothing
                clocy = plocy + (cy-plocy)/smoothing
                # print( cx,cy,clocx,clocy)
                pyautogui.moveTo(clocx,clocy)
                plocx , plocy = clocx,clocy
                time.sleep(0.00)
                # time.sleep(0.00)
                # time.sleep(0.00)
                
        else :
            time.sleep(1)
            pass
    
def stop_programe():
    global main_status
    global main_mouse_cursor_status 
    global results
    main_status = False
    main_mouse_cursor_status = False
    results = None
    return 'hand gasture is stopped'    
                


def main():
    global main_status
    global main_mouse_cursor_status 
    global results
    try :
        main_status = True
        main_mouse_cursor_status = False
        results = None
        print('helo')
        Thread(target=find_hand).start()

    
        while type(results)==type(None):pass

        Thread(target=check_finger_status).start()

        Thread(target=click_functio).start()
        Thread(target=mouse_potion_set).start()
    except :
        stop_programe()


main()
