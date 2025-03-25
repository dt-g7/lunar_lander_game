import pygame
import math
from Box2D import b2Vec2

class Renderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Lunar Lander")
        self.scale = 20.0  # pixels per meter
        self.screen_center = b2Vec2(width/2, height * 0.75)
        
    def clear(self):
        """Clear the screen"""
        self.screen.fill((0, 0, 0))
        
    def to_screen(self, point):
        """Convert Box2D coordinates to screen coordinates"""
        return (
            int(point.x * self.scale + self.screen_center.x),
            int(self.height - (point.y * self.scale + self.screen_center.y))
        )

    def draw_flag(self, x, y, facing_right=True):
        """Draw a flag at the specified position"""
        base_pos = self.to_screen(b2Vec2(x, y))
        pole_top = self.to_screen(b2Vec2(x, y + 2))  # 2 meters tall pole
        pygame.draw.line(self.screen, (255, 255, 255), base_pos, pole_top, 2)
        flag_points = []
        if facing_right:
            flag_points = [
                pole_top,
                (pole_top[0] + 20, pole_top[1] - 10),
                (pole_top[0], pole_top[1] - 20)
            ]
        else:
            flag_points = [
                pole_top,
                (pole_top[0] - 20, pole_top[1] - 10),
                (pole_top[0], pole_top[1] - 20)
            ]
        
        pygame.draw.polygon(self.screen, (255, 0, 0), flag_points)  # Red flag
        
    def draw_landing_zone(self, landing_zone):
        """Draw the landing zone with flags and connecting line"""
        self.draw_flag(landing_zone['left'], landing_zone['y'], False)  # Left flag faces right
        self.draw_flag(landing_zone['right'], landing_zone['y'], True)  # Right flag faces left
        left_point = self.to_screen(b2Vec2(landing_zone['left'], landing_zone['y']))
        right_point = self.to_screen(b2Vec2(landing_zone['right'], landing_zone['y']))
        pygame.draw.line(self.screen, (255, 255, 0), left_point, right_point, 2)  # Yellow line
        
    def draw_lander(self, position, angle):
        """Draw the lunar lander"""
        screen_pos = self.to_screen(position)
        
        # draw lunar lander body
        points = [
            (-10, -15),  # bottom left
            (10, -15),   # bottom right
            (20, 15),    # top right
            (-20, 15),   # top left
        ]
        
        # rotate and translate points
        rotated_points = []
        for x, y in points:
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            rx += screen_pos[0]
            ry += screen_pos[1]
            rotated_points.append((int(rx), int(ry)))
            
        pygame.draw.polygon(self.screen, (255, 255, 255), rotated_points, 2)
        
    def draw_ground(self, ground_segments):
        """Draw the ground segments"""
        for segment in ground_segments:
            vertices = [(self.to_screen(b2Vec2(v))) for v in segment.fixtures[0].shape.vertices]
            # draw ground
            pygame.draw.polygon(self.screen, (150, 150, 150), vertices)
            pygame.draw.polygon(self.screen, (100, 100, 100), vertices, 2)

    def draw_game_state(self, state):
        """Draw game state (win/lose message)"""
        font = pygame.font.Font(None, 36)
        
        time_remaining = state.get('time_remaining', 0)
        timer_color = (255, 255, 255)
        if time_remaining < 5:
            timer_color = (255, 0, 0)
        timer_text = f"Time: {time_remaining:.1f}"
        timer_surface = font.render(timer_text, True, timer_color)
        self.screen.blit(timer_surface, (10, 10))
        
        if state['game_over']:
            if state['landed_successfully']:
                text = "LANDED!"
                color = (0, 255, 0)
            else:
                text = "CRASHED!"
                color = (255, 0, 0)
            
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.screen.get_width()/2, 50))
            self.screen.blit(text_surface, text_rect)

    def draw_thrust_effect(self, position, angle):
        """Draw a small red triangle under the lander when thrust is active."""
        thrust_local = [
            (-10, 20),  # left base
            (10, 20),  # right base
            (0, 25)  # tip
        ]

        # transform local flame coordinates to world coordinates
        screen_pos = self.to_screen(position)
        rotated_points = []
        for x, y in thrust_local:
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            rx += screen_pos[0]
            ry += screen_pos[1]
            rotated_points.append((int(rx), int(ry)))

        pygame.draw.polygon(self.screen, (255, 0, 0), rotated_points)

    def update(self):
        """Update the display"""
        pygame.display.flip()