# (파일: visual_effects.py)

import pygame


class VisualEffect(pygame.sprite.Sprite):
    """애니메이션을 한 번 재생하고 사라지는 이펙트 스프라이트"""

    def __init__(self, pos, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = 0.5  # 속도 조절 (0.5 = 2번 호출될 때 1프레임 넘어감)

        # 첫 번째 이미지 설정
        if self.frames:
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = pos  # 이펙트가 나타날 위치
        else:
            self.kill()  # 이미지가 없으면 바로 삭제

    def update(self):
        # 애니메이션 프레임 진행
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.kill()  # 애니메이션이 끝나면 스프라이트 삭제 (메모리 해제)
        else:
            self.image = self.frames[int(self.current_frame)]