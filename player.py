# (파일: player.py)

import pygame
import os
from attacks import Attack  # <-- [추가] 새로 만든 Attack 클래스를 가져옵니다.


# --- 0. 헬퍼 함수 (애니메이션 로드) ---
# ( attacks.py 에서 이 함수를 사용하므로, 여기에도 존재해야 합니다 )
def load_animation_frames(folder_path, scale_factor=1.0, flip_images=False):
    """폴더 경로와 배율을 받아 스케일링 및 반전된 이미지 프레임 리스트를 반환합니다."""
    frames = []
    if not os.path.exists(folder_path):
        print(f"경고: 애니메이션 폴더를 찾을 수 없습니다: {folder_path}")
        return frames

    file_names = os.listdir(folder_path)

    try:
        file_names.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or 0))
    except ValueError:
        print(f"경고: {folder_path}의 파일명에서 숫자를 추출할 수 없습니다. 일반 정렬합니다.")
        file_names.sort()

    for file_name in file_names:
        if file_name.endswith(('.png', '.jpg', '.bmp')):
            image_path = os.path.join(folder_path, file_name)
            try:
                image = pygame.image.load(image_path).convert_alpha()
                width = image.get_width()
                height = image.get_height()
                image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
                if flip_images:
                    image = pygame.transform.flip(image, True, False)
                frames.append(image)
            except pygame.error as e:
                print(f"이미지 로드 오류 {image_path}: {e}")

    if not frames:
        print(f"경고: {folder_path} 폴더에서 이미지를 로드하지 못했습니다.")

    return frames


# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2DGP 프로젝트 - 3주차 (체력 시스템 적용)")

# FPS 설정을 위한 Clock 객체
clock = pygame.time.Clock()

# --- 2. 색상 정의 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # HP 바를 위한 색상


# --- 3. 플레이어 클래스 정의 (수정) ---
class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, controls, anim_folders, scale_factor=1.0, flip_images=False):
        super().__init__()

        # --- [수정] 1. 기본 애니메이션 로딩 ---
        self.animations = {}
        self.animations['Idle'] = load_animation_frames(
            anim_folders['Idle'], scale_factor, flip_images
        )
        self.animations['Walk'] = load_animation_frames(
            anim_folders['Walk'], scale_factor, flip_images
        )

        # --- [추가] 1-2. 공격 모션 로딩 (Attack 객체 사용) ---
        self.attacks = {}
        self.attacks['Jab'] = Attack(
            anim_folders.get('Jab', 'Jab'),
            10,  # 잽 데미지
            scale_factor,
            flip_images
        )
        self.attacks['Straight'] = Attack(
            anim_folders.get('Straight', 'Straight'),
            20,  # 스트레이트 데미지
            scale_factor,
            flip_images
        )
        self.attacks['Uppercut'] = Attack(
            anim_folders.get('Uppercut', 'Uppercut'),
            30,  # 어퍼컷 데미지
            scale_factor,
            flip_images
        )

        self.looping_states = ['Idle', 'Walk']

        # --- 2. 상태 및 애니메이션 관리 ---
        self.current_state = 'Idle'
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_delay = 100

        # --- 3. 이미지 및 위치 ---
        if self.animations['Idle']:
            self.image = self.animations['Idle'][0]
            self.rect = self.image.get_rect()
        else:
            print("오류: 'Idle' 애니메이션을 찾을 수 없습니다. 임시 사각형으로 대체합니다.")
            self.image = pygame.Surface((50, 100));
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        self.rect.midbottom = start_pos
        self.speed = 5
        self.is_moving = False

        # --- 4. 조작 키 저장 ---
        self.key_left = controls[0]
        self.key_right = controls[1]
        self.key_jab = controls[2]
        self.key_straight = controls[3]
        self.key_uppercut = controls[4]

        # --- [추가] 5. 체력 시스템 (3주차 목표) ---
        self.max_hp = 100
        self.hp = 100
        self.is_alive = True

    def animate(self):
        """현재 상태에 맞춰 애니메이션을 재생합니다."""
        now = pygame.time.get_ticks()

        if now - self.last_update_time <= self.animation_delay:
            return
        self.last_update_time = now

        # --- [수정] 상태 구분 로직 ---
        is_looping = self.current_state in self.looping_states

        current_frames = []
        is_attack = False

        if is_looping:
            # 'Idle', 'Walk' (반복 애니메이션) 로직
            current_frames = self.animations.get(self.current_state, self.animations['Idle'])
        else:
            # 'Jab', 'Straight' (공격 애니메이션) 로직
            if self.current_state in self.attacks:
                current_frames = self.attacks[self.current_state].frames
                is_attack = True
            else:
                # (예: 'Hurt', 'KO' 등 방어/피격 상태)
                current_frames = self.animations.get(self.current_state, self.animations['Idle'])

        if not current_frames:
            self.current_state = 'Idle'  # 프레임 없으면 Idle로 복귀
            return

        # --- 애니메이션 재생 ---
        if is_looping:
            self.current_frame = (self.current_frame + 1) % len(current_frames)
        else:
            # 공격 또는 피격 애니메이션 (한 번만 재생)
            self.current_frame += 1
            if self.current_frame >= len(current_frames):
                self.current_state = 'Idle'  # 애니메이션 끝 -> Idle 복귀
                self.current_frame = 0  # 프레임 리셋

        # --- 이미지 업데이트 (Idle로 복귀한 경우도 처리) ---
        if self.current_state == 'Idle':
            self.image = self.animations['Idle'][self.current_frame % len(self.animations['Idle'])]
        else:
            self.image = current_frames[self.current_frame]

        # --- 위치 고정 (동일) ---
        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def update(self):
        """플레이어 입력 처리 및 상태 업데이트."""
        # (KO 상태 등에서는 조작 불가)
        if not self.is_alive:
            # (나중에 'KO' 상태 애니메이션 추가)
            return

        keys = pygame.key.get_pressed()

        # 1. 공격 중(busy)이면 다른 입력 무시
        is_busy = self.current_state not in self.looping_states
        if is_busy:
            self.animate()
            return  # update 함수 종료

        # 2. 공격 입력 (이동보다 우선)
        if keys[self.key_jab]:
            self.current_state = 'Jab'
            self.current_frame = 0
        elif keys[self.key_straight]:
            self.current_state = 'Straight'
            self.current_frame = 0
        elif keys[self.key_uppercut]:
            self.current_state = 'Uppercut'
            self.current_frame = 0

        # 3. 이동 입력 (공격 중이 아닐 때)
        else:
            self.is_moving = False
            if keys[self.key_left]:
                self.rect.x -= self.speed
                self.is_moving = True
            if keys[self.key_right]:
                self.rect.x += self.speed
                self.is_moving = True

            self.current_state = 'Walk' if self.is_moving else 'Idle'

        # --- 화면 경계 처리 ---
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        # --- 애니메이션 실행 ---
        self.animate()

    def take_damage(self, damage):
        """피해를 입고 체력을 감소시킵니다."""
        if not self.is_alive: return

        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.current_state = 'KO'  # (나중에 KO 애니메이션 추가)
            self.current_frame = 0
            print("KO!")
        else:
            # (나중에 'Hurt' 애니메이션 추가)
            # self.current_state = 'Hurt'
            # self.current_frame = 0
            print(f"Hit! HP left: {self.hp}")


# --- 4. 게임 객체 생성 ---
# (P1_ANIM_FOLDERS, P2_ANIM_FOLDERS 설정은 기존과 동일)
P1_SCALE = 0.5
P1_START_POS = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 30)
P1_CONTROLS = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e, pygame.K_r)
P1_ANIM_FOLDERS = {
    'Idle': 'Idle', 'Walk': 'Walk',
    'Jab': 'PunchLeft', 'Straight': 'PunchRight', 'Uppercut': 'PunchUp'
}
player1 = Player(P1_START_POS, P1_CONTROLS, P1_ANIM_FOLDERS, P1_SCALE, flip_images=False)

P2_SCALE = 0.5
P2_START_POS = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 30)
P2_CONTROLS = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_u, pygame.K_i, pygame.K_o)
P2_ANIM_FOLDERS = P1_ANIM_FOLDERS
player2 = Player(P2_START_POS, P2_CONTROLS, P2_ANIM_FOLDERS, P2_SCALE, flip_images=True)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)


# --- [추가] 7주차 UI 구현 (체력 바) ---
def draw_health_bar(surface, x, y, hp, max_hp):
    """체력 바를 그리는 함수"""
    if hp < 0: hp = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 20
    fill_percent = (hp / max_hp)
    fill_length = int(BAR_LENGTH * fill_percent)

    # 테두리(빨간색)와 내부(초록색)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill_length, BAR_HEIGHT)

    pygame.draw.rect(surface, RED, outline_rect)
    pygame.draw.rect(surface, GREEN, fill_rect)


# --- 5. 메인 게임 루프 ---
running = True
while running:
    # 1) 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2) 게임 로직 업데이트
    all_sprites.update()

    # --- [추가] 3주차 타격 판정 로직 ---
    # P1이 P2를 때렸는지 검사
    attack_name_p1 = player1.current_state
    if (attack_name_p1 in player1.attacks and  # P1이 공격 상태이고
            player1.current_frame == 1 and  # [수정] 애니메이션 1프레임(타격 순간)
            pygame.sprite.collide_rect(player1, player2)):  # 충돌했다면

        # P2가 아직 피격되지 않았다면 (중복 타격 방지)
        if player2.current_state == 'Idle' or player2.current_state == 'Walk':
            damage = player1.attacks[attack_name_p1].damage  # Attack 객체에서 데미지 가져오기
            player2.take_damage(damage)

    # P2가 P1을 때렸는지 검사
    attack_name_p2 = player2.current_state
    if (attack_name_p2 in player2.attacks and
            player2.current_frame == 1 and
            pygame.sprite.collide_rect(player2, player1)):

        if player1.current_state == 'Idle' or player1.current_state == 'Walk':
            damage = player2.attacks[attack_name_p2].damage
            player1.take_damage(damage)

    # 3) 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # [추가] 체력 바 그리기 (7주차 UI)
    draw_health_bar(screen, 20, 20, player1.hp, player1.max_hp)  # P1 HP (왼쪽 상단)
    draw_health_bar(screen, SCREEN_WIDTH - 320, 20, player2.hp, player2.max_hp)  # P2 HP (오른쪽 상단)

    # 4) 화면 업데이트
    pygame.display.flip()

    # 5) FPS 설정
    clock.tick(60)

# --- 6. 게임 종료 ---
pygame.quit()