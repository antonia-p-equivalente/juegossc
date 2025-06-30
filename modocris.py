#!/usr/bin/env python3
import sys
import os
import json
import random
import time
import pygame
from pygame.locals import QUIT, KEYDOWN
from leerBoton import leer_boton

# ——— Configuración general ———
BASE_WIDTH, BASE_HEIGHT = 480, 320
FPS = 30

# Snake settings
CELL_SIZE   = 20
GRID_W      = BASE_WIDTH  // CELL_SIZE
GRID_H      = BASE_HEIGHT // CELL_SIZE
BG_COLOR    = (0, 0, 0)
SNAKE_COLOR = (0, 200, 0)
APPLE_COLOR = (200, 0, 0)
TEXT_COLOR  = (255, 255, 255)

# Highscore file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HS_FILE  = os.path.join(BASE_DIR, 'highscores.json')

# Load or init highscores
if os.path.exists(HS_FILE):
    with open(HS_FILE, 'r') as f:
        highs = json.load(f)
else:
    highs = {
        'bola_rebotona': 0,
        'reaction_timer': None,
        'button_masher': 0
    }

def save_highscores():
    with open(HS_FILE, 'w') as f:
        json.dump(highs, f)

def get_button():
    """Devuelve 'UP','DOWN','LEFT','RIGHT','A','MENU' o None."""
    gpio = leer_boton()
    if gpio:
        b = gpio.strip().upper()
        if b in ('UP','DOWN','LEFT','RIGHT','A','MENU'):
            return b
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit(); sys.exit()
        if ev.type == KEYDOWN:
            if ev.key == pygame.K_UP:    return 'UP'
            if ev.key == pygame.K_DOWN:  return 'DOWN'
            if ev.key == pygame.K_LEFT:  return 'LEFT'
            if ev.key == pygame.K_RIGHT: return 'RIGHT'
            if ev.key == pygame.K_z:     return 'A'
            if ev.key == pygame.K_x:     return 'MENU'
    return None

# ——— Juego: Bola Rebotona ———
def juego_bola_rebotona(screen, clock):
    ball_r = 10
    x, y = BASE_WIDTH/2, BASE_HEIGHT/2
    vx, vy = 6.0, 4.0
    SPEEDUP = 1.05
    paddle_w, paddle_h, paddle_s = 80, 10, 20
    paddle_x = (BASE_WIDTH - paddle_w) / 2
    paddle_y = BASE_HEIGHT - paddle_h - 10
    bounce_count = 0
    font = pygame.font.Font(None, 24)

    while True:
        clock.tick(FPS)
        b = get_button()
        keys = pygame.key.get_pressed()
        if b == 'LEFT'  or keys[pygame.K_LEFT]:
            paddle_x = max(0, paddle_x - paddle_s)
        if b == 'RIGHT' or keys[pygame.K_RIGHT]:
            paddle_x = min(BASE_WIDTH - paddle_w, paddle_x + paddle_s)
        if b == 'MENU':
            return

        x += vx; y += vy
        # Rebotes
        if x - ball_r <= 0:
            x, vx, vy = ball_r, abs(vx)*SPEEDUP, vy*SPEEDUP
        elif x + ball_r >= BASE_WIDTH:
            x, vx, vy = BASE_WIDTH-ball_r, -abs(vx)*SPEEDUP, vy*SPEEDUP
        if y - ball_r <= 0:
            y, vy, vx = ball_r, abs(vy)*SPEEDUP, vx*SPEEDUP

        # Rebote pala o perder
        if y + ball_r >= paddle_y:
            if paddle_x <= x <= paddle_x + paddle_w:
                y = paddle_y - ball_r
                vy, vx = -abs(vy)*SPEEDUP, vx*SPEEDUP
                bounce_count += 1
            else:
                if bounce_count > highs['bola_rebotona']:
                    highs['bola_rebotona'] = bounce_count
                    save_highscores()
                return

        # Dibujo en superficie base
        surf = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        surf.fill(BG_COLOR)
        pygame.draw.rect(surf, (200,200,200),
                         (paddle_x, paddle_y, paddle_w, paddle_h))
        pygame.draw.circle(surf, (255,255,255),
                           (int(x), int(y)), ball_r)
        surf.blit(font.render(f"Puntaje: {bounce_count}", True, (255,255,255)), (10,10))
        surf.blit(font.render(f"Mejor: {highs['bola_rebotona']}", True, (255,255,0)), (10,30))
        # Escala y presenta
        screen.blit(pygame.transform.scale(surf, screen.get_size()), (0,0))
        pygame.display.flip()

# ——— Juego: Reaction Timer ———
def juego_reaction_timer(screen, clock):
    font = pygame.font.Font(None, 48)
    state = 'WAIT_START'
    wait_delay = start_time = reaction = 0

    while True:
        clock.tick(FPS)
        b = get_button()
        surf = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)); surf.fill(BG_COLOR)

        if state == 'WAIT_START':
            surf.blit(font.render("A: Iniciar", True, (255,255,255)), (160,140))
            if b == 'A':
                wait_delay = random.uniform(1.0,3.0)
                start_time = time.time()
                state = 'WAIT_GO'

        elif state == 'WAIT_GO':
            elapsed = time.time() - start_time
            if b == 'A' and elapsed < wait_delay:
                state = 'PENALIZE'
            elif elapsed >= wait_delay:
                surf.blit(font.render("GO!", True, (0,255,0)), (200,140))
                if b == 'A':
                    reaction = (time.time()-(start_time+wait_delay))*1000
                    best = highs['reaction_timer']
                    if best is None or reaction < best:
                        highs['reaction_timer'] = reaction
                        save_highscores()
                    state = 'SHOW_RESULT'
            else:
                surf.blit(font.render("Get Ready...", True, (200,200,200)), (140,140))

        elif state == 'PENALIZE':
            surf.blit(font.render("¡Demasiado pronto!", True, (255,50,50)), (100,120))
            surf.blit(font.render("A: Reintentar  X: Salir", True, (255,255,255)), (80,180))
            if b == 'A':
                state = 'WAIT_START'
            elif b == 'MENU':
                return

        elif state == 'SHOW_RESULT':
            surf.blit(font.render(f"Tiempo: {int(reaction)} ms", True, (255,255,0)), (80,120))
            best = highs['reaction_timer'] or 0
            surf.blit(font.render(f"Mejor: {int(best)} ms", True, (255,200,200)), (80,180))
            surf.blit(font.render("A: Reintentar ", True, (255,255,255)), (80,240))
            if b == 'A':
                state = 'WAIT_START'
            elif b == 'MENU':
                return

        screen.blit(pygame.transform.scale(surf, screen.get_size()), (0,0))
        pygame.display.flip()

# ——— Juego: Button Masher ———
def juego_button_masher(screen, clock):
    font = pygame.font.Font(None, 48)
    state = 'WAIT_START'
    count = start_time = 0
    DURATION = 5.0

    while True:
        clock.tick(FPS)
        b = get_button()
        surf = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)); surf.fill(BG_COLOR)

        if state == 'WAIT_START':
            surf.blit(font.render("A: Comenzar", True, (255,255,255)), (140,140))
            if b == 'A':
                count = 0
                start_time = time.time()
                state = 'MASH'

        elif state == 'MASH':
            elapsed = time.time() - start_time
            if elapsed < DURATION:
                if b == 'A':
                    count += 1
                surf.blit(font.render(f"Count: {count}", True, (0,255,0)), (160,100))
                surf.blit(font.render(f"Time: {int(DURATION-elapsed)}", True, (255,255,0)), (160,180))
            else:
                if count > highs['button_masher']:
                    highs['button_masher'] = count
                    save_highscores()
                state = 'SHOW_RESULT'

        elif state == 'SHOW_RESULT':
            surf.blit(font.render(f"Mejor: {highs['button_masher']}", True, (255,200,200)), (120,120))
            surf.blit(font.render("A: Reintentar ", True, (255,255,255)), (100,180))
            if b == 'A':
                state = 'WAIT_START'
            elif b == 'MENU':
                return

        screen.blit(pygame.transform.scale(surf, screen.get_size()), (0,0))
        pygame.display.flip()

# ——— Juego: Snake ———
def draw_text(surface, text, size, x, y, color):
    f = pygame.font.Font(None, size)
    surface.blit(f.render(text, True, color), (x, y))

def juego_snake(screen, clock):
    snake = [(GRID_W//2, GRID_H//2),
             (GRID_W//2-1, GRID_H//2),
             (GRID_W//2-2, GRID_H//2)]
    direction = (1,0)
    paused = False

    def place_apple():
        while True:
            p = (random.randrange(GRID_W), random.randrange(GRID_H))
            if p not in snake:
                return p

    apple = place_apple(); score = 0

    while True:
        clock.tick(FPS)
        b = get_button()
        if b == 'A':
            paused = not paused
        if b == 'MENU':
            return

        surf = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)); surf.fill(BG_COLOR)

        if not paused:
            if b == 'UP'    and direction!=(0,1): direction=(0,-1)
            elif b == 'DOWN'and direction!=(0,-1):direction=(0,1)
            elif b == 'LEFT'and direction!=(1,0):  direction=(-1,0)
            elif b == 'RIGHT'and direction!=(-1,0):direction=(1,0)

            newh = (snake[0][0]+direction[0], snake[0][1]+direction[1])
            if (newh[0]<0 or newh[0]>=GRID_W or newh[1]<0 or newh[1]>=GRID_H or newh in snake):
                # Game over
                while True:
                    clock.tick(FPS)
                    surf.fill(BG_COLOR)
                    draw_text(surf, f"Game Over! Score: {score}", 36, 40, 120, TEXT_COLOR)
                    draw_text(surf, "A=Reintentar  X=Menu", 24, 100, 180, TEXT_COLOR)
                    screen.blit(pygame.transform.scale(surf, screen.get_size()), (0,0))
                    pygame.display.flip()
                    b2 = get_button()
                    if b2=='A':
                        return juego_snake(screen, clock)
                    if b2=='MENU':
                        return

            snake.insert(0, newh)
            if newh==apple:
                score+=1
                apple = place_apple()
            else:
                snake.pop()

        # draw
        ax, ay = apple
        pygame.draw.rect(surf, APPLE_COLOR,
            (ax*CELL_SIZE, ay*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for sx, sy in snake:
            pygame.draw.rect(surf, SNAKE_COLOR,
                (sx*CELL_SIZE, sy*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        draw_text(surf, f"Puntaje: {score}", 24, 10, 10, TEXT_COLOR)
        if paused:
            draw_text(surf, "Pausa", 48,
                      BASE_WIDTH//2-60, BASE_HEIGHT//2-24, TEXT_COLOR)

        screen.blit(pygame.transform.scale(surf, screen.get_size()), (0,0))
        pygame.display.flip()

# ——— Menú principal ———
def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("PiGamer: Mini-Juegos")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    instr_font = pygame.font.Font(None, 20)

    juegos = [
        ("Bola Rebotona",    juego_bola_rebotona),
        ("Reaction Timer",   juego_reaction_timer),
        ("Button Masher",    juego_button_masher),
        ("Snake",            juego_snake),
    ]
    selected = 0
    NAV_DELAY = 0.2
    last_nav = time.time()

    while True:
        clock.tick(FPS)
        now = time.time()
        b = get_button()

        # --- navegación con delay ---
        if b in ('DOWN','UP') and now - last_nav > NAV_DELAY:
            if b=='DOWN':
                selected = (selected + 1) % len(juegos)
            else:
                selected = (selected - 1) % len(juegos)
            last_nav = now

        # --- dibujar menú en superficie base ---
        surf = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
        surf.fill(BG_COLOR)
        for idx, (label, _) in enumerate(juegos):
            color = (255,255,0) if idx==selected else (255,255,255)
            surf.blit(font.render(label, True, color), (50, 80 + idx*50))
        # instrucciones
        ins1 = instr_font.render("A: Seleccionar", True, (200,200,200))
        ins2 = instr_font.render("X: Salir",        True, (200,200,200))
        y_pos = BASE_HEIGHT - 30
        x1 = BASE_WIDTH * 0.25 - ins1.get_width()/2
        x2 = BASE_WIDTH * 0.75 - ins2.get_width()/2
        surf.blit(ins1, (x1, y_pos))
        surf.blit(ins2, (x2, y_pos))

        # escalado a pantalla completa
        screen.blit(pygame.transform.scale(surf, screen.get_size()), (0,0))
        pygame.display.flip()

        if b=='A':
            juegos[selected][1](screen, clock)
        elif b=='MENU':
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
