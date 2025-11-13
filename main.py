# (파일: main.py)

import pygame
import os
from player import Player
# [수정] collisions.py 에서 타격 판정 함수를 가져옵니다.
from collisions import handle_player_collisions

# --- Pygame 초기화 및 설정 ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2DGP 프로젝트 - (Collisions 분리)")
clock = pygame.time.Clock()

# --- 색상 정의 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# --- UI 함수 (체력 바) ---
def draw_health_bar(surface, x, y, hp, max_hp):
    """체력 바를 그리는 함수"""
    if hp < 0: hp = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 20
    fill_percent = (hp / max_hp)
    fill_length = int(BAR_LENGTH * fill_percent)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill_length, BAR_HEIGHT)
    pygame.draw.rect(surface, RED, outline_rect)
    pygame.draw.rect(surface, GREEN, fill_rect)

# --- 4. 게임 객체 생성 ---
P1_SCALE = 0.5
P1_START_POS = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 30)
P1_CONTROLS = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_s)
P1_ANIM_FOLDERS = {
    'Idle': 'Idle', 'Walk': 'Walk',
    'Jab': 'PunchLeft', 'Straight': 'PunchRight', 'Uppercut': 'PunchUp',
    'Blocking': 'Blocking'
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

    # --- [수정] 3. 타격 판정 로직 ---
    # 복잡한 if문 대신, collisions 파일의 함수를 단 한번 호출합니다.
    handle_player_collisions(player1, player2)

    # 4) 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_health_bar(screen, 20, 20, player1.hp, player1.max_hp)
    draw_health_bar(screen, SCREEN_WIDTH - 320, 20, player2.hp, player2.max_hp)

    # 5) 화면 업데이트
    pygame.display.flip()

    # 6) FPS 설정
    clock.tick(60)

# --- 6. 게임 종료 ---
pygame.quit()