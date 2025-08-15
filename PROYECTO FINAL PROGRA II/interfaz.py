import pygame
import sys
import math

pygame.init()

ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 800
FPS = 60

VERDE_OSCURO = (34, 51, 34)
VERDE_MILITAR = (75, 83, 32)
VERDE_CLARO = (106, 127, 16)
MARRON = (101, 67, 33)
MARRON_OSCURO = (62, 39, 35)
AZUL_ACERO = (70, 130, 180)
NARANJA = (255, 140, 0)
ROJO = (220, 20, 60)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)

class InterfazDefenseZone:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Defense Zone 3 Estilo - Tower Defense")
        self.reloj = pygame.time.Clock()
        self.fuente_grande = pygame.font.Font(None, 36)
        self.fuente_mediana = pygame.font.Font(None, 28)
        self.fuente_pequeña = pygame.font.Font(None, 20)
        self.dinero = 1000
        self.vidas = 20
        self.oleada = 1
        self.puntuacion = 0
        self.torre_seleccionada = None
        self.juego_pausado = False
        self.multiplicador_velocidad = 1
        self.tipos_torre = {
            'ametralladora': {'nombre': 'Ametralladora', 'costo': 50, 'color': GRIS, 'daño': 10, 'rango': 80},
            'cañon': {'nombre': 'Cañón', 'costo': 100, 'color': MARRON, 'daño': 50, 'rango': 100},
            'misil': {'nombre': 'Misil', 'costo': 200, 'color': ROJO, 'daño': 100, 'rango': 150},
            'laser': {'nombre': 'Láser', 'costo': 300, 'color': AZUL_ACERO, 'daño': 80, 'rango': 120}
        }
        self.torres_colocadas = []
        
    def dibujar_fondo(self):
        self.pantalla.fill(VERDE_OSCURO)
        for i in range(0, ANCHO_PANTALLA, 40):
            for j in range(0, ALTO_PANTALLA, 40):
                if (i + j) % 80 == 0:
                    pygame.draw.rect(self.pantalla, VERDE_MILITAR, (i, j, 35, 35))
        puntos_camino = [
            (0, 300), (200, 300), (200, 150), (400, 150),
            (400, 400), (600, 400), (600, 250), (800, 250),
            (800, 500), (ANCHO_PANTALLA, 500)
        ]
        for i in range(len(puntos_camino) - 1):
            inicio = puntos_camino[i]
            fin = puntos_camino[i + 1]
            pygame.draw.line(self.pantalla, MARRON, inicio, fin, 30)
            pygame.draw.line(self.pantalla, MARRON_OSCURO, inicio, fin, 20)
    
    def dibujar_panel_ui(self):
        rect_panel = pygame.Rect(ANCHO_PANTALLA - 220, 0, 220, ALTO_PANTALLA)
        pygame.draw.rect(self.pantalla, (40, 40, 40), rect_panel)
        pygame.draw.rect(self.pantalla, (60, 60, 60), pygame.Rect(ANCHO_PANTALLA - 218, 2, 216, ALTO_PANTALLA - 4))
        pygame.draw.rect(self.pantalla, (30, 30, 30), pygame.Rect(ANCHO_PANTALLA - 220, 0, 5, ALTO_PANTALLA))
        y_offset = 20
        texto_dinero = self.fuente_mediana.render(f"Dinero: ${self.dinero}", True, AMARILLO)
        self.pantalla.blit(texto_dinero, (ANCHO_PANTALLA - 210, y_offset))
        y_offset += 40
        texto_vidas = self.fuente_mediana.render(f"Vidas: {self.vidas}", True, ROJO)
        self.pantalla.blit(texto_vidas, (ANCHO_PANTALLA - 210, y_offset))
        y_offset += 40
        texto_oleada = self.fuente_mediana.render(f"Oleada: {self.oleada}", True, BLANCO)
        self.pantalla.blit(texto_oleada, (ANCHO_PANTALLA - 210, y_offset))
        y_offset += 40
        texto_puntuacion = self.fuente_mediana.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        self.pantalla.blit(texto_puntuacion, (ANCHO_PANTALLA - 210, y_offset))
        y_offset += 60
        titulo_torres = self.fuente_mediana.render("TORRES", True, NARANJA)
        self.pantalla.blit(titulo_torres, (ANCHO_PANTALLA - 210, y_offset))
        y_offset += 40
        for i, (tipo, info) in enumerate(self.tipos_torre.items()):
            rect_boton = pygame.Rect(ANCHO_PANTALLA - 210, y_offset, 190, 60)
            if self.dinero >= info['costo']:
                color_fondo = (50, 70, 50) if tipo == self.torre_seleccionada else (40, 60, 40)
            else:
                color_fondo = (60, 40, 40)
            pygame.draw.rect(self.pantalla, color_fondo, rect_boton)
            pygame.draw.rect(self.pantalla, BLANCO, rect_boton, 2)
            pygame.draw.circle(self.pantalla, info['color'], 
                             (ANCHO_PANTALLA - 185, y_offset + 20), 15)
            pygame.draw.circle(self.pantalla, BLANCO, 
                             (ANCHO_PANTALLA - 185, y_offset + 20), 15, 2)
            texto_nombre = self.fuente_pequeña.render(info['nombre'], True, BLANCO)
            texto_costo = self.fuente_pequeña.render(f"${info['costo']}", True, AMARILLO)
            self.pantalla.blit(texto_nombre, (ANCHO_PANTALLA - 160, y_offset + 10))
            self.pantalla.blit(texto_costo, (ANCHO_PANTALLA - 160, y_offset + 30))
            texto_daño = self.fuente_pequeña.render(f"Daño: {info['daño']}", True, GRIS_CLARO)
            self.pantalla.blit(texto_daño, (ANCHO_PANTALLA - 160, y_offset + 45))
            y_offset += 70
        y_offset += 20
        texto_pausa = "REANUDAR" if self.juego_pausado else "PAUSAR"
        color_pausa = VERDE_CLARO if self.juego_pausado else NARANJA
        boton_pausa = self.fuente_pequeña.render(texto_pausa, True, color_pausa)
        rect_pausa = pygame.Rect(ANCHO_PANTALLA - 210, y_offset, 90, 30)
        pygame.draw.rect(self.pantalla, (40, 40, 40), rect_pausa)
        pygame.draw.rect(self.pantalla, color_pausa, rect_pausa, 2)
        self.pantalla.blit(boton_pausa, (ANCHO_PANTALLA - 200, y_offset + 5))
        texto_velocidad = f"x{self.multiplicador_velocidad}"
        boton_velocidad = self.fuente_pequeña.render(texto_velocidad, True, AZUL_ACERO)
        rect_velocidad = pygame.Rect(ANCHO_PANTALLA - 110, y_offset, 90, 30)
        pygame.draw.rect(self.pantalla, (40, 40, 40), rect_velocidad)
        pygame.draw.rect(self.pantalla, AZUL_ACERO, rect_velocidad, 2)
        self.pantalla.blit(boton_velocidad, (ANCHO_PANTALLA - 100, y_offset + 5))
    
    def dibujar_torres(self):
        for torre in self.torres_colocadas:
            if torre.get('seleccionada', False):
                pygame.draw.circle(self.pantalla, (100, 100, 100, 50), 
                                 torre['posicion'], torre['rango'], 2)
            pygame.draw.circle(self.pantalla, torre['color'], torre['posicion'], 20)
            pygame.draw.circle(self.pantalla, BLANCO, torre['posicion'], 20, 3)
            angulo = torre.get('angulo', 0)
            fin_x = torre['posicion'][0] + 25 * math.cos(angulo)
            fin_y = torre['posicion'][1] + 25 * math.sin(angulo)
            pygame.draw.line(self.pantalla, torre['color'], torre['posicion'], (fin_x, fin_y), 5)
    
    def dibujar_enemigos(self):
        enemigos_demo = [(100, 300), (300, 150), (500, 400), (700, 250)]
        for pos in enemigos_demo:
            pygame.draw.circle(self.pantalla, (150, 0, 0), pos, 12)
            pygame.draw.circle(self.pantalla, (200, 0, 0), pos, 8)
            pygame.draw.polygon(self.pantalla, ROJO, [
                (pos[0] + 10, pos[1]), 
                (pos[0] - 8, pos[1] - 5), 
                (pos[0] - 8, pos[1] + 5)
            ])
    
    def dibujar_hud_superior(self):
        pygame.draw.rect(self.pantalla, (20, 20, 20), pygame.Rect(0, 0, ANCHO_PANTALLA - 220, 50))
        pygame.draw.rect(self.pantalla, GRIS, pygame.Rect(0, 48, ANCHO_PANTALLA - 220, 2))
        texto_nivel = self.fuente_mediana.render(f"Nivel: Bosque Militar", True, VERDE_CLARO)
        self.pantalla.blit(texto_nivel, (20, 15))
        if self.juego_pausado:
            texto_estado = self.fuente_mediana.render("JUEGO PAUSADO", True, ROJO)
        else:
            texto_estado = self.fuente_mediana.render("EN PROGRESO", True, VERDE_CLARO)
        self.pantalla.blit(texto_estado, (400, 15))
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    x, y = evento.pos
                    if x < ANCHO_PANTALLA - 220 and self.torre_seleccionada:
                        info_torre = self.tipos_torre[self.torre_seleccionada]
                        if self.dinero >= info_torre['costo']:
                            if not self.esta_en_camino(x, y):
                                nueva_torre = {
                                    'tipo': self.torre_seleccionada,
                                    'posicion': (x, y),
                                    'color': info_torre['color'],
                                    'rango': info_torre['rango'],
                                    'daño': info_torre['daño'],
                                    'angulo': 0
                                }
                                self.torres_colocadas.append(nueva_torre)
                                self.dinero -= info_torre['costo']
                                self.torre_seleccionada = None
                    elif x >= ANCHO_PANTALLA - 220:
                        self.manejar_click_ui(x, y)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.juego_pausado = not self.juego_pausado
                elif evento.key == pygame.K_1:
                    self.multiplicador_velocidad = 1
                elif evento.key == pygame.K_2:
                    self.multiplicador_velocidad = 2
                elif evento.key == pygame.K_3:
                    self.multiplicador_velocidad = 3
        return True
    
    def manejar_click_ui(self, x, y):
        y_torres = 260
        for i, (tipo, info) in enumerate(self.tipos_torre.items()):
            if y_torres <= y <= y_torres + 60:
                if self.dinero >= info['costo']:
                    self.torre_seleccionada = tipo if self.torre_seleccionada != tipo else None
                break
            y_torres += 70
        if 540 <= y <= 570 and ANCHO_PANTALLA - 210 <= x <= ANCHO_PANTALLA - 120:
            self.juego_pausado = not self.juego_pausado
        elif 540 <= y <= 570 and ANCHO_PANTALLA - 110 <= x <= ANCHO_PANTALLA - 20:
            self.multiplicador_velocidad = 1 if self.multiplicador_velocidad >= 3 else self.multiplicador_velocidad + 1
    
    def esta_en_camino(self, x, y):
        puntos_camino = [
            (0, 300), (200, 300), (200, 150), (400, 150),
            (400, 400), (600, 400), (600, 250), (800, 250),
            (800, 500), (ANCHO_PANTALLA, 500)
        ]
        for punto in puntos_camino:
            distancia = math.sqrt((x - punto[0])**2 + (y - punto[1])**2)
            if distancia < 40:
                return True
        return False
    
    def actualizar(self):
        if not self.juego_pausado:
            for torre in self.torres_colocadas:
                torre['angulo'] += 0.02
    
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar_fondo()
            self.dibujar_hud_superior()
            self.dibujar_enemigos()
            self.dibujar_torres()
            self.dibujar_panel_ui()
            if self.torre_seleccionada:
                pos_mouse = pygame.mouse.get_pos()
                if pos_mouse[0] < ANCHO_PANTALLA - 220:  
                    info_torre = self.tipos_torre[self.torre_seleccionada]
                    pygame.draw.circle(self.pantalla, info_torre['color'], pos_mouse, 20, 2)
                    pygame.draw.circle(self.pantalla, (100, 100, 100), pos_mouse, info_torre['rango'], 1)
            pygame.display.flip()
            self.reloj.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__  == "__main__":
    InterfazDefenseZone ().ejecutar()