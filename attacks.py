# (파일: attacks.py)

from utils import load_animation_frames
import pygame


class Attack:
    """
    공격 모션의 데이터(프레임, 데미지, 타격 시점, 범위)를 관리하는 클래스
    """

    def __init__(self, folder_name, damage, hit_frame, hitbox_rect, scale_factor=1.0, flip_images=False):
        """
        hit_frame: 공격 판정이 시작되는 프레임 번호 (예: 1)
        hitbox_rect: 공격 판정 범위 (예: pygame.Rect(50, 20, 40, 30))
        """

        # 1. 애니메이션 프레임 로드
        self.frames = load_animation_frames(folder_name, scale_factor, flip_images)
        self.frame_count = len(self.frames)

        # 2. 데미지 정보
        self.damage = damage

        # --- [추가] 3. 타격 판정 정보 ---
        self.hit_frame = hit_frame

        # 4. 공격 범위 (Hitbox)
        # (주의: 이 Rect는 (0,0) 기준의 상대적 위치와 크기입니다)
        base_hitbox = pygame.Rect(hitbox_rect)

        # 만약 이미지가 좌우 반전(flip_images)되었다면, hitbox도 좌우 반전시킵니다.
        if flip_images:
            # (이 부분은 나중에 플레이어의 실제 너비(width)를 알아야 정확히 계산 가능합니다)
            # (우선은 x좌표만 반전시킨다고 가정)
            # 예: 원본 hitbox가 (50, 20, 40, 30)이고, 플레이어 너비가 80이라면
            # 반전된 x좌표 = 80 - 50 - 40 = -10
            # (이 부분은 나중에 Player 클래스에서 처리하는 것이 더 정확할 수 있습니다)

            # 지금은 간단히 x 위치만 음수로 바꾸는 임시 처리를 합니다.
            # (이 부분은 Player 클래스에서 hitbox 위치를 계산할 때 flip 여부를 고려해야 함)
            self.hitbox = base_hitbox
        else:
            self.hitbox = base_hitbox