import pygame

TITLE_FONT_SIZE = 100
FONT_SIZE = 40

# TODO animation of falling stones
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

            outline_with_alpha = pygame.Surface(outline_surf.get_size(), pygame.SRCALPHA)
            outline_with_alpha.blit(outline_surf, (0, 0))
            outline_with_alpha.set_alpha(self.outline_alpha)

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
        color = (
            int(235),
            int(170 - 25 * t),
            int(94 + 40 * t)
        )
        pygame.draw.line(gradient, color, (0, y), (resolution[0], y))
    return gradient


def create_title(resolution, font):
    title_text = "Kameňožrút"
    center_x, center_y = resolution[0] // 2, resolution[1] // 4
    surface = font.render(title_text, True, (255, 255, 255))
    rect = surface.get_rect(center=(center_x, center_y))

    title = {
        'surface': surface,
        'rect': rect,
        'speed_x': 1,
        'speed_y': 1,
        'delay': 2.0
    }

    return title


def animate_title(title, resolution, elapsed_time):
    if elapsed_time >= title['delay']:
        rect = title['rect']
        rect.x += title['speed_x']
        rect.y += title['speed_y']

        if rect.left < 190 or rect.right > resolution[0] - 190:
            title['speed_x'] = -title['speed_x']
        if rect.top < 90 or rect.bottom > resolution[1] - 80:
            title['speed_y'] = -title['speed_y']
