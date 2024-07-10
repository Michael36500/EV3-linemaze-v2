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
    # if there is not a need to follow a line
    # if mapa[pos_to.y][pos_to.x] in '├ ┤ ┬ ┴ ┼ ▫ ■':
    #     return pos_to

    # get direction
    if pos_from.x == pos_to.x:
        if pos_from.y > pos_to.y:   direction = 'up'
        else:                       direction = 'down'
    else:
        if pos_from.x > pos_to.x:   direction = 'left'
        else:                       direction = 'right'


    print(f'from: {pos_from} to: {pos_to}')
    print(f'from: {mapa[pos_from.y][pos_from.x]} to: {mapa[pos_to.y][pos_to.x]}')
    print(f'direction: {direction}')

    pos_final = pos_to
    iter = 0

    while mapa[pos_final.y][pos_final.x] not in '├ ┤ ┬ ┴ ┼ ▫ ■':
        iter += 1
        # print(mapa[pos_final.y][pos_final.x])
        # print(direction)
        # print()
        match mapa[pos_final.y][pos_final.x]:
            case '─':
                if direction == 'left':     pos_final.x -= 1
                elif direction == 'right':  pos_final.x += 1
                else: raise Exception('something fucked up')
        
            case '│':
                if direction == 'up':       pos_final.y -= 1
                elif direction == 'down':   pos_final.y += 1
                else: raise Exception('something fucked up"')
        

            case '┌':
                if direction == 'up':       pos_final.x += 1;   direction = 'right'
                elif direction == 'left':     pos_final.y += 1;   direction = 'down'
                else: raise Exception('something fucked up"')
        
            case '┐':
                if direction == 'up':       pos_final.x -= 1;   direction = 'left'
                elif direction == 'right':    pos_final.y += 1;   direction = 'down'
                else: raise Exception('something fucked up"')
            
            case '┘':
                if direction == 'down':     pos_final.x -= 1;   direction = 'left'
                elif direction == 'right':    pos_final.y -= 1;   direction = 'up'
                else: raise Exception('something fucked up"')
            
            case '└':
                if direction == 'down':     pos_final.x += 1;   direction = 'left'
                elif direction == 'right':    pos_final.y -= 1;   direction = 'up'
                else: raise Exception('something fucked up"')

            case '▫':
                pass
        

    # print(f'final: {pos_final}')
    return pos_final, iter


def main():
    mapa = load_mapa()
    pprint_mapa(mapa)

    queue = [Pos(1, 0)]

    while queue != []:
        pos = queue.pop(-1)
        print(pos)
        for neighboor in get_neighbours_near(mapa, pos):
            print(f'pos:\t\t{pos}')
            print(f'neighboor:\t{neighboor}')
            input()
            queue.append(
                follow_line(
                    mapa,
                    pos,
                    neighboor,
                ))
            




if __name__ == '__main__':
    main()