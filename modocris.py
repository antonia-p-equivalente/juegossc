#!/usr/bin/env python3
import os
import sys
import subprocess
import pygame
from leerBoton import leer_boton

# ——— Configuración de pantalla y FPS ———
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320
FPS = 30

def launch_game(script_path):
    """Lanza el script Python indicado y espera a que termine."""
    subprocess.call([sys.executable, script_path])

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Repositorio de Mini-Juegos")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Directorio base (asume que este archivo está en la misma carpeta que los juegos)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    games = [
        ("Bola Rebotona",    os.path.join(base_dir, "juego_bola_rebotona.py")),
        ("Reaction Timer",   os.path.join(base_dir, "juego_reaction_timer.py")),
        ("Button Masher",    os.path.join(base_dir, "juego_button_masher.py")),
    ]

    current = 0
    running = True

    while running:
        clock.tick(FPS)

        # Leer GPIO
        btn = leer_boton()
        if btn:
            b = btn.strip().upper()
            if b == 'DOWN':
                current = (current + 1) % len(games)
            elif b == 'UP':
                current = (current - 1) % len(games)
            elif b == 'A':
                _, script = games[current]
                launch_game(script)
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
