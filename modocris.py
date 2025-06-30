#!/usr/bin/env python3
import os
import sys
import subprocess
import pygame
from pygame.locals import K_UP, K_DOWN, K_z, K_x, KEYDOWN, QUIT

# — Configuración —
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320
FPS = 30

def launch_game(script):
    """Lanza el script Python indicado y espera a que termine."""
    subprocess.call([sys.executable, script])

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Repositorio de Mini-Juegos")
    clock = pygame.time.Clock()
    font  = pygame.font.Font(None, 36)

    base = os.path.dirname(os.path.abspath(__file__))
    games = [
        ("Bola Rebotona",    os.path.join(base, "juego_bola_rebotona.py")),
        ("Reaction Timer",   os.path.join(base, "juego_reaction_timer.py")),
        ("Button Masher",    os.path.join(base, "juego_button_masher.py")),
    ]

    selected = 0
    running = True

    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        # Dibujar menú
        for idx, (label, _) in enumerate(games):
            color = (255, 255, 0) if idx == selected else (255, 255, 255)
            text = font.render(label, True, color)
            screen.blit(text, (50, 80 + idx * 50))
        pygame.display.flip()

        # Procesar eventos de teclado
        for ev in pygame.event.get():
            if ev.type == QUIT:
                running = False
            elif ev.type == KEYDOWN:
                if ev.key == K_DOWN:
                    selected = (selected + 1) % len(games)
                elif ev.key == K_UP:
                    selected = (selected - 1) % len(games)
                elif ev.key == K_z:
                    _, script = games[selected]
                    launch_game(script)
                elif ev.key == K_x:
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
