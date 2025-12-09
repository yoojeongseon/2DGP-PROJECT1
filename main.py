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

# --- 현재 상태 및 스크린 객체 ---
current_state = STATE_TITLE

# 타이틀 화면 객체 생성
title_screen = TitleScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
game_screen = None  # 게임 화면은 플레이 시작 시 생성

# --- 메인 루프 ---
running = True
while running:
    # 1. 이벤트 가져오기
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # 2. 상태 처리
    if current_state == STATE_TITLE:
        # [타이틀 화면]
        action = title_screen.handle_events(events)

        if action == "PLAY":
            current_state = STATE_PLAY
            # 게임 화면을 새로 생성 (이때 게임이 초기화됨)
            game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

        title_screen.update()
        title_screen.draw(screen)

    elif current_state == STATE_PLAY:
        # [게임 플레이 화면]
        if game_screen:
            action = game_screen.handle_events(events)

            if action == "RESTART":
                # 재시작: 게임 화면 객체를 다시 만듦
                game_screen = GameScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
            elif action == "TITLE":
                # 타이틀로: 상태 변경 및 게임 객체 삭제
                current_state = STATE_TITLE
                game_screen = None

            game_screen.update()
            game_screen.draw(screen)

    # 3. 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

pygame.quit()