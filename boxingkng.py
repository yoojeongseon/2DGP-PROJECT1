import pygame
import os


# --- 0. 헬퍼 함수 (애니메이션 로드) ---

def load_animation_frames(folder_path):
    """폴더 경로를 받아 이미지 프레임 리스트를 반환합니다."""
    frames = []
    if not os.path.exists(folder_path):
        print(f"경고: 애니메이션 폴더를 찾을 수 없습니다: {folder_path}")
        return frames

    # 폴더 내의 파일들을 이름순으로 정렬 (예: 0.png, 1.png, 2.png...)
    file_names = os.listdir(folder_path)

    # 파일명을 숫자로 변환하여 정렬 (예: '10.png'가 '2.png'보다 뒤에 오도록)
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
pygame.display.set_caption("2DGP 프로젝트 - 2주차 (애니메이션 적용)")

# FPS 설정을 위한 Clock 객체
clock = pygame.time.Clock()

# --- 2. 색상 정의 ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# --- 3. 플레이어 클래스 정의 (2주차 핵심 목표) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # --- 1. 애니메이션 로딩 ---
        # 이미지 폴더들이 이 스크립트와 같은 위치에 있다고 가정
        self.animations = {}  # 모든 애니메이션을 저장할 딕셔너리
        self.animations['Idle'] = load_animation_frames('Idle')
        self.animations['Walk'] = load_animation_frames('Walk')
        # (3주차에 'PunchLeft' 등 다른 애니메이션도 여기에 추가)

        # --- 2. 상태 및 애니메이션 관리 ---
        self.current_state = 'Idle'  # 플레이어의 현재 상태
        self.current_frame = 0  # 현재 애니메이션 프레임 인덱스
        self.last_update_time = pygame.time.get_ticks()  # 애니메이션 속도 조절용
        self.animation_delay = 100  # 100ms마다 프레임 변경 (0.1초)

        # --- 3. 이미지 및 위치 ---
        if self.animations['Idle']:
            self.image = self.animations['Idle'][0]  # 첫 이미지는 Idle의 0번째 프레임
            self.rect = self.image.get_rect()
        else:
            # 로드 실패 시 임시 사각형
            print("오류: 'Idle' 애니메이션을 찾을 수 없습니다. 임시 사각형으로 대체합니다.")
            self.image = pygame.Surface((50, 100))
            self.image.fill(RED)
            self.rect = self.image.get_rect()

        # 플레이어 처음 위치
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30

        self.speed = 5
        self.is_moving = False  # 현재 움직이는 중인지 확인

        def animate(self):
            """현재 상태에 맞춰 애니메이션을 재생합니다."""
            now = pygame.time.get_ticks()

            # 현재 상태에 맞는 애니메이션 프레임 리스트 가져오기
            frames = self.animations.get(self.current_state, self.animations.get('Idle'))

            if not frames:  # 애니메이션 프레임이 없으면 중단
                return

            # 마지막 업데이트로부터 'animation_delay' 시간이 지났는지 확인
            if now - self.last_update_time > self.animation_delay:
                self.last_update_time = now

                # 다음 프레임으로 이동 (루프)
                self.current_frame = (self.current_frame + 1) % len(frames)

                # 현재 이미지 업데이트
                new_image = frames[self.current_frame]

                # 이미지 교체 시 위치 고정 (중요!)
                old_midbottom = self.rect.midbottom
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.midbottom = old_midbottom

                def update(self):
                    """플레이어 입력 처리 및 상태 업데이트."""
                    keys = pygame.key.get_pressed()

                    self.is_moving = False  # 매 프레임마다 초기화

                    # 2D 복싱 게임은 보통 좌우로만 움직입니다. (상하 이동 제거)
                    if keys[pygame.K_LEFT]:
                        self.rect.x -= self.speed
                        self.is_moving = True
                    if keys[pygame.K_RIGHT]:
                        self.rect.x += self.speed
                        self.is_moving = True

                    # (만약 상하 이동이 필요하다면 아래 주석을 해제하세요)
                    # if keys[pygame.K_UP]:
                    #     self.rect.y -= self.speed
                    #     self.is_moving = True
                    # if keys[pygame.K_DOWN]:
                    #     self.rect.y += self.speed
                    #     self.is_moving = True

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

                # ( draw 메서드는 Sprite Group을 사용하므로 Player 클래스 내에는 필요 없습니다 )

            # --- 4. 게임 객체 생성 ---
            player1 = Player()

            # 스프라이트 그룹 생성
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player1)  # 플레이어를 그룹에 추가

            # --- 5. 메인 게임 루프 ---
            running = True
            while running:
                # 1) 이벤트 처리 (종료)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 창 닫기 버튼을 눌렀을 때
                        running = False

                # 2) 게임 로직 업데이트
                all_sprites.update()  # 그룹의 모든 스프라이트(현재 player1)의 update() 메서드 호출

                # 3) 화면 그리기
                screen.fill(BLACK)  # 화면을 검은색으로 채우기
                all_sprites.draw(screen)  # 그룹의 모든 스프라이트를 화면에 그림

                # 4) 화면 업데이트
                pygame.display.flip()  # 변경된 내용을 화면에 반영

                # 5) FPS 설정
                clock.tick(60)  # 초당 60 프레임으로 제한

            # --- 6. 게임 종료 ---
            pygame.quit()