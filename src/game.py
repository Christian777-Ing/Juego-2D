import pygame
import random

from src.player import Player
from src.enemy import Enemy
from src.bullet import Bullet
from src.weapon import Weapon


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Survivor 2D")
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_over = False

        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)

        self.crear_juego()


    def crear_juego(self):

        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2)  # posicion inicial del jugador en el centro de la pantalla
        self.enemies= [Enemy(100, 100), Enemy(700, 100), Enemy(100, 500)]  # Lista de enemigos con posiciones iniciales
        self.bullets = []  # Lista para almacenar las balas disparadas
        self.weapon = Weapon(self.player)  # Crear un objeto Weapon para el jugador

        self.score = 0
        self.experiencia = 0
        self.level = 1
        self.experiencia_para_siguiente_nivel = 100  # Experiencia necesaria para subir de nivel

        self.last_enemy_spawn_time = pygame.time.get_ticks()  # Tiempo del último spawn de enemigo

        self.game_over = False  # Reiniciar el estado de game_over al crear un nuevo juego

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and not self.game_over:
                    self.weapon.recargar() 

                if self.game_over:
                    if event.key == pygame.K_r:
                        self.crear_juego()  # Reiniciar el juego al presionar 'R' cuando el juego ha terminado
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False  # Salir del juego al presionar 'ESC' cuando el juego ha terminado

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.weapon.is_reloading():  # Botón izquierdo del ratón
                    if self.weapon.disparar():  # Intentar disparar
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, mouse_x, mouse_y)
                        bullet.damage = self.weapon.damage  # Asignar el daño de la bala según el arma
                        self.bullets.append(bullet)  # Agregar la bala a la lista de balas


    def actualizar(self):

        if self.game_over:
            return  # No actualizar el juego si ha terminado
        
        self.player.actualizar(self.screen)

        for enemy in self.enemies:
            enemy.actualizar(self.player)  # Actualizar la posición del enemigo hacia el jugador

        for bullet in self.bullets:
            bullet.actualizar()  # Actualizar la posición de la bala

        self.weapon.actualizar_balas()  # Actualizar el estado del arma
        self.spawn_enemigos_periodicamente()

        self.detectar_colisiones()

        if self.player.health <= 0:
            self.game_over = True 

    def detectar_colisiones(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if enemy.atacar(self.player):
                    self.player.health -= enemy.damage  # Reducir la salud del jugador al colisionar con un enemigo

                if enemy.rect.x < self.player.rect.x:
                    enemy.rect.x -= 20
                else:
                    enemy.rect.x += 20

                if self.player.health < 0:
                    self.player.health = 0  # Evitar que la salud sea negativa

        for bullet in self.bullets[:]:  # Iterar sobre una copia de la lista de balas
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= bullet.damage  # Reducir la salud del enemigo al colisionar con una bala
                    if enemy.health <= 0:
                        self.experiencia += enemy.xp_ganada  
                        self.score += enemy.score_ganada  
                        self.enemies.remove(enemy)  
                        self.chechear_subida_nivel()  
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break  # Salir del bucle de enemigos después de una colisión

    def chechear_subida_nivel(self):
        while self.experiencia >= self.experiencia_para_siguiente_nivel:
            self.experiencia -= self.experiencia_para_siguiente_nivel
            self.level += 1

            self.weapon.damage += 5  # Incrementar el daño del arma al subir de nivel
            self.player.health= min(self.player.health + 10, self.player.max_health)  # Incrementar la salud del jugador al subir de nivel, sin exceder la salud máxima

            self.experiencia_para_siguiente_nivel = int(self.experiencia_para_siguiente_nivel * 1.5)  # Incrementar la experiencia necesaria para el siguiente nivel

    def spawn_enemigo(self):

        side= random.randint(0, 3) 
        if side ==0:
            x= random.randint(0, self.WIDTH-40)
            y= -40
        elif side ==1:
            x= self.WIDTH
            y= random.randint(0, self.HEIGHT-40)
        elif side ==2:
            x= random.randint(0, self.WIDTH-40)
            y= self.HEIGHT
        else:
            x= -40
            y= random.randint(0, self.HEIGHT-40)

        if self.level < 3:
            enemy_type = random.choice(["Zombie", "Skeleton", "Zombie"])  # Mayor probabilidad de Zombies en niveles bajos
        else:
            enemy_type = random.choice(["Zombie", "Skeleton", "Golem"])  # Mayor variedad de enemigos en niveles más altos

        enemy = Enemy(x, y, enemy_type)
        self.enemies.append(enemy)  # Agregar el nuevo enemigo a la lista de enemigos

    def spawn_enemigos_periodicamente(self):
        current_time = pygame.time.get_ticks()
        spawn_interval = max(2000 - (self.level - 1) * 100, 500)  # Reducir el intervalo de spawn a medida que sube de nivel, con un mínimo de 500 ms

        if current_time - self.last_enemy_spawn_time >= spawn_interval:
            self.spawn_enemigo()
            self.last_enemy_spawn_time = current_time

    def barra_de_vida(self):
        # Dibujar la barra de vida del jugador
        health_bar_width = 200
        health_bar_height = 20

        x=20
        y=20

        pygame.draw.rect(self.screen, (80, 80, 80), (x, y, health_bar_width, health_bar_height))
        health_width = (self.player.health / 100) * health_bar_width
        pygame.draw.rect(self.screen, (50, 200, 50), (x, y, health_width, health_bar_height))

    def dibujar_game_over(self):

        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(100)  # Transparencia del overlay
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        title_text = self.font.render("Game Over", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.WIDTH // 2, 220))
        self.screen.blit(title_text, title_rect)

        texto_reiniciar = self.small_font.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
        reiniciar_rect = texto_reiniciar.get_rect(center=(self.WIDTH // 2, 300))
        self.screen.blit(texto_reiniciar, reiniciar_rect)

        salida_texto = self.small_font.render("Presiona 'ESC' para salir", True, (255, 255, 255))
        salida_rect = salida_texto.get_rect(center=(self.WIDTH // 2, 350))
        self.screen.blit(salida_texto, salida_rect)

    def dibujar_municion(self):
        ammo_text = self.small_font.render(f"Munición: {self.weapon.ammo}/{self.weapon.cargador}", True, (255, 255, 255))
        self.screen.blit(ammo_text, (20, 50)) 

        if self.weapon.is_reloading():
            reload_text = self.small_font.render("Recargando...", True, (255, 0, 0))
            self.screen.blit(reload_text, (20, 80))  # Mostrar el texto de recarga debajo de la munición

    def dibujar_estadisticas(self):
        score_text = self.small_font.render(f"Experiencia: {self.experiencia}/{self.experiencia_para_siguiente_nivel}  Nivel: {self.level}", True, (255, 255, 255))
        level_text = self.small_font.render(f"Nivel: {self.level}", True, (255, 255, 255))
        xp_text = self.small_font.render(f"Experiencia: {self.experiencia}/{self.experiencia_para_siguiente_nivel}", True, (255, 255, 255))

        self.screen.blit(score_text, (20, 50))  # Mostrar la experiencia y el nivel debajo de la munición
        self.screen.blit(level_text, (20, 80))
        self.screen.blit(xp_text, (20, 110))


    def dibujar(self):
        self.screen.fill((20, 20, 20))  # Fill the screen with a dark gray color
        self.player.dibujar(self.screen)
        for enemy in self.enemies:
            enemy.dibujar(self.screen)
        for bullet in self.bullets:
            bullet.dibujar(self.screen)

        self.barra_de_vida()
        self.dibujar_municion()
        self.dibujar_estadisticas()

        if self.game_over:
            self.dibujar_game_over()

        pygame.display.flip()

    def ejecutar(self):
        while self.running:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        pygame.quit()