# (파일: attacks.py)

# [중요] player.py 파일에서 헬퍼 함수를 가져옵니다.
try:
    from player import load_animation_frames
except ImportError:
    print("오류: player.py 파일을 찾을 수 없거나, 순환 참조 오류일 수 있습니다.")


    # 임시 함수
    def load_animation_frames(folder, scale, flip):
        print(f"임시 함수 호출됨: {folder}")
        return []

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

        # (나중에 여기에 공격 범위(hitbox), 쿨타임 등을 추가할 수 있습니다.)