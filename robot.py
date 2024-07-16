#!/usr/bin/env pybricks-micropython

from typing import *
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase


class Position():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class Orientation():
    def num2str(self, num: int) -> str:
        if num == 0: return 'up'
        if num == 1: return 'right'
        if num == 2: return 'down'
        if num == 3: return 'left'

    def str2num(self, stri: str) -> int:
        if stri == 'up':    return 0
        if stri == 'right': return 1
        if stri == 'down':  return 2
        if stri == 'left':  return 3

    def __init__(self, starting: str) -> None:
        if starting not in ['up', 'right', 'down', 'left']:
            raise ValueError('Invalid orientation')

        self.str_orient = starting
        self.int_orient = self.str2num(starting)

    def left(self) -> None:
        self.int_orient = (self.int_orient - 1) % 4
        self.str_orient = self.num2str(self.int_orient)
    
    def right(self) -> None:
        self.int_orient = (self.int_orient + 1) % 4
        self.str_orient = self.num2str(self.int_orient)


class Robot():
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
        return self.secret_mapa[self.pos.y][self.pos.x]

    def forward(self) -> None:
        # todo
        pass


    def turn_left(self) -> None:
        # todo
        pass

    def turn_right(self) -> None:
        # todo
        pass

    def turn_around(self) -> None:
        # todo
        pass

    def turn_absolute(self, orient: str) -> None:
        start = self.orientation.int_orient
        end = Orientation.str2num('self', orient)
        # print(f'start: {start}, end: {end}')

        if start == end: return
        if (start - end) % 4 == 1: self.turn_left()
        if (start - end) % 4 == 3: self.turn_right()
        if (start - end) % 4 == 2: self.turn_around()
        
       


    def __init__(self) -> None:
        self.ev3 = EV3Brick()
        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.D)

        self.drive_base = DriveBase(self.left_motor, self.right_motor, 30, 156)
        self.drive_base.settings(200, 100, 100, 50)


        # self.secret_mapa = self.load_mapa()
        # self.found_end = False
        self.pos = Position(0, 0)
        self.orientation = Orientation('right')


        
robot = Robot()
print(robot.drive_base.settings())
robot.drive_base.straight(4*150)