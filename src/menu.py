import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width= screen.get_width()
        self.height = screen.get_height()

        self.font_titulo = pygame.font.Font(None, 80)
        self.font_boton = pygame.font.Font(None, 50)
        self.font_ranking= pygame.font.Font(None, 35)

        self.opciones = ["Jugar","Continuar","Ranking", "Ajustes", "Salir"]

        self.seleccion = 0  # Opción seleccionada actualmente
        self.mostrar_Ranking= False
        self.ranking=[]

        self.enterirng_jugador=False
        self.nombre_jugador=""

        self.mostrar_Ajustes = False
        self.opcion_ajuste = 0  # 0 = Música, 1 = Sonidos
        self.volumen_musica = 0.5
        self.volumen_sonidos = 0.5
        self.musica_activada = True
        self.sonidos_activados = True

    def abrir_Ajustes(self):
        self.mostrar_Ajustes = True

    def dibujar(self):

        if self.mostrar_Ranking:
            self.dibujar_Ranking()

        elif self.enterirng_jugador:
            self.dibujar_nombre_pantalla()

        else:
            self.screen.fill((20, 20, 20))

            titulo = self.font_titulo.render(
                "SURVIVOR 2D",
                True,
                (255, 255, 255)
            )

            titulo_rect = titulo.get_rect(
                center=(self.width // 2, 120)
            )

            self.screen.blit(titulo, titulo_rect)

            for index, opcion in enumerate(self.opciones):

                if index == self.seleccion:
                    color = (255, 220, 50)
                else:
                    color = (255, 255, 255)

                texto = self.font_boton.render(
                    opcion,
                    True,
                    color
                )

                texto_rect = texto.get_rect(
                    center=(self.width // 2, 250 + index * 70)
                )

                self.screen.blit(texto, texto_rect)

    def dibujar_nombre_pantalla(self):

        self.screen.fill((20, 20, 20))

        # Título
        titulo = self.font_titulo.render(
            "INGRESA TU NOMBRE",
            True,
            (255, 255, 255)
        )

        titulo_rect = titulo.get_rect(
            center=(self.width // 2, 150)
        )

        self.screen.blit(titulo, titulo_rect)

        # Nombre ingresado
        nombre_texto = self.font_titulo.render(
            self.nombre_jugador + "_",
            True,
            (255, 220, 50)
        )

        nombre_rect = nombre_texto.get_rect(
            center=(self.width // 2, 280)
        )

        self.screen.blit(nombre_texto, nombre_rect)

        # Instrucción
        instruccion = self.font_ranking.render(
            "ENTER = comenzar",
            True,
            (180, 180, 180)
        )

        instruccion_rect = instruccion.get_rect(
            center=(self.width // 2, 400)
        )

        self.screen.blit(instruccion, instruccion_rect)

        
        

    def dibujar_Ranking(self):

        # Limpiar la pantalla
        self.screen.fill((20, 20, 20))

        # Título
        titulo = self.font_titulo.render(
            "RANKING",
            True,
            (255, 255, 255)
        )

        titulo_rect = titulo.get_rect(
            center=(self.width // 2, 80)
        )

        self.screen.blit(titulo, titulo_rect)

        # Mostrar ranking
        if not self.ranking:

            texto = self.font_ranking.render(
                "No hay partidas registradas",
                True,
                (255, 255, 255)
            )

            texto_rect = texto.get_rect(
                center=(self.width // 2, 250)
            )

            self.screen.blit(texto, texto_rect)

        else:

            for posicion, player in enumerate(self.ranking, start=1):

                name = player[0]
                score = player[1]
                nivel = player[2]

                texto = self.font_ranking.render(
                    f"{posicion}. {name}    Score: {score}    Nivel: {nivel}",
                    True,
                    (255, 255, 255)
                )

                texto_rect = texto.get_rect(
                    center=(self.width // 2, 160 + posicion * 45)
                )

                self.screen.blit(texto, texto_rect)

        # Texto para regresar
        back_text = self.font_ranking.render(
            "Presiona ESC para volver",
            True,
            (180, 180, 180)
        )

        back_rect = back_text.get_rect(
            center=(self.width // 2, self.height - 50)
        )

        self.screen.blit(back_text, back_rect)

    def dibujar_Ajustes(self):
        self.screen.fill((20, 20, 20))

        titulo = self.font_titulo.render("AJUSTES", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.width // 2, 100))
        self.screen.blit(titulo, titulo_rect)

        opciones_ajuste = [
            ("Música", self.musica_activada, self.volumen_musica),
            ("Sonidos", self.sonidos_activados, self.volumen_sonidos),
        ]

        for i, (nombre, activo, volumen) in enumerate(opciones_ajuste):
            seleccionado = (i == self.opcion_ajuste)
            color_texto = (255, 220, 50) if seleccionado else (255, 255, 255)

            y = 220 + i * 100

            # Nombre + estado ON/OFF
            estado = "ON" if activo else "OFF"
            texto = self.font_boton.render(f"{nombre}: {estado}", True, color_texto)
            texto_rect = texto.get_rect(center=(self.width // 2, y))
            self.screen.blit(texto, texto_rect)

            # Barra de volumen
            barra_ancho = 300
            barra_alto = 25
            barra_x = self.width // 2 - barra_ancho // 2
            barra_y = y + 40

            # Fondo de la barra
            pygame.draw.rect(
                self.screen,
                (60, 60, 60),
                (barra_x, barra_y, barra_ancho, barra_alto),
                border_radius=6
            )

            # Relleno según el volumen
            relleno_ancho = int(barra_ancho * volumen)
            if relleno_ancho > 0:
                color_relleno = (255, 220, 50) if seleccionado else (100, 180, 255)
                pygame.draw.rect(
                    self.screen,
                    color_relleno,
                    (barra_x, barra_y, relleno_ancho, barra_alto),
                    border_radius=6
                )

            # Borde de la barra
            borde_color = (255, 255, 255) if seleccionado else (120, 120, 120)
            pygame.draw.rect(
                self.screen,
                borde_color,
                (barra_x, barra_y, barra_ancho, barra_alto),
                width=2,
                border_radius=6
            )

            # Porcentaje
            porcentaje_texto = self.font_ranking.render(f"{int(volumen * 100)}%", True, (255, 255, 255))
            porcentaje_rect = porcentaje_texto.get_rect(midleft=(barra_x + barra_ancho + 15, barra_y + barra_alto // 2))
            self.screen.blit(porcentaje_texto, porcentaje_rect)

        instrucciones = self.font_ranking.render(
            "↑↓ seleccionar   ←→ volumen   ENTER activar/desactivar   ESC volver",
            True,
            (180, 180, 180)
        )
        instrucciones_rect = instrucciones.get_rect(center=(self.width // 2, self.height - 60))
        self.screen.blit(instrucciones, instrucciones_rect)


    def manejar_eventos(self, event):

        if self.mostrar_Ajustes:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mostrar_Ajustes = False

                elif event.key == pygame.K_UP:
                    self.opcion_ajuste = (self.opcion_ajuste - 1) % 2

                elif event.key == pygame.K_DOWN:
                    self.opcion_ajuste = (self.opcion_ajuste + 1) % 2

                elif event.key == pygame.K_LEFT:
                    if self.opcion_ajuste == 0:
                        self.volumen_musica = max(0.0, self.volumen_musica - 0.1)
                        pygame.mixer.music.set_volume(self.volumen_musica)
                    else:
                        self.volumen_sonidos = max(0.0, self.volumen_sonidos - 0.1)

                elif event.key == pygame.K_RIGHT:
                    if self.opcion_ajuste == 0:
                        self.volumen_musica = min(1.0, self.volumen_musica + 0.1)
                        pygame.mixer.music.set_volume(self.volumen_musica)
                    else:
                        self.volumen_sonidos = min(1.0, self.volumen_sonidos + 0.1)

                elif event.key == pygame.K_RETURN:
                    if self.opcion_ajuste == 0:
                        self.musica_activada = not self.musica_activada
                        if self.musica_activada:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    else:
                        self.sonidos_activados = not self.sonidos_activados
            return None
        
        if self.mostrar_Ranking:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mostrar_Ranking = False
            return None

        if self.enterirng_jugador:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.nombre_jugador.strip() != "":
                        self.enterirng_jugador = False
                        return "Jugar"
                elif event.key == pygame.K_BACKSPACE:
                    self.nombre_jugador = self.nombre_jugador[:-1]

                else:
                    if len(self.nombre_jugador) < 15:
                        self.nombre_jugador += event.unicode

            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.seleccion = (
                    self.seleccion - 1
                ) % len(self.opciones)
            elif event.key == pygame.K_DOWN:
                self.seleccion = (
                    self.seleccion + 1
                ) % len(self.opciones)
            elif event.key == pygame.K_RETURN:
                if self.opciones[self.seleccion] == "Jugar":
                    self.nombre_jugador = ""
                    self.enterirng_jugador = True
                    return None
                elif self.opciones[self.seleccion] == "Continuar":
                    return "Continuar"

                elif self.opciones[self.seleccion] == "Ranking":
                    return "Ranking"

                elif self.opciones[self.seleccion ]== "Ajustes":
                    return "Ajustes"

                elif self.opciones[self.seleccion] == "Salir":
                    return "Salir"
        return None

    def abrir_Ranking(self, ranking):
        self.ranking= ranking
        self.mostrar_Ranking= True


        