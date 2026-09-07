import pygame

from src.player import Player
from src.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Survivor 2D")
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2)  # posicion inicial del jugador en el centro de la pantalla
        self.enemies= [Enemy(100, 100), Enemy(700, 100), Enemy(100, 500)]  # Lista de enemigos con posiciones iniciales

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def actualizar(self):
        self.player.actualizar(self.screen)

        for enemy in self.enemies:
            enemy.actualizar(self.player)  # Actualizar la posición del enemigo hacia el jugador

        self.detectar_colisiones()

    def detectar_colisiones(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.health -= enemy.damage  # Reducir la salud del jugador al colisionar con un enemigo
                if self.player.health < 0:
                    self.player.health = 0  # Evitar que la salud sea negativa
                # Mover al enemigo hacia atrás al colisionar con el jugador
                if enemy.rect.x < self.player.rect.x:
                    enemy.rect.x -= 20
                else:
                    enemy.rect.x += 20

    def barra_de_vida(self):
        # Dibujar la barra de vida del jugador
        health_bar_width = 200
        health_bar_height = 20

        x=20
        y=20

        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, health_bar_width, health_bar_height))
        health_width = (self.player.health / 100) * health_bar_width
        pygame.draw.rect(self.screen, (50, 200, 50), (x, y, health_width, health_bar_height))
 

    def dibujar(self):
        self.screen.fill((20, 20, 20))  # Fill the screen with a dark gray color
        self.player.dibujar(self.screen)
        for enemy in self.enemies:
            enemy.dibujar(self.screen)
        self.barra_de_vida()
        pygame.display.flip()

    def ejecutar(self):
        while self.running:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()