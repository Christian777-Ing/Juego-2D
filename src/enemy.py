import pygame as pg
import math

class Enemy:
    def __init__(self, x, y, enemy_type="Zombie"):

        enemy_types={
            "Zombie":{ "health": 50, "damage": 10, "speed": 2, "xp": 10, "score": 100},
            "Skeleton":{ "health": 30, "damage": 8, "speed": 4, "xp": 15, "score": 150},
            "Golem":{ "health": 120, "damage": 20 , "speed": 1, "xp": 30, "score": 300},
        }

        data=enemy_types[enemy_type]# Selecciona el tipo de enemigo que deseas crear
        self.type=enemy_type

        self.width = 40
        self.height = 40

        self.health = data["health"]
        self.max_health = self.health
        self.damage = data["damage"]
        self.speed = data["speed"]
        self.xp_ganada= data["xp"]
        self.score_ganada = data["score"]


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
        if self.type == "Zombie":
            color = (0, 255, 0)  # Verde para Zombie
        elif self.type == "Skeleton":
            color = (255, 255, 255)  # Blanco para Skeleton
        else:  # Golem
            color = (128, 128, 128)  # Gris para Golem
        pg.draw.rect(screen, color, self.rect)  # Dibujar el enemigo con el color correspondiente

        barra_vida_width = self.width
        barra_vida_height = 5
        vida_porcentaje = self.health / self.max_health
        vida_width = int(barra_vida_width * vida_porcentaje)
        pg.draw.rect(screen, (80, 80, 80), (self.rect.x, self.rect.y - 10, barra_vida_width, barra_vida_height))
        pg.draw.rect(screen, (255, 0, 0), (self.rect.x , self.rect.y - 10, vida_width, barra_vida_height))

