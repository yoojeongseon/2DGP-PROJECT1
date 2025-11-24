# (파일: visual_effects.py)

import pygame


class VisualEffect(pygame.sprite.Sprite):
    """애니메이션을 한 번 재생하고 사라지는 이펙트 스프라이트"""

    def __init__(self, pos, frames, flip=False):  # [수정] flip 파라미터 추가
        super().__init__()

        # [추가] flip이 True면 전달받은 프레임들을 모두 좌우 반전시킴
        if flip:
            # 원본 리스트를 건드리지 않기 위해 새로운 리스트로 생성
            self.frames = [pygame.transform.flip(img, True, False) for img in frames]
        else:
            self.frames = frames

        self.current_frame = 0
        self.animation_speed = 0.5  # 속도 조절

        # 첫 번째 이미지 설정
        if self.frames:
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.center = pos  # 이펙트가 나타날 위치 (중심 기준)
        else:
            self.kill()

    def update(self):
        # 애니메이션 프레임 진행
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.kill()  # 애니메이션이 끝나면 스프라이트 삭제
        else:
            self.image = self.frames[int(self.current_frame)]