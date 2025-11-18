# (파일: player.py)

import pygame
import os
from attacks import Attack
from utils import load_animation_frames
from defenses import Defense
from effects import Effect  # <-- effects.py 에서 Effect 클래스 가져오기


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, controls, anim_folders, screen_width, scale_factor=1.0, flip_images=False):
        super().__init__()

        self.screen_width = screen_width

        # --- 1. 기본 애니메이션 로딩 ---
        self.animations = {}
        self.animations['Idle'] = load_animation_frames(
            anim_folders['Idle'], scale_factor, flip_images
        )
        self.animations['Walk'] = load_animation_frames(
            anim_folders['Walk'], scale_factor, flip_images
        )
        # (KO 애니메이션은 나중에 여기에 추가)
        # self.animations['KO'] = ...

        # --- 1-2. 공격 모션 로딩 ---
        self.attacks = {}
        self.attacks['Jab'] = Attack(
            folder_name=anim_folders.get('Jab', 'Jab'),
            damage=10, hit_frame=1, hitbox_rect=pygame.Rect(50, 20, 40, 30),
            scale_factor=scale_factor, flip_images=flip_images, is_ko_move=False
        )
        self.attacks['Straight'] = Attack(
            folder_name=anim_folders.get('Straight', 'Straight'),
            damage=20, hit_frame=2, hitbox_rect=pygame.Rect(60, 25, 50, 30),
            scale_factor=scale_factor, flip_images=flip_images, is_ko_move=False
        )
        self.attacks['Uppercut'] = Attack(
            folder_name=anim_folders.get('Uppercut', 'Uppercut'),
            damage=0, hit_frame=1, hitbox_rect=pygame.Rect(40, 0, 40, 50),
            scale_factor=scale_factor, flip_images=flip_images, is_ko_move=True
        )

        # --- 1-3. 방어 모션 로딩 ---
        self.defenses = {}
        self.defenses['Blocking'] = Defense(
            anim_folders.get('Blocking', 'Blocking'),
            scale_factor,
            flip_images
        )

        # --- 1-4. 효과(Effect) 로딩 ---
        self.effects = {}
        self.effects['Dizzy'] = Effect(
            anim_folders.get('Dizzy', 'Dizzy'),  # 'Dizzy' 폴더 사용
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

        # --- 7. 각성 상태 플래그 ---
        self.is_awakened = False

    def animate(self):
        """현재 상태에 맞춰 애니메이션을 재생합니다."""
        now = pygame.time.get_ticks()

        if now - self.last_update_time <= self.animation_delay:
            return
        self.last_update_time = now

        is_looping = self.current_state in self.looping_states

        current_frames = []

        if is_looping:
            # (Idle, Walk)
            current_frames = self.animations.get(self.current_state)
            # (Blocking)
            if self.current_state == 'Blocking':
                if 'Blocking' in self.defenses and self.defenses['Blocking'].frames:
                    current_frames = self.defenses['Blocking'].frames
                else:
                    current_frames = self.animations.get('Idle')

            if not current_frames:
                current_frames = self.animations.get('Idle')
        else:
            # (공격, 효과, 기타 상태)
            if self.current_state in self.attacks:
                # (Jab, Straight, Uppercut)
                current_frames = self.attacks[self.current_state].frames
            elif self.current_state in self.effects:
                # (Dizzy)
                current_frames = self.effects[self.current_state].frames
            else:
                # (KO 등)
                current_frames = self.animations.get(self.current_state, self.animations['Idle'])

        if not current_frames:
            self.current_state = 'Idle'
            return

        # --- 애니메이션 재생 ---
        if is_looping:
            self.current_frame = (self.current_frame + 1) % len(current_frames)
        else:
            # (한 번만 재생되는 애니메이션: 공격, Dizzy, KO 등)
            self.current_frame += 1
            if self.current_frame >= len(current_frames):

                # 'Dizzy' 애니메이션이 끝났는지 확인
                if self.current_state == 'Dizzy':
                    self.current_state = 'Idle'
                    self.current_frame = 0
                    self.is_awakened = True  # <-- 각성 상태 활성화!
                    print("AWAKENING ACTIVATED!")
                else:
                    self.current_state = 'Idle'
                    self.current_frame = 0

        # --- 이미지 업데이트 ---
        if not self.is_alive and self.current_state != 'KO':
            self.current_state = 'Idle'

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
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def update(self):
        """플레이어 입력 처리 및 상태 업데이트."""
        # 'Dizzy' 중이거나 'KO' 상태면 조작 불가
        if not self.is_alive or self.current_state == 'Dizzy':
            self.animate()  # 애니메이션은 재생
            return

        keys = pygame.key.get_pressed()

        is_busy = self.current_state not in self.looping_states
        if is_busy:
            self.animate()
            return

        # --- 입력 우선순위: 공격 > 방어 > 이동 ---
        if keys[self.key_jab]:
            self.current_state = 'Jab'
            self.current_frame = 0
            self.has_hit = False
        elif keys[self.key_straight]:
            self.current_state = 'Straight'
            self.current_frame = 0
            self.has_hit = False
        elif keys[self.key_uppercut]:
            self.current_state = 'Uppercut'
            self.current_frame = 0
            self.has_hit = False
        elif keys[self.key_block]:
            self.current_state = 'Blocking'
            self.current_frame = 0
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
        if self.rect.right > self.screen_width: self.rect.right = self.screen_width

        self.animate()

    def take_damage(self, damage):
        """피해를 입고 체력을 감소시킵니다."""
        if not self.is_alive: return

        self.hp -= damage

        # 1. KO 판정
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.current_state = 'KO'  # (KO 애니메이션 폴더 필요)
            self.current_frame = 0
            print("KO!")

        # 2. 각성(Dizzy) 판정
        elif self.hp <= 30 and not self.is_awakened:
            self.current_state = 'Dizzy'  # Dizzy 애니메이션 재생
            self.current_frame = 0
            self.has_hit = False
            print("HP low! Triggering Dizzy...")

        # 3. 일반 피격
        else:
            print(f"Hit! HP left: {self.hp}")