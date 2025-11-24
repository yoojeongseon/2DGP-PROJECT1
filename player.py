# (파일: player.py - 넉백 기능 추가)

import pygame
import os
from attacks import Attack
from utils import load_animation_frames
from defenses import Defense
from effects import Effect


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos, controls, anim_folders, screen_width, scale_factor=1.0, flip_images=False):
        super().__init__()

        self.screen_width = screen_width
        self.flip_images = flip_images

        # --- 1. 애니메이션 로딩 ---
        self.animations = {}
        self.animations['Idle'] = load_animation_frames(anim_folders['Idle'], scale_factor, flip_images)
        self.animations['Walk'] = load_animation_frames(anim_folders['Walk'], scale_factor, flip_images)
        self.animations['KO'] = load_animation_frames(anim_folders.get('KO', 'KO'), scale_factor, flip_images)

        # --- 1-2. 공격 모션 로딩 ---
        self.attacks = {}
        self.attacks['Jab'] = Attack(
            folder_name=anim_folders.get('Jab', 'Jab'),
            damage=10, hit_frame=1, hitbox_rect=pygame.Rect(170, 120, 75, 30),
            scale_factor=scale_factor, flip_images=flip_images, is_ko_move=False
        )
        self.attacks['Straight'] = Attack(
            folder_name=anim_folders.get('Straight', 'Straight'),
            damage=20, hit_frame=2, hitbox_rect=pygame.Rect(170, 120, 70, 30),
            scale_factor=scale_factor, flip_images=flip_images, is_ko_move=False
        )
        self.attacks['Uppercut'] = Attack(
            folder_name=anim_folders.get('Uppercut', 'Uppercut'),
            damage=0, hit_frame=1, hitbox_rect=pygame.Rect(170, 120, 55, 50),
            scale_factor=scale_factor, flip_images=flip_images, is_ko_move=True
        )

        # --- 1-3. 방어 모션 로딩 ---
        self.defenses = {}
        self.defenses['Blocking'] = Defense(anim_folders.get('Blocking', 'Blocking'), scale_factor, flip_images)

        # --- 1-4. 효과(Effect) 로딩 ---
        self.effects = {}
        self.effects['Dizzy'] = Effect(anim_folders.get('Dizzy', 'Dizzy'), scale_factor, flip_images)

        self.looping_states = ['Idle', 'Walk', 'Blocking']

        # --- 2. 상태 및 애니메이션 관리 ---
        self.current_state = 'Idle'
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.base_animation_delay = 100

        # --- 3. 이미지 및 위치 ---
        if self.animations['Idle']:
            self.image = self.animations['Idle'][0]
            self.rect = self.image.get_rect()
        else:
            print("오류: 'Idle' 애니메이션을 찾을 수 없습니다. 임시 사각형으로 대체합니다.")
            self.image = pygame.Surface((50, 100));
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()

        self.rect.midbottom = start_pos
        self.speed = 5
        self.is_moving = False

        # --- Hurtbox 로직 ---
        self.hurtbox_relative_P1 = pygame.Rect(150, 100, 40, 90)
        self.hurtbox_absolute = self.hurtbox_relative_P1.copy()
        self.hurtbox_absolute.topleft = (self.rect.x + self.hurtbox_relative_P1.x,
                                         self.rect.y + self.hurtbox_relative_P1.y)

        # --- 4. 조작 키 저장 ---
        self.key_left = controls[0]
        self.key_right = controls[1]
        self.key_jab = controls[2]
        self.key_straight = controls[3]
        self.key_uppercut = controls[4]
        self.key_block = controls[5]

        # --- 5. 체력, 각성 등 ---
        self.max_hp = 100
        self.hp = 100
        self.is_alive = True
        self.has_hit = False
        self.is_awakened = False

        # --- [추가] 넉백 속도 변수 ---
        self.knockback_velocity = 0

    def animate(self):
        if self.is_awakened:
            current_delay = int(self.base_animation_delay / 1.5)
        else:
            current_delay = self.base_animation_delay

        now = pygame.time.get_ticks()

        if now - self.last_update_time <= current_delay:
            return
        self.last_update_time = now

        is_looping = self.current_state in self.looping_states
        current_frames = []

        if is_looping:
            current_frames = self.animations.get(self.current_state)
            if self.current_state == 'Blocking':
                if 'Blocking' in self.defenses and self.defenses['Blocking'].frames:
                    current_frames = self.defenses['Blocking'].frames
                else:
                    current_frames = self.animations.get('Idle')
            if not current_frames:
                current_frames = self.animations.get('Idle')
        else:
            if self.current_state in self.attacks:
                current_frames = self.attacks[self.current_state].frames
            elif self.current_state in self.effects:
                current_frames = self.effects[self.current_state].frames
            else:
                current_frames = self.animations.get(self.current_state, self.animations['Idle'])

        if not current_frames:
            self.current_state = 'Idle'
            current_frames = self.animations['Idle']
            if not current_frames: return

        if is_looping:
            self.current_frame = (self.current_frame + 1) % len(current_frames)
        else:
            if self.current_state == 'KO':
                if self.current_frame < len(current_frames) - 1:
                    self.current_frame += 1
                else:
                    self.current_frame = len(current_frames) - 1
            else:
                self.current_frame += 1
                if self.current_frame >= len(current_frames):
                    if self.current_state == 'Dizzy':
                        self.current_state = 'Idle'
                        self.current_frame = 0
                        self.is_awakened = True
                        print("AWAKENING ACTIVATED!")
                    else:
                        self.current_state = 'Idle'
                        self.current_frame = 0

        if not self.is_alive and self.current_state != 'KO':
            self.current_state = 'Idle'

        safe_frame = min(self.current_frame, len(current_frames) - 1)

        if self.current_state == 'Idle':
            self.image = self.animations['Idle'][self.current_frame % len(self.animations['Idle'])]
        elif current_frames:
            self.image = current_frames[safe_frame]
        else:
            self.image = self.animations['Idle'][0]

        old_midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def update(self):
        """플레이어 입력 처리 및 상태 업데이트."""

        # --- [추가] 넉백 물리 적용 (가장 먼저 처리) ---
        if self.knockback_velocity != 0:
            self.rect.x += self.knockback_velocity
            self.knockback_velocity *= 0.85  # 마찰력 (속도가 점점 줄어듦)
            if abs(self.knockback_velocity) < 0.5:
                self.knockback_velocity = 0

        # 화면 경계 처리 (넉백으로 나가는 것 방지)
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.screen_width: self.rect.right = self.screen_width

        # KO나 Dizzy 상태면 조작 불가 (애니메이션만 재생)
        if not self.is_alive or self.current_state in ['KO', 'Dizzy']:
            self.animate()
        else:
            keys = pygame.key.get_pressed()
            is_busy = self.current_state not in self.looping_states

            if is_busy:
                self.animate()
            else:
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

                # 이동 입력으로 인한 경계 처리는 위에서 한 번 했지만,
                # 키 입력으로 또 움직였을 수 있으므로 안전하게 한 번 더 체크하거나
                # 위쪽의 경계 처리를 이 아래로 옮겨도 됩니다. (여기서는 안전하게 둠)
                if self.rect.left < 0: self.rect.left = 0
                if self.rect.right > self.screen_width: self.rect.right = self.screen_width

                self.animate()

        # --- Hurtbox 갱신 ---
        current_hurtbox_relative = self.hurtbox_relative_P1.copy()
        if self.flip_images:
            current_hurtbox_relative.x = self.rect.width - current_hurtbox_relative.x - current_hurtbox_relative.width

        self.hurtbox_absolute.x = self.rect.x + current_hurtbox_relative.x
        self.hurtbox_absolute.y = self.rect.y + current_hurtbox_relative.y

    def take_damage(self, damage):
        if not self.is_alive: return

        if self.current_state == 'Blocking':
            print("BLOCK!")
            # [추가] 방어 성공 시에도 살짝 밀림 (선택 사항)
            knockback_force = 5 if self.flip_images else -5
            # self.knockback_velocity = knockback_force
            return

        # [추가] 데미지 입을 때 넉백 적용
        # P1(flip=False)은 왼쪽으로(-), P2(flip=True)는 오른쪽으로(+) 밀려나야 함
        # 넉백 강도: 15
        knockback_force = 15
        if self.flip_images:  # P2인 경우 (오른쪽 -> 왼쪽 보고 있음)
            self.knockback_velocity = knockback_force  # 오른쪽으로 밀림 (+)
        else:  # P1인 경우 (왼쪽 -> 오른쪽 보고 있음)
            self.knockback_velocity = -knockback_force  # 왼쪽으로 밀림 (-)

        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            self.current_state = 'KO'
            self.current_frame = 0
            print("KO!")
        elif self.hp <= 30 and not self.is_awakened:
            self.current_state = 'Dizzy'
            self.current_frame = 0
            self.has_hit = False
            print("HP low! Triggering Dizzy...")
        else:
            print(f"Hit! HP left: {self.hp}")

    def force_ko(self):
        """HP와 상관없이 즉시 KO 상태가 됩니다."""
        if not self.is_alive: return

        print("KO PUNCH LANDED!")

        # [추가] KO 시 강한 넉백
        knockback_force = 30
        if self.flip_images:
            self.knockback_velocity = knockback_force
        else:
            self.knockback_velocity = -knockback_force

        self.hp = 0
        self.is_alive = False
        self.current_state = 'KO'
        self.current_frame = 0

    def get_absolute_hitbox(self):
        if self.current_state not in self.attacks:
            return None

        current_attack = self.attacks[self.current_state]

        if self.current_frame != current_attack.hit_frame:
            return None

        relative_box = current_attack.hitbox.copy()

        if self.flip_images:
            relative_box.x = self.rect.width - relative_box.x - relative_box.width

        absolute_box = relative_box.move(self.rect.topleft)
        return absolute_box