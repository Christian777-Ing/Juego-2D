import pygame as pg

class Player:
    def __init__(self, x, y):
        self.width = 50
        self.height = 50

        self.x=x
        self.y=y

        self.speed = 5
        self.max_health = 100
        self.health = self.max_health

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)


    def movimiento(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pg.K_UP]:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed

    def actualizar(self, screen):
        self.movimiento()

        self.rect.clamp_ip(screen.get_rect()) 

    def dibujar(self, screen):
        pg.draw.rect(screen, (255, 0, 0), self.rect)  # Red color for the player