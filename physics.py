from Box2D import b2World, b2PolygonShape, b2_dynamicBody, b2Vec2, b2FixtureDef
import math
import random


class PhysicsWorld:
    def __init__(self):
        self.world = b2World(gravity=(0, -4.905))
        self.time_step = 1.0 / 60.0
        self.vel_iters = 6
        self.pos_iters = 2

        self.elapsed_time = 0
        self.time_limit = 15  # (in seconds)
        self.ground_segments = []

        landing_zone_center = random.uniform(-14, 14)
        landing_zone_half_width = 3
        ground_y = -15

        self.landing_zone = {
            'left': landing_zone_center - landing_zone_half_width,
            'right': landing_zone_center + landing_zone_half_width,
            'y': ground_y + 1
        }

        self.create_mountainous_terrain(ground_y, landing_zone_center, landing_zone_half_width)

        self.lander = self.world.CreateDynamicBody(
            position=(0, 8),
            angle=0.0,
            angularDamping=4.0,
            linearDamping=0.1
        )


        fixture_def = b2FixtureDef(
            shape=b2PolygonShape(box=(1.0, 0.75)),
            density=1.0,
            friction=0.3,
            restitution=0.2
        )

        self.lander.CreateFixture(fixture_def)
        self.game_over = False
        self.has_landed = False
        self.landed_successfully = False

    def create_mountainous_terrain(self, base_y, landing_center, landing_half_width):
        segment_width = 2.0
        num_segments = 50
        start_x = -25
        max_height_variation = 3.0

        current_x = start_x
        prev_height = 0

        while current_x < 25:
            is_landing_zone = (landing_center - landing_half_width - 0.5 <= current_x <=
                            landing_center + landing_half_width + 0.5)

            if is_landing_zone:
                segment_width = 0.5
                height = base_y + 1
            else:
                base_variation = math.sin(current_x * 0.5) * 1.5
                random_variation = random.uniform(-1, 1) * max_height_variation
                height = base_y + 1 + base_variation + random_variation
                height = max(base_y + 1, min(height, base_y + 5))

            vertices = [
                (current_x, base_y),
                (current_x + segment_width, base_y),
                (current_x + segment_width, height),
                (current_x, prev_height if current_x > start_x else height)
            ]

            segment = self.world.CreateStaticBody(
                shapes=b2PolygonShape(vertices=vertices)
            )
            self.ground_segments.append(segment)

            prev_height = height
            current_x += segment_width

    def check_landing(self):
        lander_pos = self.lander.position
        lander_vel = self.lander.linearVelocity
        lander_angle = self.lander.angle
        while lander_angle > math.pi:
            lander_angle -= 2 * math.pi
        while lander_angle < -math.pi:
            lander_angle += 2 * math.pi

        if (abs(lander_pos.x) > 21 or
            lander_pos.y < -20 or
            lander_pos.y > 10):
            self.has_landed = True
            self.game_over = True
            self.landed_successfully = False
            return

        local_vertices = [
            b2Vec2(-1.0, -0.75),  # bottom left
            b2Vec2(1.0, -0.75),  # bottom right
            b2Vec2(1.0, 0.75),  # top right
            b2Vec2(-1.0, 0.75)  # top left
        ]

        world_vertices = [self.lander.GetWorldPoint(v) for v in local_vertices]

        has_collision = False
        for segment in self.ground_segments:
            segment_vertices = segment.fixtures[0].shape.vertices
            for v in world_vertices:
                ground_height = -float('inf')
                for i in range(len(segment_vertices)):
                    x1, y1 = segment_vertices[i]
                    x2, y2 = segment_vertices[i+1] if i < len(segment_vertices)-1 else segment_vertices[0]

                    if (min(x1, x2) <= v.x <= max(x1, x2)):
                        if abs(x2 - x1) < 0.001:
                            ground_height = max(y1, y2)
                        else:
                            t = (v.x - x1) / (x2 - x1)
                            ground_height = y1 + t * (y2 - y1)
                        break

                if v.y <= ground_height + 0.1:
                    has_collision = True
                    break
            if has_collision:
                break

        if has_collision:
            self.has_landed = True
            self.game_over = True

            landing_speed_ok = lander_vel.length < 6.0  # allowable speed
            angle_ok = abs(lander_angle) < 0.4  # about 18° tilt allowed
            position_ok = (self.landing_zone['left'] <= lander_pos.x <= self.landing_zone['right'])

            self.landed_successfully = landing_speed_ok and angle_ok and position_ok
            if not landing_speed_ok:
                print('too fast', lander_angle)
            if not angle_ok:
                print(f'angle, {lander_angle}')
            if not position_ok:
                print('out of bounds',lander_angle)
        else:
            self.has_landed = False
            self.landed_successfully = False

    def step(self):
        """Step the physics simulation forward"""
        self.world.Step(self.time_step, self.vel_iters, self.pos_iters)
        self.world.ClearForces()

        if not self.game_over:
            self.elapsed_time += self.time_step

            if self.elapsed_time >= self.time_limit:
                self.has_landed = True
                self.game_over = True
                self.landed_successfully = False
                return

            self.check_landing()

    def apply_thrust(self, thrust_magnitude: float):
        self.is_thrusting = thrust_magnitude > 0  # Always update the flag
        if self.is_thrusting and not self.game_over:
            angle = self.lander.angle
            force_dir = b2Vec2(math.sin(angle), math.cos(angle))
            force = thrust_magnitude * force_dir
            self.lander.ApplyForceToCenter(force, True)

    def apply_torque(self, torque: float):
        if not self.game_over:
            self.lander.ApplyTorque(torque, True)

    def get_lander_state(self):
        """Get current state of the lander"""
        return {
            'position': self.lander.position,
            'angle': self.lander.angle,
            'linear_velocity': self.lander.linearVelocity,
            'angular_velocity': self.lander.angularVelocity,
            'game_over': self.game_over,
            'has_landed': self.has_landed,
            'landed_successfully': self.landed_successfully,
            'is_thrusting': getattr(self, 'is_thrusting', False),
            'time_remaining': max(0, self.time_limit - self.elapsed_time)  # Add time remaining
        }

    def get_landing_zone(self):
        """Get landing zone boundaries"""
        return self.landing_zone