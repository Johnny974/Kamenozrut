import pygame

FONT_SIZE = 40


class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font("../assets/fonts/Audiowide-Regular.ttf", 40)
        self.is_hovered = False
        self.outline_alpha = 0
        self.fade_speed = 20

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and self.outline_alpha < 255:
            self.outline_alpha += self.fade_speed
            if self.outline_alpha > 255:
                self.outline_alpha = 255
        elif not self.is_hovered and self.outline_alpha > 0:
            self.outline_alpha -= self.fade_speed
            if self.outline_alpha < 0:
                self.outline_alpha = 0

        text_color = (255, 255, 255) if not self.is_hovered else (200, 200, 200)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)

        if self.outline_alpha > 0:
            outline_surf = self.font.render(self.text, True, (0, 0, 0))
            outline_rect = outline_surf.get_rect(center=self.rect.center)
            # Vytvorenie povrchu pre okraj s alfa hodnotou
            outline_with_alpha = pygame.Surface(outline_surf.get_size(), pygame.SRCALPHA)
            outline_with_alpha.blit(outline_surf, (0, 0))
            outline_with_alpha.set_alpha(self.outline_alpha)
            # Posunuté povrchy pre efekt okraja (viac smerov)
            screen.blit(outline_with_alpha, outline_rect.move(-2, -2))
            screen.blit(outline_with_alpha, outline_rect.move(2, -2))
            screen.blit(outline_with_alpha, outline_rect.move(-2, 2))
            screen.blit(outline_with_alpha, outline_rect.move(2, 2))

        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def create_gradient(resolution):
    gradient = pygame.Surface(resolution)
    for y in range(resolution[1]):
        t = y / resolution[1]
        # RGB color
        color = (
            int(235),
            int(170 - 25 * t),
            int(94 + 40 * t)
        )
        pygame.draw.line(gradient, color, (0, y), (resolution[0], y))
    return gradient


def title_letter_separation(resolution, font):
    title_text = "Kameňožrút"
    letters = []
    center_x, center_y = resolution[0] // 2, resolution[1] // 4

    full_text_surface = font.render(title_text, True, (255, 255, 255))
    full_text_rect = full_text_surface.get_rect(center=(center_x, center_y))
    current_x = full_text_rect.left
    for i, char in enumerate(title_text):
        char_surface = font.render(char, True, (255, 255, 255))
        char_width = font.size(char)[0]
        char_rect = char_surface.get_rect(topleft=(current_x, center_y))
        letters.append({
            'surface': char_surface,
            'rect': char_rect,
            'speed_x': -1,
            'speed_y': 1,
            'delay': 4.0 + i
        })
        current_x += char_width

    return letters


def title_animation(resolution, letters, elapsed_time):
    for letter in letters:
        if elapsed_time >= letter['delay']:
            letter['rect'].x += letter['speed_x']
            letter['rect'].y += letter['speed_y']
            # Odrážanie od okrajov
            if letter['rect'].left < 190 or letter['rect'].right > resolution[0] - 190:
                letter['speed_x'] = -letter['speed_x']
            if letter['rect'].top < 80 or letter['rect'].bottom > resolution[1] - 80:
                letter['speed_y'] = -letter['speed_y']
