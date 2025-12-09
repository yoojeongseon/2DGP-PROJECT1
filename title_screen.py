# (파일: title_screen.py)

import pygame
import os


class TitleScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.Font(None, 80)
        self.sub_font = pygame.font.Font(None, 40)

        try:
            self.bg_image = pygame.image.load(os.path.join("Backgrounds", "lobby.png")).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height))
        except:
            self.bg_image = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "PLAY"
        return "TITLE"

    def update(self):
        pass

    def draw(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        self.draw_text_center(screen, "BOXING KING", self.title_font, (255, 255, 0), -50)
        self.draw_text_center(screen, "Press SPACE to Start", self.sub_font, (255, 255, 255), 50)

    def draw_text_center(self, surface, text, font, color, y_offset=0):
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + y_offset))
        surface.blit(text_surface, rect)