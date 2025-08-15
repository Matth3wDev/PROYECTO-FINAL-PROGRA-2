import pygame
import math

class misiles(pygame.sprite.Sprite):
    def __init__(self, x, y, target, damage):
        super().__init__()
        
        self.position = [x, y]
        self.target = target
        self.damage = damage
        self.speed = 5
        
        # Aquí cargarías la imagen del proyectil
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0)) # Color rojo para el misil de ejemplo
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        """Mueve el misil hacia su objetivo."""
        if self.target.alive():
            # Vector de dirección hacia el objetivo
            dx = self.target.x - self.position[0]
            dy = self.target.y - self.position[1]
            dist = math.hypot(dx, dy)
            
            if dist != 0:
                dx /= dist
                dy /= dist
                
            self.position[0] += dx * self.speed
            self.position[1] += dy * self.speed
            self.rect.center = self.position

            # Colisión con el enemigo
            if pygame.sprite.collide_rect(self, self.target):
                self.target.take_damage(self.damage)
                self.kill() # Elimina el misil
        else:
            self.kill() # Elimina el misil si el objetivo ya no existe