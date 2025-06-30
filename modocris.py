#!/usr/bin/env python3
import sys
import os
import random
import time
import pygame
from pygame.locals import QUIT
from leerBoton import leer_boton

# ——— Configuración general ———
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320
FPS = 30

def get_button():
    """
    Lee un único “botón” de hardware o teclado.
    Devuelve: 'UP','DOWN','LEFT','RIGHT','A','MENU' o None.
    """
    # 1) hardware
    btn = leer_boton()
    if btn:
        b = btn.strip().upper()
        if b in ('UP','DOWN','LEFT','RIGHT','A','MENU'):
            return b
    # 2) teclado
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit(); sys.exit()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:      return 'UP'
            if ev.key == pygame.K_DOWN:    return 'DOWN'
            if ev.key == pygame.K_LEFT:    return 'LEFT'
            if ev.key == pygame.K_RIGHT:   return 'RIGHT'
            if ev.key == pygame.K_z:       return 'A'
            if ev.key == pygame.K_x:       return 'MENU'
    return None

def juego_bola_rebotona(screen, clock):
    ball_r = 10
    x, y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2
    vx, vy = 3.0, 2.0

    # Pala
    paddle_w, paddle_h, paddle_s = 80, 10, 5
    paddle_x = (SCREEN_WIDTH - paddle_w) / 2
    paddle_y = SCREEN_HEIGHT - paddle_h - 10

    while True:
        clock.tick(FPS)
        # Mover pala
        b = get_button()
        if b == 'LEFT':
            paddle_x = max(0, paddle_x - paddle_s)
        elif b == 'RIGHT':
            paddle_x = min(SCREEN_WIDTH - paddle_w, paddle_x + paddle_s)
        elif b == 'MENU':
            return

        # Mover bola
        x += vx; y += vy
        # Rebotes con paredes
        if x - ball_r <= 0:
            x = ball_r; vx = abs(vx)
        elif x + ball_r >= SCREEN_WIDTH:
            x = SCREEN_WIDTH - ball_r; vx = -abs(vx)
        if y - ball_r <= 0:
            y = ball_r; vy = abs(vy)

        # Rebote o perder en piso
        if y + ball_r >= paddle_y:
            if paddle_x <= x <= paddle_x + paddle_w:
                y = paddle_y - ball_r
                vy = -abs(vy)
            else:
                return  # pierdes

        # Dibujar
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (200,200,200), (paddle_x, paddle_y, paddle_w, paddle_h))
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), ball_r)
        pygame.display.flip()

def juego_reaction_timer(screen, clock):
    font = pygame.font.Font(None, 48)
    state = 'WAIT_START'
    wait_delay = start_time = reaction = 0

    while True:
        clock.tick(FPS)
        screen.fill((0,0,0))
        b = get_button()
        if b == 'MENU':
            return

        if state == 'WAIT_START':
            txt = font.render("Press A to start", True, (255,255,255))
            screen.blit(txt, (80,140))
            if b == 'A':
                wait_delay = random.uniform(1.0, 3.0)
                start_time = time.time()
                state = 'WAIT_GO'

        elif state == 'WAIT_GO':
            elapsed = time.time() - start_time
            if elapsed < wait_delay:
                txt = font.render("Get Ready...", True, (200,200,200))
                screen.blit(txt, (120,140))
            else:
                txt = font.render("GO!", True, (0,255,0))
                screen.blit(txt, (200,140))
                if b == 'A':
                    reaction = (time.time() - (start_time + wait_delay)) * 1000
                    state = 'SHOW_RESULT'

        elif state == 'SHOW_RESULT':
            txt1 = font.render(f"Reaction: {int(reaction)} ms", True, (255,255,0))
            txt2 = font.render("Press A to retry", True, (255,255,255))
            screen.blit(txt1, (50,120))
            screen.blit(txt2, (100,180))
            if b == 'A':
                state = 'WAIT_START'

        pygame.display.flip()

def juego_button_masher(screen, clock):
    font = pygame.font.Font(None, 48)
    state = 'WAIT_START'
    count = 0
    start_time = 0
    DURATION = 5.0

    while True:
        clock.tick(FPS)
        screen.fill((0,0,0))
        b = get_button()
        if b == 'MENU':
            return

        if state == 'WAIT_START':
            txt = font.render("Press A to begin", True, (255,255,255))
            screen.blit(txt, (100,140))
            if b == 'A':
                count = 0
                start_time = time.time()
                state = 'MASH'

        elif state == 'MASH':
            elapsed = time.time() - start_time
            if elapsed < DURATION:
                if b == 'A':
                    count += 1
                txt1 = font.render(f"Count: {count}", True, (0,255,0))
                txt2 = font.render(f"Time: {int(DURATION - elapsed)}", True, (255,255,0))
                screen.blit(txt1, (140,100))
                screen.blit(txt2, (160,180))
            else:
                state = 'SHOW_RESULT'

        elif state == 'SHOW_RESULT':
            txt1 = font.render(f"Score: {count}", True, (255,255,255))
            txt2 = font.render("Press A to retry", True, (255,255,0))
            screen.blit(txt1, (160,120))
            screen.blit(txt2, (100,180))
            if b == 'A':
                state = 'WAIT_START'

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Repositorio de Mini-Juegos")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    juegos = [
        ("Bola Rebotona",    juego_bola_rebotona),
        ("Reaction Timer",   juego_reaction_timer),
        ("Button Masher",    juego_button_masher),
    ]
    selected = 0

    while True:
        clock.tick(FPS)
        screen.fill((0,0,0))

        # Dibujar menú
        for idx, (label, _) in enumerate(juegos):
            color = (255,255,0) if idx == selected else (255,255,255)
            surf = font.render(label, True, color)
            screen.blit(surf, (50, 80 + idx*50))
        pygame.display.flip()

        b = get_button()
        if b == 'DOWN':
            selected = (selected + 1) % len(juegos)
        elif b == 'UP':
            selected = (selected - 1) % len(juegos)
        elif b == 'A':
            # Ejecuta el juego; vuelve aquí al terminar
            juegos[selected][1](screen, clock)
        elif b == 'MENU':
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
