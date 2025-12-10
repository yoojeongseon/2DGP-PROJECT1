# (파일: visual_effects.py)

import pygame


class VisualEffect(pygame.sprite.Sprite):
    """애니메이션을 한 번 재생하고 사라지는 이펙트 스프라이트"""

    # [수정] flip=False 매개변수 추가
    def __init__(self, pos, frames, flip=False):
        super().__init__()

        # [수정] flip이 True면 모든 프레임을 좌우 반전시킴
        if flip:
            self.frames = [pygame.transform.flip(img, True, False) for img in frames]
        else:
            self.frames = frames

        self.current_frame = 0
        self.animation_speed = 0.5

        if self.frames:
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = pos
        else:
            self.kill()

    def update(self):
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.current_frame)]