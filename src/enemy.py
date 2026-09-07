import pygame as pg
import math

class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 40


        self.speed = 2
        self.health = 50
        self.damage = 10

        #Tiempo entre ataques
        self.attack_cooldown = 1000  # Tiempo en milisegundos
        self.last_attack_time = 0  # Tiempo del último ataque



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

    def atacar(self, jugador):
        current_time = pg.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            return True  # El enemigo puede atacar
        return False  # El enemigo no puede atacar aún

    def actualizar(self, jugador):
        self.mover_hacia_jugador(jugador)

    def dibujar(self, screen):
        pg.draw.rect(screen, (0, 255, 0), self.rect)  # Green color for the enemy