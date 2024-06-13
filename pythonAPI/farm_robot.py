import glob
import os
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

import random
import time
import numpy as np
import cv2
try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_b
    from pygame.locals import K_c
    from pygame.locals import K_d
    from pygame.locals import K_f
    from pygame.locals import K_g
    from pygame.locals import K_h
    from pygame.locals import K_i
    from pygame.locals import K_l
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_o
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_t
    from pygame.locals import K_v
    from pygame.locals import K_w
    from pygame.locals import K_x
    from pygame.locals import K_z
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

IM_WIDTH = 640
IM_HEIGHT = 480


class KeyboardControl(object):
    """Class that handles keyboard input."""
    def __init__(self, vehicle):
        self._ackermann_enabled = False
        self._ackermann_reverse = 1
        if isinstance(vehicle, carla.Vehicle):
            self._control = carla.VehicleControl()
            self._ackermann_control = carla.VehicleAckermannControl()
        else:
            raise NotImplementedError("Actor type not supported")
        self._steer_cache = 0.0

    def parse_events(self, vehicle, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True
                if isinstance(self._control, carla.VehicleControl):
                    if event.key == K_f:
                        # Toggle ackermann controller
                        self._ackermann_enabled = not self._ackermann_enabled

        if isinstance(self._control, carla.VehicleControl):
            self._parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time())
            self._control.reverse = self._control.gear < 0
            # Apply control
            if not self._ackermann_enabled:
                vehicle.apply_control(self._control)
            else:
                world.player.apply_ackermann_control(self._ackermann_control)
                # Update control to the last one applied by the ackermann controller.
                self._control = vehicle.get_control()

    def _parse_vehicle_keys(self, keys, milliseconds):
        if keys[K_DOWN] or keys[K_s]:
            self._control.gear = -1
            self._control.brake = 0.0
            self._control.throttle = 1.0
        elif keys[K_UP] or keys[K_w]:
            self._control.gear = 1
            self._control.brake = 0.0
            self._control.throttle = 1.0
        else:
            self._control.throttle = 0.0
            self._control.brake = 1.0

        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT] or keys[K_a]:
            self._control.throttle = max(self._control.throttle, 0.2)
            self._control.brake = 0.0
            if self._steer_cache > 0:
                self._steer_cache = 0
            else:
                self._steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            self._control.throttle = max(self._control.throttle, 0.2)
            self._control.brake = 0.0
            if self._steer_cache < 0:
                self._steer_cache = 0
            else:
                self._steer_cache += steer_increment
        else:
            self._steer_cache = 0.0
        self._steer_cache = min(0.7, max(-0.7, self._steer_cache))
        if not self._ackermann_enabled:
            self._control.steer = round(self._steer_cache, 1)
        else:
            self._ackermann_control.steer = round(self._steer_cache, 1)

    @staticmethod
    def _is_quit_shortcut(key):
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)


def process_img(image, display, offset):
    i = np.array(image.raw_data)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    i3 = i2[:, :, :3]
    i4 = i3[:, :, ::-1]
    surface = pygame.surfarray.make_surface(i4.swapaxes(0, 1))
    display.blit(surface, offset)
    return i3/255.0


actor_list = []
try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('Agri_Robot')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)

    actor_list.append(vehicle)

    # https://carla.readthedocs.io/en/latest/cameras_and_sensors
    # get the blueprint for this sensor
    blueprint = blueprint_library.find('sensor.camera.rgb')
    # change the dimensions of the image
    blueprint.set_attribute('image_size_x', f'{IM_WIDTH}')
    blueprint.set_attribute('image_size_y', f'{IM_HEIGHT}')
    blueprint.set_attribute('fov', '110')

    #Pygame Window
    display = pygame.display.set_mode(
        (1280, 720),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    display.fill((0, 0, 0))
    pygame.display.flip()

    # Adjust sensor relative to vehicle
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

    sensor = world.spawn_actor(blueprint, spawn_point, attach_to=vehicle)

    actor_list.append(sensor)

    sensor.listen(lambda data: process_img(data, display, (0,0)))

    # Adjust sensor relative to vehicle
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7), carla.Rotation(0, 90, 0))

    sensor = world.spawn_actor(blueprint, spawn_point, attach_to=vehicle)

    actor_list.append(sensor)

    sensor.listen(lambda data: process_img(data, display, (IM_WIDTH, 150)))

    controller = KeyboardControl(vehicle)

    clock = pygame.time.Clock()
    while True:
        clock.tick_busy_loop(60)
        if controller.parse_events(vehicle, clock):
            break
        pygame.display.flip()

finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')