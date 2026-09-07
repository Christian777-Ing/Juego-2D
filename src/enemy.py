import pygame as pg
import math

class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40


        self.speed = 2
        self.health = 50
        self.damage = 10


        self.rect = pg.Rect(x, y, self.width, self.height)

    def mover_hacia_jugador(self, jugador):
        # Calcular la dirección hacia el jugador
        dx = jugador.rect.centerx - self.rect.centerx
        dy = jugador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

            # Mover al enemigo hacia el jugador
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def actualizar(self, jugador):
        self.mover_hacia_jugador(jugador)

    def dibujar(self, screen):
        pg.draw.rect(screen, (0, 255, 0), self.rect)  # Green color for the enemy