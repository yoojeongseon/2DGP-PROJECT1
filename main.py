# (파일: main.py)

import pygame
import os
from player import Player  # <-- player.py 파일에서 Player 클래스를 가져옵니다.

# --- Pygame 초기화 및 설정 ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2DGP 프로젝트 - 5주차 (동시 타격 수정)")
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

    # --- [수정] 3. 타격 판정 로직 (동시 타격 버그 수정) ---

    # P1이 P2를 때렸는지 검사
    attack_name_p1 = player1.current_state
    current_attack_p1 = player1.attacks.get(attack_name_p1)

    if (current_attack_p1 and
            player1.current_frame == current_attack_p1.hit_frame and
            pygame.sprite.collide_rect(player1, player2) and
            player1.has_hit == False and
            player2.is_alive):  # P2가 살아있을 때만

        player1.has_hit = True

        if player2.current_state == 'Blocking':
            print("P2 Blocked!")
        else:  # [수정] 방어 중이 아니면 (공격 중이어도) 무조건 맞음
            if attack_name_p1 == 'Uppercut':
                player2.take_damage(player2.max_hp)
            else:
                damage = current_attack_p1.damage
                player2.take_damage(damage)

    # P2가 P1을 때렸는지 검사
    attack_name_p2 = player2.current_state
    current_attack_p2 = player2.attacks.get(attack_name_p2)

    if (current_attack_p2 and
            player2.current_frame == current_attack_p2.hit_frame and
            pygame.sprite.collide_rect(player2, player1) and
            player2.has_hit == False and
            player1.is_alive):  # P1이 살아있을 때만

        player2.has_hit = True

        if player1.current_state == 'Blocking':
            print("P1 Blocked!")
        else:  # [수정] 방어 중이 아니면 (공격 중이어도) 무조건 맞음
            if attack_name_p2 == 'Uppercut':
                player1.take_damage(player1.max_hp)
            else:
                damage = current_attack_p2.damage
                player1.take_damage(damage)

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