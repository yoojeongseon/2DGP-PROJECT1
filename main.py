# (파일: main.py - 최종 버전)

import pygame
import os
from player import Player
from collisions import handle_player_collisions

# --- Pygame 초기화 및 설정 ---
pygame.init()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# [수정] 캡션에서 (디버그 모드) 제거
pygame.display.set_caption("2DGP 프로젝트")
clock = pygame.time.Clock()

# --- 색상 정의 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # 각성 효과용


# --- UI 함수 (체력 바) ---
def draw_health_bar(surface, x, y, hp, max_hp, is_awakened):
    """체력 바를 그리는 함수"""
    if hp < 0: hp = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 20
    fill_percent = (hp / max_hp)
    fill_length = int(BAR_LENGTH * fill_percent)

    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill_length, BAR_HEIGHT)

    # 각성 상태면 체력 바 색상 변경
    bar_color = YELLOW if is_awakened else GREEN

    pygame.draw.rect(surface, RED, outline_rect)
    pygame.draw.rect(surface, bar_color, fill_rect)


# --- 4. 게임 객체 생성 ---
P1_SCALE = 0.5
P1_START_POS = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 30)
P1_CONTROLS = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_s)

# 'Dizzy'와 'KO' 폴더 매핑 추가
P1_ANIM_FOLDERS = {
    'Idle': 'Idle', 'Walk': 'Walk',
    'Jab': 'PunchLeft', 'Straight': 'PunchRight', 'Uppercut': 'PunchUp',
    'Blocking': 'Blocking',
    'Dizzy': 'Dizzy',
    'KO': 'KO'
}
player1 = Player(P1_START_POS, P1_CONTROLS, P1_ANIM_FOLDERS, SCREEN_WIDTH, P1_SCALE, flip_images=False)

P2_SCALE = 0.5
P2_START_POS = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 30)
P2_CONTROLS = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_DOWN)
P2_ANIM_FOLDERS = P1_ANIM_FOLDERS
player2 = Player(P2_START_POS, P2_CONTROLS, P2_ANIM_FOLDERS, SCREEN_WIDTH, P2_SCALE, flip_images=True)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# --- 5. 메인 게임 루프 ---
running = True
while running:
    # 1) 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2) 게임 로직 업데이트
    all_sprites.update()

    # 3) 타격 판정 로직
    handle_player_collisions(player1, player2)

    # 4) 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # 체력 바 그리기
    draw_health_bar(screen, 20, 20, player1.hp, player1.max_hp, player1.is_awakened)
    draw_health_bar(screen, SCREEN_WIDTH - 320, 20, player2.hp, player2.max_hp, player2.is_awakened)

    # --- [수정] 판정 박스 시각화 (디버그 코드) 모두 제거됨 ---

    # 5) 화면 업데이트
    pygame.display.flip()

    # 6) FPS 설정
    clock.tick(60)

# --- 6. 게임 종료 ---
pygame.quit()