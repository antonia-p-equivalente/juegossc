#!/usr/bin/env python3
import pygame, sys, random, time
from leerBoton import leer_boton

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Reaction Timer")
    clock = pygame.time.Clock()
    FPS = 30
    font = pygame.font.Font(None, 48)

    state = 'WAIT_START'  # WAIT_START → WAIT_GO → SHOW_RESULT
    wait_delay = 0
    start_time = 0
    reaction = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        # Leer botón
        btn = leer_boton()
        b = btn.strip().upper() if btn else None
        if b == 'MENU':
            break

        # Lógica de estados
        if state == 'WAIT_START':
            text = font.render("Press A to start", True, (255,255,255))
            screen.blit(text, (80,140))
            if b == 'A':
                # Iniciar espera aleatoria
                wait_delay = random.uniform(1.0, 3.0)
                start_time = time.time()
                state = 'WAIT_GO'

        elif state == 'WAIT_GO':
            elapsed = time.time() - start_time
            # Antes de que salga GO
            if elapsed < wait_delay:
                text = font.render("Get Ready...", True, (200,200,200))
                screen.blit(text, (120,140))
            else:
                # Mostrar GO y esperar A
                text = font.render("GO!", True, (0,255,0))
                screen.blit(text, (200,140))
                if b == 'A':
                    reaction = (time.time() - (start_time + wait_delay)) * 1000
                    state = 'SHOW_RESULT'

        elif state == 'SHOW_RESULT':
            txt1 = f"Reaction: {int(reaction)} ms"
            text = font.render(txt1, True, (255,255,0))
            screen.blit(text, (70,120))
            text2 = font.render("Press B to retry", True, (255,255,255))
            screen.blit(text2, (100,180))
            if b == 'B':
                state = 'WAIT_START'

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
