#!/usr/bin/env python3
import pygame
import sys
import subprocess
from leerBoton import leer_boton

# ——— Configuración de pantalla y FPS ———
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320
FPS = 30

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menú de Mini-Juegos")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Lista de juegos: (Etiqueta, comando)
    games = [
        ("Bola Rebotona",      ["python3", "juego_bola_rebotona.py"]),
        ("Reaction Timer",     ["python3", "juego_reaction_timer.py"]),
        ("Button Masher",      ["python3", "juego_button_masher.py"]),
    ]

    current = 0
    running = True

    while running:
        clock.tick(FPS)

        # Procesar cierre de ventana
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # Leer botón de hardware
        btn = leer_boton()
        if btn:
            b = btn.strip().upper()
            if b == 'DOWN':
                current = (current + 1) % len(games)
            elif b == 'UP':
                current = (current - 1) % len(games)
            elif b == 'A':
                # Lanza el juego y espera a que termine
                _, cmd = games[current]
                subprocess.call(cmd)
            elif b == 'MENU':
                running = False

        # Dibujar menú
        screen.fill((0, 0, 0))
        for idx, (label, _) in enumerate(games):
            color = (255, 255, 0) if idx == current else (255, 255, 255)
            text_surf = font.render(label, True, color)
            screen.blit(text_surf, (50, 80 + idx * 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
