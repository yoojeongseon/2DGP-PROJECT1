# (수정된 파일: attacks.py)

# [수정] player.py 대신 utils.py 에서 헬퍼 함수를 가져옵니다.
from utils import load_animation_frames

import pygame

class Attack:
    """
    공격 모션의 데이터(프레임, 데미지)를 관리하는 클래스
    """

    def __init__(self, folder_name, damage, scale_factor=1.0, flip_images=False):
        # 1. 각 공격이 자신의 애니메이션 프레임을 로드합니다.
        self.frames = load_animation_frames(folder_name, scale_factor, flip_images)

        # 2. 각 공격이 자신의 프레임 수와 데미지를 저장합니다.
        self.frame_count = len(self.frames)
        self.damage = damage