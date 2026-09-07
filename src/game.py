import pygame

from src.player import Player

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

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def actualizar(self):
        self.player.actualizar(self.screen)

    def dibujar(self):
        self.screen.fill((20, 20, 20))  # Fill the screen with a dark gray color
        self.player.dibujar(self.screen)
        pygame.display.flip()

    def ejecutar(self):
        while self.running:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()