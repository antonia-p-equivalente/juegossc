#!/usr/bin/env python3
import pygame, sys
from leerBoton import leer_boton

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 320))
    pygame.display.set_caption("Bola Rebotona")
    clock = pygame.time.Clock()
    FPS = 30

    # Bola
    ball_r = 10
    x, y = 240.0, 160.0
    vx, vy = 3.0, 2.0
    speed_delta = 1.0
    running = True

    while running:
        clock.tick(FPS)

        # 1) Mover bola
        x += vx
        y += vy
        # Rebotes
        if x - ball_r <= 0 or x + ball_r >= 480:
            vx = -vx
            x = max(ball_r, min(480-ball_r, x))
        if y - ball_r <= 0 or y + ball_r >= 320:
            vy = -vy
            y = max(ball_r, min(320-ball_r, y))

        # 2) Leer botones GPIO
        btn = leer_boton()
        if btn:
            b = btn.strip().upper()
            if b == 'LEFT':
                vx -= speed_delta
            elif b == 'RIGHT':
                vx += speed_delta
            elif b == 'UP':
                vy -= speed_delta
            elif b == 'DOWN':
                vy += speed_delta
            elif b == 'MENU':
                running = False

        # 3) Dibujar
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), ball_r)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
