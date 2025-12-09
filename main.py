# (파일: main.py)

import pygame
from title_screen import TitleScreen
from game_screen import GameScreen

# --- 초기화 ---
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2DGP 프로젝트 - Boxing King")
clock = pygame.time.Clock()

# --- 상태 상수 ---
STATE_TITLE = "TITLE"
STATE_PLAY = "PLAY"

# --- 현재 상태 ---
current_state = STATE_TITLE

# 스크린 객체
title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
game_screen = None

# --- 메인 루프 ---
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if current_state == STATE_TITLE:
        action = title_screen.handle_events(events)
        if action == "PLAY":
            current_state = STATE_PLAY
            game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT)  # 게임 초기화

        title_screen.update()
        title_screen.draw(screen)

    elif current_state == STATE_PLAY:
        if game_screen:
            action = game_screen.handle_events(events)
            if action == "RESTART":
                game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT)  # 재시작
            elif action == "TITLE":
                current_state = STATE_TITLE
                game_screen = None  # 메모리 정리

            game_screen.update()
            game_screen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()