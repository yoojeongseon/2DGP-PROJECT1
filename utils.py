# (새 파일: utils.py)
import pygame
import os

def load_animation_frames(folder_path, scale_factor=1.0, flip_images=False):
    """폴더 경로와 배율을 받아 스케일링 및 반전된 이미지 프레임 리스트를 반환합니다."""
    frames = []
    if not os.path.exists(folder_path):
        print(f"경고: 애니메이션 폴더를 찾을 수 없습니다: {folder_path}")
        return frames

    file_names = os.listdir(folder_path)

    try:
        file_names.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or 0))
    except ValueError:
        print(f"경고: {folder_path}의 파일명에서 숫자를 추출할 수 없습니다. 일반 정렬합니다.")
        file_names.sort()

    for file_name in file_names:
        if file_name.endswith(('.png', '.jpg', '.bmp')):
            image_path = os.path.join(folder_path, file_name)
            try:
                image = pygame.image.load(image_path).convert_alpha()
                width = image.get_width()
                height = image.get_height()
                image = pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))
                if flip_images:
                    image = pygame.transform.flip(image, True, False)
                frames.append(image)
            except pygame.error as e:
                print(f"이미지 로드 오류 {image_path}: {e}")

    if not frames:
        print(f"경고: {folder_path} 폴더에서 이미지를 로드하지 못했습니다.")

    return frames