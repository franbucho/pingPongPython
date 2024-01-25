import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ping Pong")

# Definir las paletas y la pelota
paleta_ancho = 15
paleta_alto = 60
pelota_tamano = 20

paleta1_x = 50
paleta1_y = ALTO // 2 - paleta_alto // 2

paleta2_x = ANCHO - 50 - paleta_ancho
paleta2_y = ALTO // 2 - paleta_alto // 2

pelota_x = ANCHO // 2 - pelota_tamano // 2
pelota_y = ALTO // 2 - pelota_tamano // 2

velocidad_paleta = 8  # Aumentamos la velocidad de las paletas
velocidad_pelota = [random.choice([-6, 6]), random.choice([-6, 6])]

# Marcadores
puntuacion1 = 0
puntuacion2 = 0
fuente = pygame.font.Font(None, 36)

# Mensaje de reinicio
mensaje_reinicio = ""

# Bucle principal del juego
reloj = pygame.time.Clock()

def reiniciar_juego():
    global pelota_x, pelota_y, velocidad_pelota, puntuacion1, puntuacion2, mensaje_reinicio
    pelota_x = ANCHO // 2 - pelota_tamano // 2
    pelota_y = ALTO // 2 - pelota_tamano // 2
    velocidad_pelota = [random.choice([-6, 6]), random.choice([-6, 6])]
    mensaje_reinicio = ""

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                reiniciar_juego()

    # Obtener las teclas presionadas
    teclas = pygame.key.get_pressed()

    # Mover las paletas
    if teclas[pygame.K_w] and paleta1_y > 0:
        paleta1_y -= velocidad_paleta
    if teclas[pygame.K_s] and paleta1_y < ALTO - paleta_alto:
        paleta1_y += velocidad_paleta

    if teclas[pygame.K_UP] and paleta2_y > 0:
        paleta2_y -= velocidad_paleta
    if teclas[pygame.K_DOWN] and paleta2_y < ALTO - paleta_alto:
        paleta2_y += velocidad_paleta

    # Mover la pelota
    pelota_x += velocidad_pelota[0]
    pelota_y += velocidad_pelota[1]

    # Rebotar la pelota en las paredes verticales
    if pelota_y <= 0 or pelota_y >= ALTO - pelota_tamano:
        velocidad_pelota[1] = -velocidad_pelota[1]

    # Rebotar la pelota en las paletas
    if (
        paleta1_x <= pelota_x <= paleta1_x + paleta_ancho
        and paleta1_y <= pelota_y <= paleta1_y + paleta_alto
    ) or (
        paleta2_x <= pelota_x <= paleta2_x + paleta_ancho
        and paleta2_y <= pelota_y <= paleta2_y + paleta_alto
    ):
        velocidad_pelota[0] = -velocidad_pelota[0]

    # Puntuación y reinicio
    if pelota_x <= 0:
        puntuacion2 += 1
        mensaje_reinicio = "Presiona 'R' para reiniciar"
        reiniciar_juego()
    elif pelota_x >= ANCHO - pelota_tamano:
        puntuacion1 += 1
        mensaje_reinicio = "Presiona 'R' para reiniciar"
        reiniciar_juego()

    # Si la pelota pasa más allá de las paletas, aumenta el marcador del jugador contrario
    if pelota_x < 0 or pelota_x > ANCHO:
        mensaje_reinicio = "Presiona 'R' para reiniciar"
        reiniciar_juego()

    # Limpiar la pantalla
    pantalla.fill(BLANCO)

    # Dibujar las paletas
    pygame.draw.rect(pantalla, NEGRO, (paleta1_x, paleta1_y, paleta_ancho, paleta_alto))
    pygame.draw.rect(pantalla, NEGRO, (paleta2_x, paleta2_y, paleta_ancho, paleta_alto))

    # Dibujar la pelota
    pygame.draw.ellipse(pantalla, NEGRO, (pelota_x, pelota_y, pelota_tamano, pelota_tamano))

    # Dibujar el marcador
    texto_puntuacion = fuente.render(f"{puntuacion1} - {puntuacion2}", True, NEGRO)
    pantalla.blit(texto_puntuacion, (ANCHO // 2 - 50, 20))

    # Dibujar el mensaje de reinicio
    texto_reinicio = fuente.render(mensaje_reinicio, True, NEGRO)
    pantalla.blit(texto_reinicio, (ANCHO // 2 - 140, ALTO // 2 - 20))

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer la velocidad del juego
    reloj.tick(60)
