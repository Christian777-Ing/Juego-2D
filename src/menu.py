import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width= screen.get_width()
        self.height = screen.get_height()

        self.font_titulo = pygame.font.Font(None, 80)
        self.font_boton = pygame.font.Font(None, 50)
        self.font_ranking= pygame.font.Font(None, 35)

        self.opciones = ["Jugar","Ranking", "Salir"]

        self.seleccion = 0  # Opción seleccionada actualmente
        self.mostrar_Ranking= False
        self.ranking=[]

    def dibujar(self):
        self.screen.fill((20, 20, 20))

        titulo= self.font_titulo.render("SURVIVOR 2D", True, (255, 255, 255))

        titulo_rect = titulo.get_rect(center=(self.width // 2, 120))
        self.screen.blit(titulo, titulo_rect)

        for index, opcion in enumerate(self.opciones):
            if index == self.seleccion:
                color = (255, 220, 50) 
            else:
                color = (255, 255, 255)
            texto= self.font_boton.render(opcion, True, color)
            texto_rect = texto.get_rect(center=(self.width // 2, 250 + index * 70))
            self.screen.blit(texto, texto_rect)

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


    def manejar_eventos(self, event):
        if self.mostrar_Ranking:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mostrar_Ranking=False
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.seleccion = (self.seleccion - 1) % len(self.opciones)
            elif event.key == pygame.K_DOWN:
                self.seleccion = (self.seleccion + 1) % len(self.opciones)
            elif event.key == pygame.K_RETURN:
                return self.opciones[self.seleccion]

        return None

    def abrir_Ranking(self, ranking):
        self.ranking= ranking
        self.mostrar_Ranking= True


        