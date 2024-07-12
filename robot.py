from typing import *
# from dataclasses import dataclass
# from pydantic import BaseModel




class Position():
    # @enforce_types
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
    def load_mapa(_) -> List[List[str]]:
        mapa = []
        with open('maze2') as f:
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

    def forward(self) -> None:
        # check if all alrigh
        ## check if orient is valid
        if self.orientation.str_orient not in ['up', 'right', 'down', 'left']: 
            raise ValueError(f'Invalid orientation: {self.orientation.str_orient}')

        ## check if out of bounds
        if self.orientation.str_orient == 'up' and self.pos.y-1 < -1:      
            raise ValueError(f'Out of bounds: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}')
        if self.orientation.str_orient == 'right' and self.pos.x == len(self.secret_mapa[0]):   
            raise ValueError(f'Out of bounds: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}')
        if self.orientation.str_orient == 'down' and self.pos.y == len(self.secret_mapa):
            raise ValueError(f'Out of bounds: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}')
        if self.orientation.str_orient == 'left' and self.pos.x-1 < -1:
            raise ValueError(f'Out of bounds: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}')

        ## check if wall
        current: str = self.secret_mapa[self.pos.y][self.pos.x]
        match current:
            case '╴':
                # print(self.orientation.str_orient != 'left')
                if self.orientation.str_orient != 'left':
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '╵':
                if self.orientation.str_orient != 'up':
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '╶':
                if self.orientation.str_orient != 'right':
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '╷':
                if self.orientation.str_orient != 'down':
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '─':   
                if self.orientation.str_orient == 'up' or self.orientation.str_orient == 'down':      
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '│':
                if self.orientation.str_orient == 'right' or self.orientation.str_orient == 'left':   
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┌':
                if self.orientation.str_orient == 'left' or self.orientation.str_orient == 'up':      
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┐':
                if self.orientation.str_orient == 'right' or self.orientation.str_orient == 'up':     
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '└':
                if self.orientation.str_orient == 'left' or self.orientation.str_orient == 'down':    
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┘':
                if self.orientation.str_orient == 'right' or self.orientation.str_orient == 'down':   
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '├':
                if self.orientation.str_orient == 'left':                                            
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┤':
                if self.orientation.str_orient == 'right':                                             
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┬':  
                if self.orientation.str_orient == 'up':                                             
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┴':
                if self.orientation.str_orient == 'down':                                               
                    raise ValueError(f'Wall: {self.pos.x}, {self.pos.y}, {self.orientation.str_orient}. {current}')
            case '┼':
                pass
            case '■':
                if not self.found_end:
                    self.found_end = True
                    return 'end'
                else: 
                    # print('End already found')
                    pass
            case _:
                raise ValueError(f'Invalid character: {current} at {self.pos.x}, {self.pos.y}')                


        if self.orientation.str_orient == 'up':    self.pos.y -= 1
        if self.orientation.str_orient == 'right': self.pos.x += 1
        if self.orientation.str_orient == 'down':  self.pos.y += 1
        if self.orientation.str_orient == 'left':  self.pos.x -= 1


    def turn_left(self) -> None:
        self.orientation.left()

    def turn_right(self) -> None:
        self.orientation.right()
    
    def turn_around(self) -> None:
        self.turn_left()
        self.turn_left()
    
    def turn_absolute(self, orient: str) -> None:
        start = self.orientation.int_orient
        end = Orientation.str2num('self', orient)
        # print(f'start: {start}, end: {end}')

        if start == end: return
        if (start - end) % 4 == 1: self.turn_left()
        if (start - end) % 4 == 3: self.turn_right()
        if (start - end) % 4 == 2: self.turn_around()
        
       


    def __init__(self) -> None:
        self.secret_mapa = self.load_mapa()
        self.found_end = False
        self.pos = Position(0, 0)
        self.orientation = Orientation('right')


        
