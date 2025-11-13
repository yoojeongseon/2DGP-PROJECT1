# (파일: attacks.py)

from utils import load_animation_frames
import pygame


class Attack:
    """
    공격 모션의 데이터(프레임, 데미지, 타격 시점, 범위, KO여부)를 관리
    """

    def __init__(self, folder_name, damage, hit_frame, hitbox_rect,
                 scale_factor=1.0, flip_images=False, is_ko_move=False):  # <-- [수정]

        self.frames = load_animation_frames(folder_name, scale_factor, flip_images)
        self.frame_count = len(self.frames)

        # 2. 데미지 정보
        self.damage = damage
        self.is_ko_move = is_ko_move  # <-- [수정] KO 기술인지 여부 저장

        # 3. 타격 판정 정보
        self.hit_frame = hit_frame

        # 4. 공격 범위 (Hitbox)
        self.hitbox = pygame.Rect(hitbox_rect)

        # (참고: hitbox 좌우 반전은 Player 클래스 __init__에서 처리하는 것이 더 정확합니다)