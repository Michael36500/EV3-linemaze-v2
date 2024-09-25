#!/usr/bin/env pybricks-micropython

from typing import *
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase


class Position:
    def __init__(slef, x: int, y: int) -> None:
        slef.x = x
        slef.y = y


class Orientation:
    def num2str(slef, num: int) -> str:
        if num == 0:
            return "up"
        if num == 1:
            return "right"
        if num == 2:
            return "down"
        if num == 3:
            return "left"

    def str2num(slef, stri: str) -> int:
        if stri == "up":
            return 0
        if stri == "right":
            return 1
        if stri == "down":
            return 2
        if stri == "left":
            return 3

    def __init__(slef, starting: str) -> None:
        if starting not in ["up", "right", "down", "left"]:
            raise ValueError("Invalid orientation")

        slef.str_orient = starting
        slef.int_orient = slef.str2num(starting)

    def left(slef) -> None:
        slef.int_orient = (slef.int_orient - 1) % 4
        slef.str_orient = slef.num2str(slef.int_orient)

    def right(slef) -> None:
        slef.int_orient = (slef.int_orient + 1) % 4
        slef.str_orient = slef.num2str(slef.int_orient)


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

    def where_am_i(slef) -> str:
        print("where am i")
        bottom = [
            True if slef.left_color.reflection() < slef.target_color else False,
            True if slef.mid_color.reflection() < slef.target_color else False,
            True if slef.right_color.reflection() < slef.target_color else False,
        ]

        if bottom == [True, False, False]:
            print(bottom)
            raise Exception("something went wrong")
        if bottom == [False, False, True]:
            print(bottom)
            raise Exception("something went wrong")

        slef.step_a_inch()

        top = [
            True if slef.left_color.reflection() < slef.target_color else False,
            True if slef.mid_color.reflection() < slef.target_color else False,
            True if slef.right_color.reflection() < slef.target_color else False,
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
            return slef.dict_where[tuple(bottom)][tuple(top)][
                slef.orientation.num2str(slef.orientation.int_orient)
            ]
        except KeyError as e:
            print("bottom", bottom)
            print("top", top)
            print("orient", slef.orientation.str_orient)
            raise KeyError(e)

    def step_a_inch(slef) -> None:
        print("step a inch")
        curr = slef.drive_base.distance()
        while slef.drive_base.distance() - curr < slef.distance_wheels:
            slef.make_follow_step()

        slef.drive_base.stop()

    def forward(slef) -> None:
        print("forward")
        # curr = slef.drive_base.distance()
        # while slef.drive_base.distance() - curr < 150 - 23 - slef.distance_wheels:
        # slef.make_follow_step((slef.drive_base.distance() - curr)/(150-slef.wheel_center))
        # slef.make_follow_step()
        start_lenght = slef.drive_base.distance()

        while (
            slef.left_color.reflection() > slef.target_color
            and slef.right_color.reflection() > slef.target_color
            and slef.drive_base.distance() - start_lenght
            < 150 + 20 - slef.distance_wheels
        ):
            slef.make_follow_step()

        slef.drive_base.stop()
        slef.left_motor.hold()
        slef.right_motor.hold()

        if slef.drive_base.distance() - start_lenght >= 150 + 20 - slef.distance_wheels:
            slef.drive_base.straight(-20)

        lenght = 1
        if slef.orientation.str_orient == "up":
            slef.pos.y -= lenght
        elif slef.orientation.str_orient == "right":
            slef.pos.x += lenght
        elif slef.orientation.str_orient == "down":
            slef.pos.y += lenght
        elif slef.orientation.str_orient == "left":
            slef.pos.x -= lenght
        else:
            raise ValueError("Invalid orientation")

    def make_follow_step(slef) -> None:
        # part -= 0.5
        # part = abs(part)*2
        # part = 0.7-part
        # part += 0.3

        # print(part)

        error = slef.navigation_color.reflection() - slef.target_color
        error *= slef.kp
        # print(error)
        slef.drive_base.drive(slef.speed, error)

    def turn_left(slef) -> None:
        print("turn left")
        slef.drive_base.turn(-90)
        slef.orientation.left()

    def turn_right(slef) -> None:
        print("turn right")
        slef.drive_base.turn(90)
        slef.orientation.right()

    def turn_around(slef) -> None:
        print("turn around")
        slef.drive_base.turn(180)
        slef.orientation.left()
        slef.orientation.left()

    def turn_absolute(slef, orient: str) -> None:
        print("turn absolute", orient)
        start = slef.orientation.int_orient
        end = Orientation.str2num("slef", orient)
        # print(f'start: {start}, end: {end}')

        if start == end:
            return
        if (start - end) % 4 == 1:
            slef.turn_left()
        if (start - end) % 4 == 3:
            slef.turn_right()
        if (start - end) % 4 == 2:
            slef.turn_around()

    def __init__(slef) -> None:
        slef.ev3 = EV3Brick()
        slef.left_motor = Motor(Port.A)
        slef.right_motor = Motor(Port.D)
        slef.distance_wheels = 70

        slef.drive_base = DriveBase(slef.left_motor, slef.right_motor, 30.5, 169)
        slef.drive_base.settings(300, 150, 100, 100)

        slef.left_color = ColorSensor(Port.S3)
        slef.mid_color = ColorSensor(Port.S1)
        slef.right_color = ColorSensor(Port.S2)
        slef.navigation_color = ColorSensor(Port.S4)

        slef.target_color = 38
        slef.kp = -1.0
        slef.speed = 100

        # slef.secret_mapa = slef.load_mapa()
        # slef.found_end = False
        slef.pos = Position(0, 0)
        slef.orientation = Orientation("right")

        slef.dict_where = {
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
