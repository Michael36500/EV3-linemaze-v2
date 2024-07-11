from typing import *
from dataclasses import dataclass
from pydantic import BaseModel




class Position():
    # @enforce_types
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def forward(self, orient: str) -> None:
        # check if all alrigh
                


        if orient == 'up':    self.y -= 1
        if orient == 'right': self.x += 1
        if orient == 'down':  self.y += 1
        if orient == 'left':  self.x -= 1


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
    def load_mapa(_) -> List[List[str]]:
        mapa = []
        with open('maze') as f:
            for line in f:
                lin = []
                for char in line:
                    char = char.strip()
                    if char == '': char = ' '
                    lin.append(char)
                mapa.append(lin)
        return mapa


    def where_am_i(self) -> str:
        return self.secret_mapa[self.pos.y][self.pos.x]


    def __init__(self) -> None:
        self.secret_mapa = self.load_mapa()
        self.pos = Position(0, 0)
        self.orientation = Orientation('right')

        
