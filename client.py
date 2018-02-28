#!/usr/bin/env python3
import pygame
import json
from functools import partial
from argparse import ArgumentParser
from http.client import HTTPConnection
from types import SimpleNamespace

SPEED = 1000 * 80
START_POS = dict(x=130, y=0, z=-16)
FPS = 60
MAX_POS = dict(x=300, y=300, z=165)
MIN_POS = dict(x=0, y=-300, z=-20)
PS4_BUTTONS = {1: 'X', 2: 'O', 3: 'T', 4: 'L1', 5: 'R1', 6: 'L2', 7: 'R2'}
WRIST_DIRECTION = dict(L1=-10, R1=10)
PS4_AXIS = {0: 'y', 1: 'x', 5: 'z'}
MOVEMENT_FACTOR = 3.0
STATUS_LINE = """\
pos({pos[x]:.2f}, {pos[y]:.2f}, {pos[z]:.2f}) \
move({move[x]:.2f}, {move[y]:.2f}, {move[z]:.2f}) \
grip_closed[{grip_closed}], wrist_angle[{wrist_angle}]"""


def init_pygame():
    pygame.init()
    pygame.joystick.init()
    pygame.joystick.Joystick(0).init()


def swift_call(conn, action, **kwargs):
    conn.request('POST', '/', json.dumps(dict(action=action, kwargs=kwargs)))
    response = conn.getresponse().read().decode()
    return json.loads(response)['results']


def move_to_start(conn):
    swift_call(conn, 'set_position', **START_POS, speed=SPEED, wait=True)
    swift_call(conn, 'set_wrist', angle=90, wait=True)


def grip(conn, state, button):
    state.grip_closed = not state.grip_closed
    swift_call(conn, 'set_gripper', catch=state.grip_closed)


def turn_wrist(conn, state, button, direction):
    state.wrist_angle = max(min(state.wrist_angle + direction, 180), 0)
    swift_call(conn, 'set_wrist', angle=state.wrist_angle, wait=True)


def swing_wrist(conn, state, button):
    state.wrist_angle = 0 if state.wrist_angle == 180 else 180
    swift_call(conn, 'set_wrist', angle=state.wrist_angle, wait=True)


def move_arm(conn, state):
    if any(state.move.values()):
        for k, v in state.move.items():
            state.pos[k] += v
            state.pos[k] = min(state.pos[k], MAX_POS[k])
            state.pos[k] = max(state.pos[k], MIN_POS[k])
        swift_call(conn, 'set_position', **state.pos, speed=SPEED, wait=True)


def abort(conn, state, button):
    state.running = False


def handle_events(conn, state, handlers):
    for e in pygame.event.get():
        button = PS4_BUTTONS.get(getattr(e, 'button', None))
        handler = handlers.get(button)
        if e.type == pygame.JOYAXISMOTION and e.axis in PS4_AXIS:
            state.move[PS4_AXIS[e.axis]] = -round(e.value, 2) * MOVEMENT_FACTOR
        elif e.type == pygame.JOYBUTTONDOWN and handler:
            handler(conn, state, button)


def status_update(last_status, state):
    status = STATUS_LINE.format(**vars(state))
    if status != last_status:
        print(status)
    return status


def parse_args():
    parser = ArgumentParser(description='remote robot client')
    parser.add_argument('--host', default='localhost', help='server hostname')
    parser.add_argument('--port', default=8000, help='server port number')
    return parser.parse_args()


def get_handlers():
    wrist_right = partial(turn_wrist, direction=10)
    wrist_left = partial(turn_wrist, direction=-10)
    return dict(X=grip, O=abort, T=swing_wrist, L1=wrist_left, R1=wrist_right)


def main():
    args = parse_args()
    conn = HTTPConnection(args.host, args.port)
    move_to_start(conn)
    init_pygame()
    clock = pygame.time.Clock()
    last_status = ''
    state = SimpleNamespace(pos=START_POS.copy(), move=dict(x=0, y=0, z=0),
                            grip_closed=False, wrist_angle=90, running=True)
    handlers = get_handlers()
    while state.running:
        handle_events(conn, state, handlers)
        move_arm(conn, state)
        last_status = status_update(last_status, state)
        clock.tick(FPS)
    move_to_start(conn)


if __name__ == '__main__':
    main()
