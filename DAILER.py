import pygame
import math
import sys

# --- Configuration & Colors ---
WIDTH, HEIGHT = 800, 800
FPS = 60

# Colors (matching your React component)
COLOR_BG = (10, 10, 12)
COLOR_AUTO = (16, 185, 129)
COLOR_MANUAL = (239, 68, 68)
COLOR_TEXT = (255, 255, 255)
COLOR_GRAY = (156, 163, 175)

# Mode Definitions
MODES = [
    {"label": "Auto", "id": "Auto", "color": COLOR_AUTO, "desc": "Automatic Mode"},
    {"label": "P", "id": "P", "color": (255, 255, 255), "desc": "Program Mode"},
    {"label": "A", "id": "A", "color": (100, 149, 237), "desc": "Aperture Priority"},
    {"label": "S", "id": "S", "color": (147, 51, 234), "desc": "Shutter Priority"},
    {"label": "M", "id": "M", "color": COLOR_MANUAL, "desc": "Manual Mode"},
    {"label": "SCN", "id": "Scene", "color": (6, 182, 212), "desc": "Scene Mode"},
    {"label": "Portrait", "id": "Portrait", "color": (219, 39, 119), "desc": "Portrait Mode"},
    {"label": "Night", "id": "Night", "color": (79, 70, 229), "desc": "Night Mode"},
    {"label": "Video", "id": "Video", "color": (234, 88, 12), "desc": "Video Mode"},
    {"label": "Sport", "id": "Sport", "color": (202, 138, 4), "desc": "Sport Mode"},
    {"label": "Sunset", "id": "Sunset", "color": (244, 63, 94), "desc": "Sunset Mode"},
    {"label": "Macro", "id": "Macro", "color": (13, 148, 136), "desc": "Macro Mode"},
]

class CameraDial:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Camera Dial Pro")
        self.clock = pygame.time.Clock()
        self.font_lg = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_md = pygame.font.SysFont("Arial", 24)
        self.font_sm = pygame.font.SysFont("Arial", 18)

        self.selected_index = 4
        self.current_rotation = -4 * (360 / len(MODES))
        self.target_rotation = self.current_rotation
        self.radius = 220

    def draw_dial_marks(self, center, rotation):
        """Draws the tick marks on the outer ring."""
        num_marks = 120
        for i in range(num_marks):
            angle_deg = (i * 3) + rotation
            angle_rad = math.radians(angle_deg)
            
            is_large = i % 10 == 0
            length = 25 if is_large else 10
            width = 3 if is_large else 1
            alpha = 200 if is_large else 80

            start_x = center[0] + math.cos(angle_rad) * 260
            start_y = center[1] + math.sin(angle_rad) * 260
            end_x = center[0] + math.cos(angle_rad) * (260 - length)
            end_y = center[1] + math.sin(angle_rad) * (260 - length)

            pygame.draw.line(self.screen, (255, 255, 255), (start_x, start_y), (end_x, end_y), width)

    def draw_modes(self, center, rotation):
        """Draws the interactive mode buttons."""
        angle_step = 360 / len(MODES)
        for i, mode in enumerate(MODES):
            # Calculate position
            angle_deg = (i * angle_step) + rotation - 90
            angle_rad = math.radians(angle_deg)
            
            x = center[0] + math.cos(angle_rad) * 180
            y = center[1] + math.sin(angle_rad) * 180

            is_selected = i == self.selected_index
            scale = 1.4 if is_selected else 1.0
            
            # Draw Button Background
            rect_size = (60 * scale, 40 * scale)
            rect = pygame.Rect(0, 0, *rect_size)
            rect.center = (x, y)
            
            color = mode['color'] if is_selected else (40, 40, 40)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            if not is_selected:
                pygame.draw.rect(self.screen, mode['color'], rect, 2, border_radius=8)

            # Draw Label
            text_color = (0, 0, 0) if is_selected else mode['color']
            txt = self.font_sm.render(mode['label'], True, text_color)
            txt_rect = txt.get_rect(center=(x, y))
            self.screen.blit(txt, txt_rect)

    def run(self):
        while True:
            self.screen.fill(COLOR_BG)
            center = (WIDTH // 2, HEIGHT // 2)
            
            # --- Input Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEWHEEL:
                    self.selected_index = (self.selected_index - event.y) % len(MODES)
                    self.target_rotation = -self.selected_index * (360 / len(MODES))

            # --- Logic (Smooth Rotation) ---
            # Simple lerp for smooth movement
            diff = (self.target_rotation - self.current_rotation)
            self.current_rotation += diff * 0.1

            # --- Rendering ---
            current_mode = MODES[self.selected_index]

            # 1. Background Glow
            glow_surface = pygame.Surface((400, 400), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*current_mode['color'], 30), (200, 200), 180)
            self.screen.blit(glow_surface, (center[0]-200, center[1]-200))

            # 2. Outer Marks
            self.draw_dial_marks(center, self.current_rotation)

            # 3. Modes
            self.draw_modes(center, self.current_rotation)

            # 4. Center Display
            pygame.draw.circle(self.screen, (20, 20, 20), center, 80)
            pygame.draw.circle(self.screen, current_mode['color'], center, 80, 4)
            
            label_txt = self.font_lg.render(current_mode['label'], True, current_mode['color'])
            label_rect = label_txt.get_rect(center=(center[0], center[1] - 10))
            self.screen.blit(label_txt, label_rect)
            
            id_txt = self.font_sm.render(current_mode['id'], True, COLOR_GRAY)
            id_rect = id_txt.get_rect(center=(center[0], center[1] + 30))
            self.screen.blit(id_txt, id_rect)

            # 5. Top Indicator
            pygame.draw.polygon(self.screen, current_mode['color'], [
                (center[0] - 10, center[1] - 280),
                (center[0] + 10, center[1] - 280),
                (center[0], center[1] - 260)
            ])

            # 6. Title and Desc
            title_txt = self.font_md.render("CAMERA DIAL", True, (200, 200, 200))
            self.screen.blit(title_txt, (center[0] - title_txt.get_width()//2, 50))
            
            desc_txt = self.font_sm.render(current_mode['desc'], True, COLOR_GRAY)
            self.screen.blit(desc_txt, (center[0] - desc_txt.get_width()//2, 90))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    dial = CameraDial()
    dial.run()