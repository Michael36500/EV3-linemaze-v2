from dataclasses import dataclass
from typing import *


@dataclass
class Pos:
    x: int
    y: int

def pprint_mapa(mapa: List[List[int]]) -> None:
    for lin in mapa:
        for char in lin:
            print(char, end='')
            if char in '─┌├└┬┴┼':
                print('-', end='')
            else:
                print(' ', end='')
        print()


def load_mapa() -> List[List[int]]:
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


def get_neighbours_near(mapa: List[List[int]], pos: Pos) -> List[Pos]:
    # ─ │ ┌ ┐ ┘ ├ └ ┤ ┬ ┴ ┼ ▫ ■
    current_char = mapa[pos.y][pos.x]
    neighbours_close = []
    if current_char in '─│':
        raise Exception('you are in a straight line')

    if current_char in '┌┐┘└':
        raise Exception('you are in a turn')

    if current_char in ' ':
        raise Exception('you are in an empty space')

    if current_char == '├':
        neighbours_close.append(Pos(pos.x, pos.y - 1))
        neighbours_close.append(Pos(pos.x, pos.y + 1))
        neighbours_close.append(Pos(pos.x + 1, pos.y))
    
    if current_char == '┤':
        neighbours_close.append(Pos(pos.x, pos.y - 1))
        neighbours_close.append(Pos(pos.x, pos.y + 1))
        neighbours_close.append(Pos(pos.x - 1, pos.y))

    if current_char == '┬':
        neighbours_close.append(Pos(pos.x - 1, pos.y))
        neighbours_close.append(Pos(pos.x + 1, pos.y))
        neighbours_close.append(Pos(pos.x, pos.y + 1))

    if current_char == '┴':
        neighbours_close.append(Pos(pos.x - 1, pos.y))
        neighbours_close.append(Pos(pos.x + 1, pos.y))
        neighbours_close.append(Pos(pos.x, pos.y - 1))  

    if current_char == '┼':
        neighbours_close.append(Pos(pos.x - 1, pos.y))
        neighbours_close.append(Pos(pos.x + 1, pos.y))
        neighbours_close.append(Pos(pos.x, pos.y - 1))
        neighbours_close.append(Pos(pos.x, pos.y + 1))
    
    if current_char in '■':
        raise Exception('you are at the end of the maze')


    return neighbours_close


def follow_line(mapa: List[List[int]], pos_from: Pos, pos_to: Pos) -> Pos:
    # ─ │ ┌ ┐ ┘ ├ └ ┤ ┬ ┴ ┼ ▫ ■
    print(f'from: {pos_from} to: {pos_to}')
    print(f'from: {mapa[pos_from.y][pos_from.x]} to: {mapa[pos_to.y][pos_to.x]}')

    # if there is not a need to follow a line
    if mapa[pos_to.y][pos_to.x] in '├ ┤ ┬ ┴ ┼ ▫ ■':
        return pos_to

    # get direction
    if pos_from.x == pos_to.x:
        if pos_from.y > pos_to.y:   direction = 'up'
        else:                       direction = 'down'
    else:
        if pos_from.x > pos_to.x:   direction = 'left'
        else:                       direction = 'right'

    print(f'direction: {direction}')

    pos_final = pos_to

    while pos_final not in '├ ┤ ┬ ┴ ┼ ▫ ■':
        if mapa[pos_to.y][pos_to.x] == '─':
            if direction == 'left':     pos_final.x -= 1
            elif direction == 'right':  pos_final.x += 1
            else: raise Exception('something fucked up')
        
        if mapa[pos_to.y][pos_to.x] == '│':
            if direction == 'up':       pos_final.y -= 1
            elif direction == 'down':   pos_final.y += 1
            else: raise Exception('something fucked up"')




def main():
    mapa = load_mapa()
    pprint_mapa(mapa)
    # pos = Pos(1, 0)
    # print(get_neighbours_near(mapa, pos))
    follow_line(mapa, Pos(1, 0), Pos(1, 1))



if __name__ == '__main__':
    main()