import pygame
import math
import misiles

class torres :
    def __init__(self, x, y):
        super().__init__()
        
        self.x = x
        self.y = y
        self.position = (x, y)
        self.range = 150  # Alcance en píxeles
        self.damage = 10
        self.fire_rate = 1.0  # Disparos por segundo
        self.last_shot_time = 0
        self.cost = 100
        self.level = 1
        
        # Aquí cargarías la imagen de la torre
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 100, 255)) # Color azul para la torre de ejemplo
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        """Busca el enemigo más cercano dentro del alcance."""
        closest_enemy = None
        min_distance = self.range

        for enemy in enemies:
            # Distancia euclidiana
            distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
            if distance <= self.range:
                if closest_enemy is None or distance < min_distance:
                    closest_enemy = enemy
                    min_distance = distance
        return closest_enemy

    def shoot(self, target, projectiles_group):
        """Dispara un proyectil al enemigo objetivo."""
        current_time = pygame.time.get_ticks() / 1000  # Convertir a segundos
        if current_time - self.last_shot_time > 1.0 / self.fire_rate:
            if target:
                new_missile = misiles(self.x, self.y, target, self.damage) 
                projectiles_group.add(new_missile)
                self.last_shot_time = current_time

    def draw(self, screen):
        """Dibuja la torre y su radio de alcance en la pantalla."""
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.range, 1)
        screen.blit(self.image, self.rect)