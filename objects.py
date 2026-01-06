import cv2
import random as rd
import numpy as np

class GameObject():
    def __init__(self,img,speed):
        self.img = img
        self.speed = speed
        self.x = rd.randint(50,750)
        self.y = 0
        self.radius = 40
        self.alive = True
    def move(self):
        self.y += self.speed
    def draw(self,frame):
        H,W,C = self.img.shape
        fH,fW,_ = frame.shape
        # Bounds check
        if self.x < 0 or self.y < 0:
            return
        if self.x + W > fW or self.y + H > fH:
            return
         # If PNG has alpha channel, blend with frame
        if C == 4:
            alpha = self.img[:, :, 3] / 255.0
            for c in range(3):  # only BGR channels
                frame[self.y:self.y+H, self.x:self.x+W, c] = (
                    alpha * self.img[:, :, c] + (1 - alpha) * frame[self.y:self.y+H, self.x:self.x+W, c]
                )
        else:
            frame[self.y:self.y+H, self.x:self.x+W] = self.img
        
    def collide(self,fx,fy):
        if fx is None or fy is None:
            return False

        cx = self.x + self.img.shape[1] // 2
        cy = self.y + self.img.shape[0] // 2

        return np.hypot(cx - fx, cy - fy) < self.radius
        
class FruitClass(GameObject):
    def on_slice(self):
        self.alive = False
        return 1


class BombClass(GameObject):
    def on_slice(self):
        self.alive = False
        return "GAME_OVER"     
        