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
    def __init__(self, start_pos, controls, anim_folders, scale_factor=1.0, flip_images=False):
        super().__init__()

        # --- 1. 애니메이션 로딩 ---
        self.animations = {}
        self.animations['Idle'] = load_animation_frames(
            anim_folders['Idle'], scale_factor, flip_images
        )
        self.animations['Walk'] = load_animation_frames(
            anim_folders['Walk'], scale_factor, flip_images
        )
        # --- [추가] 공격 애니메이션 로드 ---
        # (폴더 이름이 'Jab', 'Straight', 'Uppercut'이라고 가정)
        self.animations['Jab'] = load_animation_frames(
            anim_folders.get('Jab', 'Jab'), scale_factor, flip_images  # .get으로 오류 방지
        )
        self.animations['Straight'] = load_animation_frames(
            anim_folders.get('Straight', 'Straight'), scale_factor, flip_images
        )
        self.animations['Uppercut'] = load_animation_frames(
            anim_folders.get('Uppercut', 'Uppercut'), scale_factor, flip_images
        )

        # --- [추가] 어떤 상태가 반복되어야 하는지 정의 ---
        self.looping_states = ['Idle', 'Walk']

        # --- 2. 상태 및 애니메이션 관리 ---
        self.current_state = 'Idle'
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_delay = 100

        # --- 3. 이미지 및 위치 (기존과 동일) ---
        if self.animations['Idle']:
            self.image = self.animations['Idle'][0]
            self.rect = self.image.get_rect()
        else:
            print("오류: 'Idle' 애니메이션을 찾을 수 없습니다. 임시 사각형으로 대체합니다.")
            self.image = pygame.Surface((50, 100))
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        self.rect.midbottom = start_pos
        self.speed = 5
        self.is_moving = False

        # --- [수정] 조작 키 저장 ---
        self.key_left = controls[0]
        self.key_right = controls[1]
        # --- [추가] 공격 키 저장 ---
        self.key_jab = controls[2]
        self.key_straight = controls[3]
        self.key_uppercut = controls[4]

    def animate(self):
        """현재 상태에 맞춰 애니메이션을 재생합니다. (반복/한번만 재생 구분)"""
        now = pygame.time.get_ticks()

        # 현재 상태의 애니메이션 프레임 목록 가져오기
        current_frames = self.animations.get(self.current_state, self.animations.get('Idle'))
        if not current_frames:
            return

        # 딜레이 시간이 지나지 않았으면 아무것도 안 함
        if now - self.last_update_time <= self.animation_delay:
            return

        self.last_update_time = now

        # --- [수정] 반복 상태와 한 번만 재생하는 상태 구분 ---

        is_looping = self.current_state in self.looping_states

        if is_looping:
            # 'Idle', 'Walk'는 계속 반복
            self.current_frame = (self.current_frame + 1) % len(current_frames)
        else:
            # 'Jab' 등은 한 번만 재생
            self.current_frame += 1
            # 애니메이션이 끝났는지 확인
            if self.current_frame >= len(current_frames):
                self.current_state = 'Idle'  # <--- (중요!) Idle 상태로 복귀
                self.current_frame = 0  # 프레임 리셋

        # --- 이미지 업데이트 ---
        # (상태가 'Idle'로 방금 바뀌었을 수 있으므로, 프레임 목록을 다시 가져옴)
        final_frames = self.animations.get(self.current_state, self.animations.get('Idle'))

        # (프레임이 리셋되어 0이 되었을 때 final_frames[0]을 안전하게 참조)
        self.image = final_frames[self.current_frame]

        # 위치 고정
        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def update(self):
        """플레이어 입력 처리 및 상태 업데이트."""
        keys = pygame.key.get_pressed()

        # --- [수정] 상태 머신 로직 ---

        # 1. 현재 '한 번만 재생'하는 애니메이션(공격)이 실행 중인지 확인
        is_busy = self.current_state not in self.looping_states

        # 2. (중요!) 공격 중이면, 다른 모든 입력을 무시하고 애니메이션만 재생
        if is_busy:
            self.animate()
            return  # <- update 함수를 여기서 종료

        # 3. 공격 중이 아닐 때만 새 입력을 받음 (공격이 이동보다 우선순위 높음)
        if keys[self.key_jab]:
            self.current_state = 'Jab'
            self.current_frame = 0  # 애니메이션 처음부터 시작
        elif keys[self.key_straight]:
            self.current_state = 'Straight'
            self.current_frame = 0
        elif keys[self.key_uppercut]:
            self.current_state = 'Uppercut'
            self.current_frame = 0

        # 4. 공격 키가 눌리지 않았을 때만 이동 처리
        else:
            self.is_moving = False
            if keys[self.key_left]:
                self.rect.x -= self.speed
                self.is_moving = True
            if keys[self.key_right]:
                self.rect.x += self.speed
                self.is_moving = True

            # 이동 상태에 따라 'Walk' 또는 'Idle' 결정
            if self.is_moving:
                self.current_state = 'Walk'
            else:
                self.current_state = 'Idle'

        # --- 화면 경계 처리 ---
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH
        # ... (상하 경계는 필요시 주석 해제) ...

        # --- 애니메이션 실행 ---
        self.animate()


# --- 4. 게임 객체 생성 ---

# [수정] 플레이어 1 설정
# --- 4. 게임 객체 생성 ---

# [수정] 플레이어 1 설정 (A,D 이동 / W,E,R 공격)
P1_SCALE = 0.5
P1_START_POS = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 30)
# (Left, Right, Jab, Straight, Uppercut)
P1_CONTROLS = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e, pygame.K_r)

# [수정] 애니메이션 폴더명 지정 (사용자님의 폴더명으로 변경)
P1_ANIM_FOLDERS = {
    'Idle': 'Idle',
    'Walk': 'Walk',
    'Jab': 'PunchLeft',     # <-- 'Jab' 상태일 때 'PunchLeft' 폴더 사용
    'Straight': 'PunchRight', # <-- 'Straight' 상태일 때 'PunchRight' 폴더 사용
    'Uppercut': 'PunchUp'     # <-- 'Uppercut' 상태일 때 'PunchUp' 폴더 사용
}

player1 = Player(P1_START_POS, P1_CONTROLS, P1_ANIM_FOLDERS, P1_SCALE, flip_images=False)

# [수정] 플레이어 2 설정 (화살표 이동 / U,I,O 공격)
P2_SCALE = 0.5
P2_START_POS = (SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT - 30)
# (Left, Right, Jab, Straight, Uppercut)
P2_CONTROLS = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_u, pygame.K_i, pygame.K_o)
# [수정] P1과 동일한 폴더 매핑 사용 (flip_images=True로 반전됨)
P2_ANIM_FOLDERS = P1_ANIM_FOLDERS

player2 = Player(P2_START_POS, P2_CONTROLS, P2_ANIM_FOLDERS, P2_SCALE, flip_images=True)


# 스프라이트 그룹 생성 (기존과 동일)
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)

# --- 5. 메인 게임 루프 (기존과 동일) ---
# ... (이하 동일) ...

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