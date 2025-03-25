import pygame
from Box2D import b2Vec2
import math

class InputHandler:
    def __init__(self):
        self.thrust_power = 50.0
        self.rotation_power = 20.0
        
    def process_input(self, events):
        """Process input events and return forces to apply"""
        thrust_magnitude = 0
        torque = 0
        
        # quit event
        for event in events:
            if event.type == pygame.QUIT:
                return None, None

        keys = pygame.key.get_pressed()
        
        # w key for  thrust
        if keys[pygame.K_w]:
            thrust_magnitude = self.thrust_power
        # a and d keys for rotation
        if keys[pygame.K_d]:
            torque = self.rotation_power
        if keys[pygame.K_a]:
            torque = -self.rotation_power

        return thrust_magnitude, torque 