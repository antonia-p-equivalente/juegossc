#!/usr/bin/env python3
import os
import sys
import subprocess
import pygame
from pygame.locals import QUIT, KEYDOWN, K_DOWN, K_UP, K_RETURN
from leerBoton import leer_boton

# ——— Configuración ———
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 480
SCREEN_HEIGHT= 320
FPS          = 30

# Define tus juegos con rutas absolutas
GAMES = [
    ("Bola Rebotona",      os.path.join(BASE_DIR, "juego_bola_rebotona.py")),
    ("Reaction Timer",     os.path.join(BASE_DIR, "juego_reaction_timer.py")),
    ("Button Masher",      os.path.join(BASE_DIR, "juego_button_masher.py")),
]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Menú de Mini-Juegos")
    clock = pygame.time.Clock()
    font  = pygame.font.Font(None, 36)

    current = 0
    running = True

    print("DEBUG: MENU arrancado")  # Ver en consola

    while running:
        clock.tick(FPS)

        # 1) Leer hardware
        btn = leer_boton()
        print(f"DEBUG: leer_boton() → {btn!r}")
        if btn:
            b = btn.strip().upper()
            print(f"DEBUG: botón normalizado → {b!r}")

            if b == 'DOWN':
                current = (current + 1) % len(GAMES)
            elif b == 'UP':
                current = (current - 1) % len(GAMES)
            elif b == 'A':
                label, path = GAMES[current]
                print(f"DEBUG: Lanzando «{label}» → {path}")
                # Usa el mismo intérprete de este script
                subprocess.call([sys.executable, path])
                print("DEBUG: retorno de subprocess.call")
            elif b == 'MENU':
                print("DEBUG: MENU presionado, saliendo del menú")
                running = False

        # 2) Fallback teclado
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_DOWN:
                    current = (current + 1) % len(GAMES)
                elif e.key == K_UP:
                    current = (current - 1) % len(GAMES)
                elif e.key == K_RETURN:
                    label, path = GAMES[current]
                    print(f"DEBUG: (teclado) Lanzando «{label}» → {path}")
                    subprocess.call([sys.executable, path])
                # no usamos ESC o similar aquí para MENU

        # 3) Dibujar menú
        screen.fill((0, 0, 0))
        for idx, (label, _) in enumerate(GAMES):
            color = (255,255,0) if idx == current else (255,255,255)
            surf  = font.render(label, True, color)
            screen.blit(surf, (50, 80 + idx * 50))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
