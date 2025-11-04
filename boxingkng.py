import pygame
import os


# --- 0. 헬퍼 함수 (애니메이션 로드) ---

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

                # --- [수정] 크기 조절 (Scaling) ---
                width = image.get_width()
                height = image.get_height()
                image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))

                # --- [수정] 좌우 반전 (Flipping) ---
                if flip_images:
                    image = pygame.transform.flip(image, True, False)  # True: 수평, False: 수직

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
pygame.display.set_caption("2DGP 프로젝트 - 복싱 게임 (2P)")

# FPS 설정을 위한 Clock 객체
clock = pygame.time.Clock()

# --- 2. 색상 정의 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# --- 3. 플레이어 클래스 정의 (수정) ---
class Player(pygame.sprite.Sprite):
    # [수정] __init__을 재사용 가능하도록 매개변수 추가
    def __init__(self, start_pos, controls, anim_folders, scale_factor=1.0, flip_images=False):
        super().__init__()

        # --- 1. 애니메이션 로딩 (매개변수 사용) ---
        self.animations = {}
        self.animations['Idle'] = load_animation_frames(
            anim_folders['Idle'], scale_factor, flip_images
        )
        self.animations['Walk'] = load_animation_frames(
            anim_folders['Walk'], scale_factor, flip_images
        )
        # (다른 애니메이션도 anim_folders 딕셔너리를 통해 추가 가능)

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
            self.image = pygame.Surface((50, 100))  # 임시 크기
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        # [수정] 플레이어 처음 위치 (매개변수 사용)
        self.rect.midbottom = start_pos

        self.speed = 5
        self.is_moving = False

        # [수정] 조작 키 저장 (매개변수 사용)
        self.key_left = controls[0]
        self.key_right = controls[1]
        # (펀치 키 등은 controls[2], controls[3] 등으로 확장 가능)

    def animate(self):
        """현재 상태에 맞춰 애니메이션을 재생합니다."""
        now = pygame.time.get_ticks()

        frames = self.animations.get(self.current_state, self.animations.get('Idle'))

        if not frames:
            return

        if now - self.last_update_time > self.animation_delay:
            self.last_update_time = now
            self.current_frame = (self.current_frame + 1) % len(frames)

            new_image = frames[self.current_frame]

            old_midbottom = self.rect.midbottom
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom

    def update(self):
        """플레이어 입력 처리 및 상태 업데이트."""
        keys = pygame.key.get_pressed()

        self.is_moving = False

        # [수정] 저장된 조작 키 사용
        if keys[self.key_left]:
            self.rect.x -= self.speed
            self.is_moving = True
        if keys[self.key_right]:
            self.rect.x += self.speed
            self.is_moving = True

        # --- 상태 결정 ---
        if self.is_moving:
            self.current_state = 'Walk'
        else:
            self.current_state = 'Idle'

        # --- 화면 경계 처리 ---
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

        # --- 애니메이션 실행 ---
        self.animate()


# --- 4. 게임 객체 생성 ---

# [수정] 플레이어 1 설정
P1_SCALE = 0.5  # <--- 요청하신 크기 조절 (50%)
P1_START_POS = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 30)  # 왼쪽
P1_CONTROLS = (pygame.K_a, pygame.K_d)  # A, D 키
P1_ANIM_FOLDERS = {'Idle': 'Idle', 'Walk': 'Walk'}  # Idle, Walk 폴더 사용

player1 = Player(P1_START_POS, P1_CONTROLS, P1_ANIM_FOLDERS, P1_SCALE, flip_images=False)

# [수정] 플레이어 2 설정
P2_SCALE = 0.5  # P1과 동일한 크기
P2_START_POS = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 30)  # 오른쪽
P2_CONTROLS = (pygame.K_LEFT, pygame.K_RIGHT)  # 화살표 키
P2_ANIM_FOLDERS = {'Idle': 'Idle', 'Walk': 'Walk'}  # P1과 동일한 애니메이션 사용

player2 = Player(P2_START_POS, P2_CONTROLS, P2_ANIM_FOLDERS, P2_SCALE, flip_images=True)  # 좌우 반전

# 스프라이트 그룹 생성
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)  # <--- 플레이어 2 추가

# --- 5. 메인 게임 루프 ---
running = True
while running:
    # 1) 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2) 게임 로직 업데이트
    all_sprites.update()  # player1과 player2의 update()가 모두 호출됨

    # 3) 화면 그리기
    screen.fill(BLACK)
    all_sprites.draw(screen)  # player1과 player2를 모두 그림

    # 4) 화면 업데이트
    pygame.display.flip()

    # 5) FPS 설정
    clock.tick(60)

# --- 6. 게임 종료 ---
pygame.quit()