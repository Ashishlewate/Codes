import cv2
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ======================
# CONFIGURATION
# ======================
WIDTH, HEIGHT = 1280, 800
MAX_SWORDS = 1000

class Sword:
    def __init__(self):
        self.pos = [random.uniform(-30, 30), random.uniform(-20, 20), random.uniform(-20, 20)]
        self.vel = [0, 0, 0]
        self.color = [1, 1, 1]
        self.offset = random.random() * 2 * math.pi 

    def update(self, target, gesture, active):
        if active:
            tx, ty, tz = target
            
            # --- SHAPE COMMANDS ---
            if gesture == "SQUARE": # 1: Fist
                side = 7.0
                edge = random.randint(0, 3)
                if edge == 0: tx += random.uniform(-side, side); ty += side
                elif edge == 1: tx += random.uniform(-side, side); ty -= side
                elif edge == 2: tx += side; ty += random.uniform(-side, side)
                else: tx -= side; ty += random.uniform(-side, side)
                self.color = [1.0, 0.1, 0.1] # Red

            elif gesture == "HEART": # 2: Thumb
                t = self.offset + pygame.time.get_ticks() * 0.002
                # Parametric Heart Formula
                hx = 16 * math.sin(t)**3
                hy = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                tx += hx * 0.5
                ty += hy * 0.5
                self.color = [1.0, 0.3, 0.6] # Pink

            elif gesture == "MAGIC": # 3: Two Fingers (Double Helix)
                t = self.offset + pygame.time.get_ticks() * 0.004
                tx += math.cos(t) * 6
                ty += math.sin(t) * 6
                tz += math.sin(t * 0.5) * 12
                self.color = [0.0, 0.8, 1.0] # Electric Blue

            elif gesture == "WALL": # 4: Four Fingers
                tx += random.uniform(-12, 12)
                ty += random.uniform(-10, 10)
                tz = -8
                self.color = [0.9, 0.9, 1.0] # White/Silver

            else: # 5: Five Fingers (Vortex)
                r = 10.0
                tx += math.cos(self.offset + pygame.time.get_ticks() * 0.002) * r
                ty += math.sin(self.offset + pygame.time.get_ticks() * 0.002) * r
                self.color = [0.3, 1.0, 0.4] # Emerald Green

            # --- PHYSICS ---
            dx, dy, dz = tx - self.pos[0], ty - self.pos[1], tz - self.pos[2]
            dist = math.sqrt(dx**2 + dy**2 + dz**2) + 0.1
            self.vel[0] += (dx / dist) * 0.25
            self.vel[1] += (dy / dist) * 0.25
            self.vel[2] += (dz / dist) * 0.25
        
        for i in range(3):
            self.pos[i] += self.vel[i]
            self.vel[i] *= 0.82 # High friction for crisp shapes

    def draw(self):
        glBegin(GL_LINES)
        glColor3f(*self.color)
        glVertex3f(self.pos[0], self.pos[1], self.pos[2])
        glColor3f(0, 0, 0)
        glVertex3f(self.pos[0]-self.vel[0]*4, self.pos[1]-self.vel[1]*4, self.pos[2]-self.vel[2]*4)
        glEnd()

# ======================
# GESTURE CLASSIFIER
# ======================
def get_gesture(landmarks):
    fingers = []
    # Thumb Detection
    if landmarks[4].x < landmarks[3].x: fingers.append("THUMB")
    # Finger Detection (Tips vs Joints)
    for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
        if landmarks[tip].y < landmarks[pip].y:
            fingers.append("FINGER")
    
    count = len(fingers)
    if count == 0: return "SQUARE"
    if count == 1 and "THUMB" in fingers: return "HEART"
    if count == 2: return "MAGIC"
    if count == 4: return "WALL"
    return "VORTEX"

# ======================
# EXECUTION ENGINE
# ======================
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE) # Glow effect
gluPerspective(45, (WIDTH/HEIGHT), 0.1, 100.0)
glTranslatef(0, 0, -45)

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
swords = [Sword() for _ in range(MAX_SWORDS)]
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); exit()

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = detector.detect(mp_img)

    h_target = [0,0,0]; h_active = False; gesture = "VORTEX"

    if result.hand_landmarks:
        h_active = True
        lms = result.hand_landmarks[0]
        gesture = get_gesture(lms)
        h_target = [(lms[9].x - 0.5) * 55, (0.5 - lms[9].y) * 45, 0]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Global rotation for 3D depth
    glPushMatrix()
    glRotatef(pygame.time.get_ticks() * 0.01, 0, 1, 0)
    for s in swords:
        s.update(h_target, gesture, h_active)
        s.draw()
    glPopMatrix()
    
    pygame.display.flip()
    clock.tick(60)