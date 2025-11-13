# (파일: player.py)

import pygame
import os
from attacks import Attack
from utils import load_animation_frames
from defenses import Defense


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, controls, anim_folders, scale_factor=1.0, flip_images=False):
        super().__init__()

        # --- 1. 기본 애니메이션 로딩 ---
        self.animations = {}
        self.animations['Idle'] = load_animation_frames(
            anim_folders['Idle'], scale_factor, flip_images
        )
        self.animations['Walk'] = load_animation_frames(
            anim_folders['Walk'], scale_factor, flip_images
        )

        # --- [수정] 1-2. 공격 모션 로딩 (Attack 클래스 업그레이드) ---
        self.attacks = {}

        # 잽(Jab): 1번 프레임에, (50, 20) 위치에 40x30 크기로 타격 (예시값)
        self.attacks['Jab'] = Attack(
            folder_name=anim_folders.get('Jab', 'Jab'),
            damage=10,
            hit_frame=1,  # 잽은 1번 프레임(0번 다음)에 타격
            hitbox_rect=pygame.Rect(50, 20, 40, 30),  # (x, y, w, h) - 캐릭터 기준 상대 위치
            scale_factor=scale_factor,
            flip_images=flip_images
        )

        # 스트레이트(Straight): 2번 프레임에, (60, 25) 위치에 50x30 크기로 타격 (예시값)
        self.attacks['Straight'] = Attack(
            folder_name=anim_folders.get('Straight', 'Straight'),
            damage=20,
            hit_frame=2,  # 스트레이트는 2번 프레임에 타격
            hitbox_rect=pygame.Rect(60, 25, 50, 30),
            scale_factor=scale_factor,
            flip_images=flip_images
        )

        # 어퍼컷(Uppercut): 1번 프레임에, (40, 0) 위치에 40x50 크기로 타격 (예시값)
        self.attacks['Uppercut'] = Attack(
            folder_name=anim_folders.get('Uppercut', 'Uppercut'),
            damage=0,  # (어차피 KO 로직)
            hit_frame=1,  # 어퍼컷은 1번 프레임에 타격
            hitbox_rect=pygame.Rect(40, 0, 40, 50),
            scale_factor=scale_factor,
            flip_images=flip_images
        )

        # --- 1-3. 방어 모션 로딩 ---
        self.defenses = {}
        self.defenses['Blocking'] = Defense(
            anim_folders.get('Blocking', 'Blocking'),
            scale_factor,
            flip_images
        )

        self.looping_states = ['Idle', 'Walk', 'Blocking']

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
            self.image.fill((255, 0, 0))  # RED
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
        self.key_block = controls[5]

        # --- 5. 체력 시스템 ---
        self.max_hp = 100
        self.hp = 100
        self.is_alive = True

        # --- 6. 중복 타격 방지 플래그 ---
        self.has_hit = False

    def animate(self):
        """현재 상태에 맞춰 애니메이션을 재생합니다."""
        now = pygame.time.get_ticks()

        if now - self.last_update_time <= self.animation_delay:
            return
        self.last_update_time = now

        is_looping = self.current_state in self.looping_states

        current_frames = []
        is_attack = False

        if is_looping:
            current_frames = self.animations.get(self.current_state)

            if self.current_state == 'Blocking':
                if 'Blocking' in self.defenses and self.defenses['Blocking'].frames:
                    current_frames = self.defenses['Blocking'].frames
                else:
                    print("경고: 'Blocking' 애니메이션을 찾을 수 없습니다.")
                    current_frames = self.animations.get('Idle')

            if not current_frames:
                current_frames = self.animations.get('Idle')

        else:
            if self.current_state in self.attacks:
                current_frames = self.attacks[self.current_state].frames
                is_attack = True
            else:
                current_frames = self.animations.get(self.current_state, self.animations['Idle'])

        if not current_frames:
            self.current_state = 'Idle'
            return

        # --- 애니메이션 재생 ---
        if is_looping:
            self.current_frame = (self.current_frame + 1) % len(current_frames)
        else:
            self.current_frame += 1
            if self.current_frame >= len(current_frames):
                self.current_state = 'Idle'
                self.current_frame = 0

        # --- 이미지 업데이트 ---
        if self.current_state == 'Idle':
            self.image = self.animations['Idle'][self.current_frame % len(self.animations['Idle'])]
        else:
            if self.current_frame < len(current_frames):
                self.image = current_frames[self.current_frame]
            else:
                self.image = self.animations['Idle'][0]
                self.current_state = 'Idle'
                self.current_frame = 0

        # --- 위치 고정 ---
        old_midbottom = self.rect.midbottom
        self.rect = self.image