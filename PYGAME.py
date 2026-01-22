# ===============================
# BATTLE ROYALE 3D – REFINED EDITION
# ===============================

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math, random, time
from dataclasses import dataclass

WIDTH, HEIGHT = 1400, 800
FPS = 60

# -------------------------------
# DATA CLASSES
# -------------------------------
@dataclass
class Player:
    pos: np.ndarray
    vel: np.ndarray
    color: tuple
    name: str
    health: float = 100
    ammo: int = 60
    angle: float = 0
    alive: bool = True
    shield: float = 0
    kills: int = 0
    grounded: bool = True

@dataclass
class Bullet:
    pos: np.ndarray
    vel: np.ndarray
    owner: str
    life: float = 2.5

@dataclass
class Particle:
    pos: np.ndarray
    vel: np.ndarray
    color: tuple
    life: float

# -------------------------------
# CAMERA
# -------------------------------
class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 18.0, 28.0])
        self.target = np.zeros(3)

    def update(self, target):
        self.target = self.target * 0.9 + target * 0.1
        angle = time.time() * 0.2
        self.pos = self.target + np.array([
            math.cos(angle) * 28,
            18,
            math.sin(angle) * 28
        ])

# -------------------------------
# MAIN GAME
# -------------------------------
class BattleRoyale3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Battle Royale 3D – Refined Edition")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        gluPerspective(70, WIDTH / HEIGHT, 0.1, 200)

        self.clock = pygame.time.Clock()
        self.camera = Camera()

        self.players = self.spawn_players()
        self.bullets = []
        self.particles = []

        self.zone_radius = 35

    # ---------------------------
    def spawn_players(self):
        colors = [(0,1,0),(1,0,0),(0,0.5,1),(1,1,0)]
        names = ["VIPER","PHOENIX","FROST","REAPER"]
        players = []

        for i in range(4):
            angle = i * (math.pi/2)
            players.append(Player(
                pos=np.array([math.cos(angle)*15,0.5,math.sin(angle)*15]),
                vel=np.zeros(3),
                color=colors[i],
                name=names[i],
                angle=angle+math.pi
            ))
        return players

    # ---------------------------
    def shoot(self, player, target):
        if player.ammo <= 0: return
        direction = target - player.pos
        direction[1] = 0
        direction /= np.linalg.norm(direction)
        self.bullets.append(Bullet(
            pos=player.pos + direction,
            vel=direction * 0.9,
            owner=player.name
        ))
        player.ammo -= 1

    # ---------------------------
    def update(self, dt):
        # AI
        for ai in self.players[1:]:
            if not ai.alive: continue
            target = self.players[0]
            if random.random() < 0.02:
                self.shoot(ai, target.pos)
            move = target.pos - ai.pos
            move[1] = 0
            ai.pos += (move/np.linalg.norm(move)) * dt * 0.08

        # Bullets
        for b in self.bullets[:]:
            b.pos += b.vel
            b.life -= dt
            if b.life <= 0:
                self.bullets.remove(b)
                continue

            for p in self.players:
                if p.alive and p.name != b.owner:
                    if np.linalg.norm(p.pos - b.pos) < 0.8:
                        p.health -= 15
                        if p.health <= 0:
                            p.alive = False
                        self.bullets.remove(b)
                        break

        # Camera
        alive = [p.pos for p in self.players if p.alive]
        if alive:
            self.camera.update(np.mean(alive, axis=0))

    # ---------------------------
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(*self.camera.pos, *self.camera.target, 0,1,0)

        # Ground
        glColor3f(0.4,0.35,0.3)
        glBegin(GL_QUADS)
        glVertex3f(-50,0,-50)
        glVertex3f(50,0,-50)
        glVertex3f(50,0,50)
        glVertex3f(-50,0,50)
        glEnd()

        # Zone
        glColor3f(1,0,0)
        glBegin(GL_LINE_LOOP)
        for i in range(60):
            a = i/60*2*math.pi
            glVertex3f(math.cos(a)*self.zone_radius,0.1,math.sin(a)*self.zone_radius)
        glEnd()

        # Players
        for p in self.players:
            if not p.alive: continue
            glPushMatrix()
            glTranslatef(*p.pos)
            glColor3fv(p.color)
            quad = gluNewQuadric()
            gluSphere(quad,0.6,16,16)
            gluDeleteQuadric(quad)
            glPopMatrix()

        # Bullets
        glPointSize(6)
        glBegin(GL_POINTS)
        glColor3f(1,1,0)
        for b in self.bullets:
            glVertex3fv(b.pos)
        glEnd()

        pygame.display.flip()

    # ---------------------------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 60

            for e in pygame.event.get():
                if e.type == QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
                    running = False
                if e.type == MOUSEBUTTONDOWN:
                    self.shoot(self.players[0], self.players[0].pos + np.array([math.cos(self.players[0].angle)*10,0,math.sin(self.players[0].angle)*10]))
                if e.type == MOUSEMOTION:
                    self.players[0].angle -= e.rel[0] * 0.004

            keys = pygame.key.get_pressed()
            p = self.players[0]
            if p.alive:
                if keys[K_w]:
                    p.pos += np.array([math.cos(p.angle),0,math.sin(p.angle)]) * dt * 4
                if keys[K_s]:
                    p.pos -= np.array([math.cos(p.angle),0,math.sin(p.angle)]) * dt * 4

            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    BattleRoyale3D().run()
