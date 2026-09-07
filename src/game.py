import pygame
import random

from src.player import Player
from src.enemy import Enemy
from src.bullet import Bullet
from src.weapon import Weapon
from src.database import Database
from src.menu import Menu




class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Survivor 2D")
        self.clock = pygame.time.Clock()
        self.running = True

        self.menu= Menu(self.screen)
        self.in_menu= True

        self.game_over = False
        self.database = Database() 

        self.pausa=False
        self.mostrar_guardado = False
        self.tiempo_guardado = 0

        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)
        self.player_name = ""

        self.crear_juego()


    def crear_juego(self):

        self.player = Player(self.WIDTH // 2, self.HEIGHT // 2) #Posición inicial del jugador en el centro de la pantalla
        self.score_saved= False  # Variable para controlar si la puntuación ya se ha guardado

        self.enemies= [Enemy(100, 100), Enemy(700, 100), Enemy(100, 500)]  # Lista de enemigos con posiciones iniciales
        self.bullets = []  # Lista para almacenar las balas disparadas
        self.weapon = Weapon(self.player)  # Crear un objeto Weapon para el jugador

        self.score = 0
        self.experiencia = 0
        self.level = 1
        self.experiencia_para_siguiente_nivel = 100  # Experiencia necesaria para subir de nivel

        self.last_enemy_spawn_time = pygame.time.get_ticks()  # Tiempo del último spawn de enemigo

        self.game_over = False  # Reiniciar el estado de game_over al crear un nuevo juego
        self.pausa= False
        self.partida_guardada = False

    def cargar_partida(self):

        partida = self.database.load_game()

        if partida is None:
            return False

        (
            self.player_name,
            player_x,
            player_y,
            health,
            self.score,
            self.experiencia,
            self.level,
            self.experiencia_para_siguiente_nivel,
            weapon_damage,
            ammo
        ) = partida

        # CARGAR JUGADOR
        self.player = Player(player_x, player_y)

        self.player.health = health

        # CARGAR ARMA
        self.weapon = Weapon(self.player)
        self.weapon.damage = weapon_damage
        self.weapon.ammo = ammo

        # CARGAR ENEMIGOS
        self.enemies = []
        enemigos_guardados = self.database.load_enemies()
        for enemy_data in enemigos_guardados:
            enemy_type, x, y, health = enemy_data
            enemy = Enemy(
                x,
                y,
                enemy_type
            )
            enemy.health = health
            self.enemies.append(enemy)

        # BALAS
        self.bullets = []

        self.score_saved = False
        self.game_over = False
        self.pausa = False
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.partida_guardada = True 
        return True

    def guardar_partida(self):

        self.database.save_game(
            self.player_name,
            self.player.rect.x,
            self.player.rect.y,
            self.player.health,
            self.score,
            self.experiencia,
            self.level,
            self.experiencia_para_siguiente_nivel,
            self.weapon.damage,
            self.weapon.ammo,
            self.enemies
        )



    def manejar_eventos(self, event):

        if event.type == pygame.KEYDOWN:

            # Pausar / continuar
            if event.key == pygame.K_p and not self.game_over:
                self.pausa = not self.pausa

            if event.key == pygame.K_g and self.pausa and not self.game_over:
                self.guardar_partida()
                self.mostrar_guardado = True
                self.tiempo_guardado = pygame.time.get_ticks()
                self.partida_guardada = True

            if event.key == pygame.K_m and self.pausa and self.partida_guardada:
                self.in_menu = True
                self.pausa = False
                self.mostrar_guardado = False

            if event.key == pygame.K_r and not self.game_over:
                self.weapon.recargar()

            if self.game_over:

                if event.key == pygame.K_r:
                    self.crear_juego()

                elif event.key == pygame.K_ESCAPE:
                    self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and not self.weapon.is_reloading():

                if self.weapon.disparar():

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    bullet = Bullet(
                        self.player.rect.centerx,
                        self.player.rect.centery,
                        mouse_x,
                        mouse_y
                    )

                    bullet.damage = self.weapon.damage

                    self.bullets.append(bullet)


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
            if not self.score_saved:
                self.database.save_scores(
                    self.player_name,
                    self.score,
                    self.level
                )
                self.database.delete_saved_game()
                self.score_saved = True

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

    def dibujar_pausa(self):

        # Fondo oscuro transparente
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        self.screen.blit(overlay, (0, 0))

        # TÍTULO PAUSA
        pausa_text = self.font.render(
            "PAUSA",
            True,
            (255, 255, 255)
        )
        pausa_rect = pausa_text.get_rect(
            center=(self.WIDTH // 2, 180)
        )

        self.screen.blit(pausa_text, pausa_rect)

        # OPCIONES
        continuar = self.small_font.render(
            "P = Continuar",
            True,
            (255, 255, 255)
        )
        continuar_rect = continuar.get_rect(
            center=(self.WIDTH // 2, 270)
        )

        self.screen.blit(continuar, continuar_rect)

        guardar = self.small_font.render(
            "G = Guardar partida",
            True,
            (255, 220, 50)
        )

        guardar_rect = guardar.get_rect(
            center=(self.WIDTH // 2, 320)
        )

        self.screen.blit(guardar, guardar_rect)


        # MENSAJE PARTIDA GUARDADA
        if self.mostrar_guardado:
            # Mostrar durante 2 segundos
            if pygame.time.get_ticks() - self.tiempo_guardado < 2000:
                guardado = self.small_font.render(
                    "PARTIDA GUARDADA",
                    True,
                    (50, 255, 100)
                )
                guardado_rect = guardado.get_rect(
                    center=(self.WIDTH // 2, 390)
                )

                self.screen.blit(guardado, guardado_rect)

            else:
                self.mostrar_guardado = False

        
        if self.partida_guardada:
            volver = self.small_font.render(
                "M = Volver al menú principal",
                True,
                (100, 200, 255)
            )
        else:
            volver = self.small_font.render(
                "Guarda con G para poder salir al menú",
                True,
                (150, 150, 150)
            )

        volver_rect = volver.get_rect(center=(self.WIDTH // 2, 450))
        self.screen.blit(volver, volver_rect)



        
    def mostrar_ranking(self):
        ranking= self.database.get_Raking()
        print("Ranking de puntuaciones:")
        for posiciones, player in enumerate(ranking, start=1):
            print(f"{posiciones}. {player[0]} - Puntuación: {player[1]} - Nivel: {player[2]}")
        

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


    def ejecutar(self):

        while self.running:
            # EVENTOS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.in_menu:
                    opcion_seleccionada = self.menu.manejar_eventos(event)
                    if opcion_seleccionada == "Jugar":
                        self.player_name = self.menu.nombre_jugador
                        self.database.delete_saved_game()
                        self.crear_juego()
                        self.in_menu = False

                    elif opcion_seleccionada == "Continuar":
                        if self.cargar_partida():
                            self.in_menu = False
                        else:
                            print("No existe una partida guardada")

                    elif opcion_seleccionada == "Ranking":
                        ranking = self.database.get_Raking()
                        self.menu.abrir_Ranking(ranking)

                    elif opcion_seleccionada == "Ajustes":
                        self.menu.abrir_Ajustes()

                    elif opcion_seleccionada == "Salir":
                        self.running = False

                else:
                    self.manejar_eventos(event)

            # ACTUALIZAR JUEGO
            if not self.in_menu and not self.pausa:
                self.actualizar()

            # DIBUJAR
            if self.in_menu:
                if self.menu.mostrar_Ranking:
                    self.menu.dibujar_Ranking()
                elif self.menu.mostrar_Ajustes:
                    self.menu.dibujar_Ajustes()
                else:
                    self.menu.dibujar()

            else:
                self.dibujar()
                if self.pausa:
                    self.dibujar_pausa()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()