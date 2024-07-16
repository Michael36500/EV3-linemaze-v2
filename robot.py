#!/usr/bin/env pybricks-micropython

from typing import *
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Orientation:
    def num2str(self, num: int) -> str:
        if num == 0:
            return "up"
        if num == 1:
            return "right"
        if num == 2:
            return "down"
        if num == 3:
            return "left"

    def str2num(self, stri: str) -> int:
        if stri == "up":
            return 0
        if stri == "right":
            return 1
        if stri == "down":
            return 2
        if stri == "left":
            return 3

    def __init__(self, starting: str) -> None:
        if starting not in ["up", "right", "down", "left"]:
            raise ValueError("Invalid orientation")

        self.str_orient = starting
        self.int_orient = self.str2num(starting)

    def left(self) -> None:
        self.int_orient = (self.int_orient - 1) % 4
        self.str_orient = self.num2str(self.int_orient)

    def right(self) -> None:
        self.int_orient = (self.int_orient + 1) % 4
        self.str_orient = self.num2str(self.int_orient)


class Robot:
    # def load_mapa(_) -> List[List[str]]:
    #     mapa = []
    #     with open('maze2') as f:
    #         for line in f:
    #             lin = []
    #             for char in line:
    #                 char = char.strip()
    #                 if char == '': char = ' '
    #                 lin.append(char)
    #             mapa.append(lin)
    #     return mapa

    def where_am_i(self) -> str:
        bottom = [
            True if self.left_color.reflection() < self.target_color else False,
            True if self.mid_color.reflection() < self.target_color else False,
            True if self.right_color.reflection() < self.target_color else False,
        ]

        if bottom == [True, False, False]:
            raise Exception("something went wrong")
        if bottom == [False, False, True]:
            raise Exception("something went wrong")

        top = [
            True if self.left_color.reflection() < self.target_color else False,
            True if self.mid_color.reflection() < self.target_color else False,
            True if self.right_color.reflection() < self.target_color else False,
        ]

        if top == [True, False, False]:
            raise Exception("something went wrong")
        if top == [False, False, True]:
            raise Exception("something went wrong")

        return self.where_dict[tuple(bottom)][tuple(top)][self.orientation.str_orient]

    def step_a_inch(self) -> None:
        self.drive_base.straight(self.wheel_center)

    def forward(self) -> None:
        curr = self.drive_base.distance()
        while self.drive_base.distance() - curr < 150 - self.wheel_center:
            # self.make_follow_step((self.drive_base.distance() - curr)/(150-self.wheel_center))
            self.make_follow_step()

        self.drive_base.stop()

    def make_follow_step(self) -> None:
        # part -= 0.5
        # part = abs(part)*2
        # part = 0.7-part
        # part += 0.3

        # print(part)

        error = self.navigation_color.reflection() - self.target_color
        error *= self.kp
        self.drive_base.drive(self.speed, error)

    def turn_left(self) -> None:
        self.drive_base.turn(-90)

    def turn_right(self) -> None:
        self.drive_base.turn(90)

    def turn_around(self) -> None:
        self.drive_base.turn(180)

    def turn_absolute(self, orient: str) -> None:
        start = self.orientation.int_orient
        end = Orientation.str2num("self", orient)
        # print(f'start: {start}, end: {end}')

        if start == end:
            return
        if (start - end) % 4 == 1:
            self.turn_left()
        if (start - end) % 4 == 3:
            self.turn_right()
        if (start - end) % 4 == 2:
            self.turn_around()

    def __init__(self) -> None:
        self.ev3 = EV3Brick()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.D)
        self.wheel_center = 60

        self.drive_base = DriveBase(self.left_motor, self.right_motor, 30.5, 169)
        self.drive_base.settings(300, 150, 100, 100)

        self.left_color = ColorSensor(Port.S3)
        self.mid_color = ColorSensor(Port.S1)
        self.right_color = ColorSensor(Port.S2)
        self.navigation_color = ColorSensor(Port.S4)

        self.target_color = 45
        self.kp = 5
        self.speed = 100

        # self.secret_mapa = self.load_mapa()
        # self.found_end = False
        self.pos = Position(0, 0)
        self.orientation = Orientation("right")

        self.where_dict = {
            # straight or dead end
            (False, True, False): {
                # straight
                (False, True, False): {
                    "up": "│",
                    "right": "─",
                    "down": "│",
                    "left": "─",
                },
                # dead end
                (False, False, False): {
                    "up": "╷",
                    "right": "╴",
                    "down": "╵",
                    "left": "╶",
                },
            },
            # left turn or ┤
            (True, True, False): {
                # left turn
                (False, False, False): {
                    "up": "┐",
                    "right": "┘",
                    "down": "└",
                    "left": "┌",
                },
                # ┤
                (False, True, False): {
                    "up": "┤",
                    "right": "┴",
                    "down": "├",
                    "left": "┬",
                },
            },
            # right turn or ├
            (False, True, True): {
                # right turn
                (False, False, False): {
                    "up": "┌",
                    "right": "┐",
                    "down": "┘",
                    "left": "└",
                },
                # ├
                (False, True, False): {
                    "up": "├",
                    "right": "┬",
                    "down": "┤",
                    "left": "┴",
                },
            },
            # t-shape, cross or end
            (True, True, True): {
                # t-shapes
                (False, False, False): {
                    "up": "┬",
                    "right": "┤",
                    "down": "┴",
                    "left": "├",
                },
                # cross
                (False, True, False): {
                    "up": "┼",
                    "right": "┼",
                    "down": "┼",
                    "left": "┼",
                },
                # end
                (True, True, True): {"up": "■", "right": "■", "down": "■", "left": "■"},
            },
        }


robot = Robot()
print(robot.drive_base.settings())
# robot.drive_base.straight(4*150)
