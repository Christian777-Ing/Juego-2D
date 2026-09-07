import pygame as pg
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.width = 10
        self.height = 10
        self.speed = 10
        self.damage = 25

        self.rect = pg.Rect(x, y, self.width, self.height)
        # Calcular la dirección del disparo
        dx = target_x - x
        dy = target_y - y
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            self.direccion_x = dx / distancia
            self.direccion_y = dy / distancia
        else:
            self.direccion_x = 0
            self.direccion_y = 0

    def actualizar(self):
        # Mover la bala en la dirección calculada
        self.rect.x += self.direccion_x * self.speed
        self.rect.y += self.direccion_y * self.speed

    def dibujar(self, screen):
        pg.draw.rect(screen, (255, 220, 50), self.rect)  # Yellow color for the bullet