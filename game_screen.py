# (파일: game_screen.py)

import pygame
import os
from player import Player
from collisions import handle_player_collisions
from utils import load_animation_frames


class GameScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # --- 폰트 및 배경 ---
        self.result_font = pygame.font.Font(None, 80)
        self.guide_font = pygame.font.Font(None, 40)

        try:
            self.bg_image = pygame.image.load(os.path.join("Backgrounds", "game.png")).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height))
        except:
            print("게임 배경 이미지를 찾을 수 없습니다.")
            self.bg_image = None

        # --- [기존 코드 반영] 이펙트 로드 ---
        self.effect_frames = {
            'BlockEffect': load_animation_frames('BlockEffect', scale_factor=2.0),
            'HitEffect': load_animation_frames('HitEffect', scale_factor=2.0)
        }
        self.effect_group = pygame.sprite.Group()

        # --- [기존 코드 반영] 플레이어 생성 ---
        P1_SCALE = 0.5
        P1_START_POS = (screen_width // 4, screen_height - 30)
        P1_CONTROLS = (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_s)

        ANIM_FOLDERS = {
            'Idle': 'Idle', 'Walk': 'Walk', 'Jab': 'PunchLeft', 'Straight': 'PunchRight',
            'Uppercut': 'PunchUp', 'Blocking': 'Blocking', 'Dizzy': 'Dizzy', 'KO': 'KO'
        }

        self.player1 = Player(P1_START_POS, P1_CONTROLS, ANIM_FOLDERS, screen_width, P1_SCALE, flip_images=False)

        P2_SCALE = 0.5
        P2_START_POS = (screen_width * 3 // 4, screen_height - 30)
        P2_CONTROLS = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_DOWN)

        self.player2 = Player(P2_START_POS, P2_CONTROLS, ANIM_FOLDERS, screen_width, P2_SCALE, flip_images=True)

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)

        # 게임 상태 변수
        self.game_over = False
        self.winner_text = ""

    def handle_events(self, events):
        """게임 중 키 입력 처리"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 게임 오버 상태일 때만 R(재시작)이나 ESC(나가기) 가능
                if self.game_over:
                    if event.key == pygame.K_r:
                        return "RESTART"
                    elif event.key == pygame.K_ESCAPE:
                        return "TITLE"
        return "PLAY"

    def update(self):
        """게임 로직 업데이트"""
        self.all_sprites.update()
        self.effect_group.update()  # 이펙트 업데이트

        # [기존 코드 반영] 타격 판정 (이펙트 그룹과 프레임 전달)
        handle_player_collisions(self.player1, self.player2, self.effect_group, self.effect_frames)

        # 승패 판정 로직
        if not self.game_over:
            # 둘 중 하나가 죽었고, KO 애니메이션 상태라면 게임오버 처리
            if (not self.player1.is_alive and self.player1.current_state == 'KO') or \
                    (not self.player2.is_alive and self.player2.current_state == 'KO'):
                self.game_over = True
                if not self.player1.is_alive:
                    self.winner_text = "2P WINS!"
                else:
                    self.winner_text = "1P WINS!"

    def draw(self, screen):
        """그리기"""
        # 1. 배경
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # 2. 스프라이트 및 이펙트
        self.all_sprites.draw(screen)
        self.effect_group.draw(screen)

        # 3. 체력바 (각성 효과 적용)
        self.draw_health_bar(screen, 20, 20, self.player1)
        self.draw_health_bar(screen, self.screen_width - 320, 20, self.player2)

        # 4. 게임 오버 텍스트
        if self.game_over:
            self.draw_text_center(screen, self.winner_text, self.result_font, (255, 0, 0), -50)
            self.draw_text_center(screen, "Press R to Restart / ESC to Title", self.guide_font, (255, 255, 255), 50)

    # --- 헬퍼 함수 ---
    def draw_health_bar(self, surface, x, y, player):
        hp = max(0, player.hp)
        max_hp = player.max_hp
        BAR_LENGTH = 300
        BAR_HEIGHT = 20
        fill_percent = (hp / max_hp)
        fill_length = int(BAR_LENGTH * fill_percent)

        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill_length, BAR_HEIGHT)

        # [기존 코드 반영] 각성 상태면 노란색
        bar_color = (255, 255, 0) if player.is_awakened else (0, 255, 0)

        pygame.draw.rect(surface, (255, 0, 0), outline_rect)
        pygame.draw.rect(surface, bar_color, fill_rect)

    def draw_text_center(self, surface, text, font, color, y_offset=0):
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + y_offset))
        surface.blit(text_surface, rect)