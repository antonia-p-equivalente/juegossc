#!/usr/bin/env python3
import pygame, sys, time
from leerBoton import leer_boton

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Button Masher")
    clock = pygame.time.Clock()
    FPS = 30
    font = pygame.font.Font(None, 48)

    state = 'WAIT_START'  # WAIT_START → MASH → SHOW_RESULT
    mash_count = 0
    mash_start = 0
    MASH_DURATION = 5.0  # segundos

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        # Leer botón
        btn = leer_boton()
        b = btn.strip().upper() if btn else None
        if b == 'MENU':
            break

        if state == 'WAIT_START':
            text = font.render("Press A to begin", True, (255,255,255))
            screen.blit(text, (90,140))
            if b == 'A':
                mash_count = 0
                mash_start = time.time()
                state = 'MASH'

        elif state == 'MASH':
            elapsed = time.time() - mash_start
            if elapsed < MASH_DURATION:
                if b == 'A':
                    mash_count += 1
                # Mostrar cuenta y tiempo
                txt1 = font.render(f"Count: {mash_count}", True, (0,255,0))
                screen.blit(txt1, (140,100))
                txt2 = font.render(f"Time: {int(MASH_DURATION - elapsed)}", True, (255,255,0))
                screen.blit(txt2, (160,180))
            else:
                state = 'SHOW_RESULT'

        elif state == 'SHOW_RESULT':
            txt = font.render(f"Score: {mash_count}", True, (255,255,255))
            screen.blit(txt, (160,120))
            txt2 = font.render("Press B to retry", True, (255,255,0))
            screen.blit(txt2, (120,180))
            if b == 'B':
                state = 'WAIT_START'

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
