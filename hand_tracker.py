import cv2
import mediapipe as mp

class HandTracker():
    def __init__(self):
        self.hand = mp.solutions.hands.Hands(static_image_mode=False,max_num_hands=1,model_complexity=1,
                                 min_detection_confidence=0.7,min_tracking_confidence=0.7)
    def get_finger(self,frame):
        if frame is None:
            return None
        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = self.hand.process(rgb)
        if result.multi_hand_landmarks:
            H,W,_ = frame.shape
            lm = result.multi_hand_landmarks[0].landmark[8]
            indx,indy = int(lm.x*W),int(lm.y*H)
            return (indx,indy)
        return None