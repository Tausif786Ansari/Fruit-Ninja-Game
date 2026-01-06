import cv2
import numpy as np
from hand_tracker import HandTracker
from objects import FruitClass,BombClass
import random as rd
import pygame
import json
import os
#-------------Constants----------------------
SPEED = 5
LIVES = 3
TRAIL = []
OBJECTS = []
SCORE = 0
GAME_OVER = False
RESTART = False
if 'HighScore.json' in os.listdir('assets'):
    with open('D:/language/mediapipe/mp_env/Fruit_Ninja/assets/HighScore.json','r') as f:
        HIGHSCORE = int(json.load(f)['HighScore'])
else:
    HIGHSCORE = 0

#-------------Mouse CallBack Function-----------
def mouse_click(event, x, y, flags, param):
    global GAME_OVER, RESTART, LIVES, SCORE, OBJECTS, SPEED, FRAME

    if GAME_OVER and event == cv2.EVENT_LBUTTONDOWN:
        # START button
        if 300 <= x <= 500 and 320 <= y <= 370:
            LIVES = 3
            SCORE = 0
            SPEED = 5
            FRAME = 0
            OBJECTS.clear()
            GAME_OVER = False
            RESTART = True

        # END button
        if 300 <= x <= 500 and 390 <= y <= 440:
            Cap.release()
            cv2.destroyAllWindows()
            

#-------------Playing sound------------------
pygame.mixer.init()
slice_sound = pygame.mixer.Sound("assets/fruit.wav")
bomb_sound = pygame.mixer.Sound("assets/bomb.wav")
#--------------Drawing Line------------------
def DrawLine(frame,x,y):
    if x is None or y is None:
        TRAIL.clear()
        return
    TRAIL.append((x,y))
    if len(TRAIL)>20:
        TRAIL.pop(0)
    for i in range(1,len(TRAIL)):
        cv2.line(frame,TRAIL[i-1],TRAIL[i],(0,0,255),3,cv2.LINE_AA)
        
#----------------Spwan Function--------------------
def spawn_img(fruit_img,bomb_img,speed):
    if rd.randint(1,10) > 8:
        return BombClass(bomb_img,speed)
    return FruitClass(rd.choice(fruit_img),speed)
#-----------------Load Images-----------------------
def load_img(img_path,size=(60,60)):
    img = cv2.imread(img_path,cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img,size)
    return img
#-----------------Selecting Images-----------------------------
Apple = ['apple1.png','apple2.png','apple3.png','apple4.png']
Banana = ['banana1.png','banana2.png','banana3.png']
Melon = ['watermelon1.png','watermelon2.png','watermelon3.png']
Bomb = ['bomb1.png','bomb2.png','bomb3.png']
FRUITS = [
    load_img(f"assets/{rd.choice(Apple)}"),load_img(f"assets/{rd.choice(Banana)}"),
    load_img(f"assets/{rd.choice(Melon)}")]
BOMB = load_img(f"assets/{rd.choice(Bomb)}")

#-----------------Creating VideoObject & HandTrackingObject---------------       
cv2.namedWindow("Fruit Ninja",cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("Fruit Ninja", mouse_click)
Cap = cv2.VideoCapture(0)
track_obj = HandTracker()
FRAME = 0
#----------------Main Loop---------------------
while Cap.isOpened():
    ret,frame = Cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(800,600))
    frame = cv2.flip(frame,1)
    
    #--------Tracking Finger----------------
    finger = track_obj.get_finger(frame)
    if finger is not None:
        fx,fy = finger
        DrawLine(frame,fx,fy)
    else:
        DrawLine(frame,None,None)
        
    #---------Spawn Object-------------------
    if not GAME_OVER:
        if rd.randint(0,15) == 0:
            OBJECTS.append(spawn_img(FRUITS,BOMB,SPEED))
            
        #---------Update objects, check collision, etc---------------- 
        for obj in OBJECTS[:]:
            obj.move()
            obj.draw(frame)
            if finger and obj.collide(*finger):
                result = obj.on_slice()
                if result == "GAME_OVER":
                    bomb_sound.play()
                    LIVES -= 1
                    OBJECTS.remove(obj)
                    if LIVES <= 0:
                        GAME_OVER = True
                        if SCORE > HIGHSCORE:
                            HIGHSCORE = SCORE
                            with open('D:/language/mediapipe/mp_env/Fruit_Ninja/assets/HighScore.json','w') as f:
                                json.dump({'HighScore':HIGHSCORE},f)
                else:
                    slice_sound.play()
                    SCORE +=1
                    OBJECTS.remove(obj)
            elif obj.y > frame.shape[0]:
                OBJECTS.remove(obj)
                
    #-------------Putting The Level Name on Screen----------------- 
    Level = 'Level:Easy' if SPEED < 10  else 'Level:Medium' if (SPEED >=10 and SPEED < 20) else 'Level:Hard'
    cv2.rectangle(frame,(15,10),(180,100),(0,0,255),-1,cv2.LINE_AA)
    cv2.putText(frame,Level,(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    cv2.putText(frame,f'Lives:{LIVES}',(20,65),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),1)
    cv2.putText(frame,f'Score:{SCORE}',(20,85),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,225,0),1)
    
    if GAME_OVER:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (800, 600), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)

        cv2.putText(frame, "GAME OVER", (240, 100),
                    cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)
        
        #HighScore
        cv2.rectangle(frame, (300, 180), (500, 230), (128, 128,128), -1)
        cv2.putText(frame, f"Highscore : {HIGHSCORE}", (310, 210),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        #Score
        cv2.rectangle(frame, (300, 250), (500, 300), (255, 0, 0), -1)
        cv2.putText(frame, f"SCORE : {SCORE}", (310, 285),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # START button
        cv2.rectangle(frame, (300, 320), (500, 370), (0, 255, 0), -1)
        cv2.putText(frame, "START", (350, 355),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

        # END button
        cv2.rectangle(frame, (300, 390), (500, 440), (0, 0, 255), -1)
        cv2.putText(frame, "END", (370, 425),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    
    #----------Displaying the feed------------         
    cv2.imshow("Fruit Ninja",frame)
    if cv2.waitKey(1) == ord('q'):
        break
    if FRAME >= 400:
        SPEED += 1
        FRAME = 0
        FRUITS = [
            load_img(f"assets/{rd.choice(Apple)}"),load_img(f"assets/{rd.choice(Banana)}"),
            load_img(f"assets/{rd.choice(Melon)}")]
        BOMB = load_img(f"assets/{rd.choice(Bomb)}")
    FRAME += 1
    
Cap.release()
cv2.destroyAllWindows()