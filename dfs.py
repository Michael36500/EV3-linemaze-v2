from dataclasses import dataclass


@dataclass
class Pos:
    x: int
    y: int

def pprint_mapa(mapa):
    for lin in mapa:
        for char in lin:
            print(char, end='')
            if char in '─┌├└┬┴┼':
                print('-', end='')
            else:
                print(' ', end='')
        print()


def load_mapa():
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


def get_neighbours(mapa, pos):
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


    # next node, not turn
    neig_far = []


def main():
    mapa = load_mapa()
    pprint_mapa(mapa)
    pos = Pos(1, 0)
    print(get_neighbours(mapa, pos))



if __name__ == '__main__':
    main()