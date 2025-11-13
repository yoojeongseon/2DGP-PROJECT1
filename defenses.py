# (파일: defenses.py)

import pygame
from utils import load_animation_frames  # utils.py 에서 헬퍼 함수를 가져옵니다.


class Defense:
    """
    방어/회피 모션의 데이터(프레임)를 관리하는 클래스
    """

    def __init__(self, folder_name, scale_factor=1.0, flip_images=False):
        # 1. 방어 동작의 애니메이션 프레임을 로드합니다.
        self.frames = load_animation_frames(folder_name, scale_factor, flip_images)
        self.frame_count = len(self.frames)

        # (나중에 여기에 '데미지 감소율', '무적 시간' 등을 추가할 수 있습니다.)