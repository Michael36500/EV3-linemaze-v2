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
        print("where am i")
        bottom = [
            True if self.left_color.reflection() < self.target_color else False,
            True if self.mid_color.reflection() < self.target_color else False,
            True if self.right_color.reflection() < self.target_color else False,
        ]

        if bottom == [True, False, False]:
            print(bottom)
            raise Exception("something went wrong")
        if bottom == [False, False, True]:
            print(bottom)
            raise Exception("something went wrong")

        self.step_a_inch()

        top = [
            True if self.left_color.reflection() < self.target_color else False,
            True if self.mid_color.reflection() < self.target_color else False,
            True if self.right_color.reflection() < self.target_color else False,
        ]

        if top == [True, False, False]:
            print(top)
            raise Exception("something went wrong")
        if top == [False, False, True]:
            print(top)
            raise Exception("something went wrong")

        print(top)
        print(bottom)

        try:
            return self.dict_where[tuple(bottom)][tuple(top)][
                self.orientation.num2str(self.orientation.int_orient)
            ]
        except KeyError as e:
            print("bottom", bottom)
            print("top", top)
            print("orient", self.orientation.str_orient)
            raise KeyError(e)

    def step_a_inch(self) -> None:
        print("step a inch")
        curr = self.drive_base.distance()
        while self.drive_base.distance() - curr < self.distance_wheels:
            self.make_follow_step()

        self.drive_base.stop()

    def forward(self) -> None:
        print("forward")
        # curr = self.drive_base.distance()
        # while self.drive_base.distance() - curr < 150 - 23 - self.distance_wheels:
        # self.make_follow_step((self.drive_base.distance() - curr)/(150-self.wheel_center))
        # self.make_follow_step()
        start_lenght = self.drive_base.distance()

        while (
            self.left_color.reflection() > self.target_color
            and self.right_color.reflection() > self.target_color
            and self.drive_base.distance() - start_lenght
            < 150 + 20 - self.distance_wheels
        ):
            self.make_follow_step()

        self.drive_base.stop()
        self.left_motor.hold()
        self.right_motor.hold()

        if self.drive_base.distance() - start_lenght >= 150 + 20 - self.distance_wheels:
            self.drive_base.straight(-20)

        lenght = 1
        if self.orientation.str_orient == "up":
            self.pos.y -= lenght
        elif self.orientation.str_orient == "right":
            self.pos.x += lenght
        elif self.orientation.str_orient == "down":
            self.pos.y += lenght
        elif self.orientation.str_orient == "left":
            self.pos.x -= lenght
        else:
            raise ValueError("Invalid orientation")

    def make_follow_step(self) -> None:
        # part -= 0.5
        # part = abs(part)*2
        # part = 0.7-part
        # part += 0.3

        # print(part)

        error = self.navigation_color.reflection() - self.target_color
        error *= self.kp
        # print(error)
        self.drive_base.drive(self.speed, error)

    def turn_left(self) -> None:
        print("turn left")
        self.drive_base.turn(-90)
        self.orientation.left()

    def turn_right(self) -> None:
        print("turn right")
        self.drive_base.turn(90)
        self.orientation.right()

    def turn_around(self) -> None:
        print("turn around")
        self.drive_base.turn(180)
        self.orientation.left()
        self.orientation.left()

    def turn_absolute(self, orient: str) -> None:
        print("turn absolute", orient)
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
        self.distance_wheels = 70

        self.drive_base = DriveBase(self.left_motor, self.right_motor, 30.5, 169)
        self.drive_base.settings(300, 150, 100, 100)

        self.left_color = ColorSensor(Port.S3)
        self.mid_color = ColorSensor(Port.S1)
        self.right_color = ColorSensor(Port.S2)
        self.navigation_color = ColorSensor(Port.S4)

        self.target_color = 38
        self.kp = -1.0
        self.speed = 100

        # self.secret_mapa = self.load_mapa()
        # self.found_end = False
        self.pos = Position(0, 5)
        self.orientation = Orientation("up")

        self.dict_where = {
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


# robot = Robot()
# print(robot.drive_base.settings())
# robot.drive_base.straight(4*150)

if __name__ == "__main__":
    r = Robot()
    # r.where_am_i()
    # r.turn_right()
    # r.forward()
