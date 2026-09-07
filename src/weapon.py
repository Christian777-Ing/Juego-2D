import pygame as pg

class Weapon:
    def __init__(self, player):
        self.damage = 25
        self.fire_rate = 300  # Tiempo entre disparos en milisegundos
        self.cargador = 10  # Número de balas en el cargador
        self.ammo= self.cargador  # Munición actual

        self.ultimo_disparo = 0  

        self.tiempo_recarga = 1500  # Tiempo de recarga en milisegundos
        self.reload_start= None



    def puede_disparar(self):
        current_time = pg.time.get_ticks()
        if self.reload_start is not None:
            return False

        if current_time - self.ultimo_disparo >= self.fire_rate and self.ammo > 0:
            return True  # Disparo exitoso

        return False  # No se puede disparar aún o no hay munición


    def disparar(self):
        if self.puede_disparar():
            self.ultimo_disparo = pg.time.get_ticks()
            self.ammo -= 1
            return True  # Disparo exitoso
        return False  # No se pudo disparar

    def recargar(self):
        if self.ammo == self.cargador:
            return  # No es necesario recargar si el cargador está lleno
        if self.reload_start is None:
            self.reload_start = pg.time.get_ticks()  # Iniciar el tiempo de recarga

    
        
    def actualizar_balas(self):
        if self.reload_start is None:
            return  # No se está recargando

        current_time = pg.time.get_ticks()
        if current_time - self.reload_start >= self.tiempo_recarga:
            self.ammo = self.cargador  # Recargar el cargador
            self.reload_start = None  # Reiniciar el tiempo de recarga
            
    def is_reloading(self):
        return self.reload_start is not None