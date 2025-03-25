import pygame
from physics import PhysicsWorld
from rendering import Renderer
from input_handler import InputHandler

def main():
    pygame.init()
    
    physics = PhysicsWorld()
    renderer = Renderer()
    input_handler = InputHandler()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        events = pygame.event.get()
        thrust_magnitude, torque = input_handler.process_input(events)

        if thrust_magnitude is None:  # Quit signal
            running = False
            continue

        physics.apply_thrust(thrust_magnitude)

        if torque != 0:
            physics.apply_torque(torque)


        if thrust_magnitude > 0:
            physics.apply_thrust(thrust_magnitude)
        if torque != 0:
            physics.apply_torque(torque)
            
        physics.step()
        
        state = physics.get_lander_state()

        renderer.clear()
        renderer.draw_ground(physics.ground_segments)
        renderer.draw_landing_zone(physics.get_landing_zone())
        renderer.draw_lander(state['position'], state['angle'])
        if state.get('is_thrusting'):
            renderer.draw_thrust_effect(state['position'], state['angle'])

        renderer.draw_game_state(state)
        renderer.update()

        clock.tick(60)
        
    pygame.quit()

if __name__ == "__main__":
    main() 