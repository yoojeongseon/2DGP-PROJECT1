# (파일: title_screen.py)

import pygame
import os


class TitleScreen:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        # 폰트 설정
        self.title_font = pygame.font.Font(None, 100)  # 큰 폰트
        self.sub_font = pygame.font.Font(None, 50)  # 작은 폰트

        # --- 이미지 로드 (파일이 없으면 예외 처리) ---
        self.bg_image = None
        try:
            # 'assets' 폴더나 같은 폴더에 'title_bg.png'가 있다고 가정
            image_path = os.path.join("assets", "title_bg.png")
            if os.path.exists(image_path):
                img = pygame.image.load(image_path).convert()
                self.bg_image = pygame.transform.scale(img, (screen_width, screen_height))
            else:
                print("알림: 타이틀 배경 이미지를 찾을 수 없습니다. (검은색 배경 사용)")
        except Exception as e:
            print(f"이미지 로드 에러: {e}")

        # --- 깜빡임 효과 변수 ---
        self.blink_timer = 0
        self.show_text = True

    def handle_input(self, event):
        """스페이스바를 누르면 게임 시작(PLAY) 신호 반환"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "PLAY"
        return None

    def update(self):
        """텍스트 깜빡임 효과 업데이트"""
        self.blink_timer += 1
        if self.blink_timer >= 30:  # 30프레임(0.5초)마다 상태 변경
            self.show_text = not self.show_text
            self.blink_timer = 0

    def draw(self, screen):
        # 1. 배경 그리기
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill((20, 20, 40))  # 이미지가 없으면 짙은 남색 배경

        # 2. 타이틀 텍스트 (그림자가 있는 효과)
        text_string = "SUPER FIGHTER"

        # 그림자 (검은색)
        shadow_surf = self.title_font.render(text_string, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(self.width // 2 + 5, self.height // 3 + 5))
        screen.blit(shadow_surf, shadow_rect)

        # 본문 (빨간색)
        text_surf = self.title_font.render(text_string, True, (255, 50, 50))
        text_rect = text_surf.get_rect(center=(self.width // 2, self.height // 3))
        screen.blit(text_surf, text_rect)

        # 3. 시작 안내 텍스트 (깜빡임 효과)
        if self.show_text:
            start_surf = self.sub_font.render("Press SPACE to Start", True, (255, 255, 255))
            start_rect = start_surf.get_rect(center=(self.width // 2, self.height * 0.7))
            screen.blit(start_surf, start_rect)