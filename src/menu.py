import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width= screen.get_width()
        self.height = screen.get_height()

        self.font_titulo = pygame.font.Font(None, 80)
        self.font_boton = pygame.font.Font(None, 50)

        self.opciones = ["Jugar","Ranking", "Salir"]

        self.seleccion = 0  # Opción seleccionada actualmente

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

    def manejar_eventos(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.seleccion = (self.seleccion - 1) % len(self.opciones)
            elif event.key == pygame.K_DOWN:
                self.seleccion = (self.seleccion + 1) % len(self.opciones)
            elif event.key == pygame.K_RETURN:
                return self.opciones[self.seleccion]

        return None


        