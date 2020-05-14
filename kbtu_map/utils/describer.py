from .phrases import MOVES, DIRECTIONS, FLOORS


def describe(path, language, level):
    if level <= 0 or level > 3:
        return ''

    result = '1. ' + MOVES.get('leave').get(language).format(departure=path[0],
                                                             direction=DIRECTIONS.get(path[1]).get(language)) + '\n'
    counter = 2

    i = 2
    while i < len(path) - 2:

        if path[i].isnumeric():
            if path[i + 1].isnumeric():
                if level > 2:
                    result += str(counter) + '. ' + 'Pass ' + path[i]
                else:
                    i += 1
                    continue
            else:
                if level > 1:
                    result += str(counter) + '. ' + 'Pass ' + path[i]
                else:
                    i += 1
                    continue
        else:
            result += str(counter) + '. '

            if path[i].startswith('up') or path[i].startswith('down'):
                result += _describe_floor(path[i], path[i + 1], language)
                i += 1
            else:
                result += MOVES.get(path[i]).get(language)

        result += '\n'
        counter += 1
        i += 1

    result += str(counter) + '. ' + MOVES.\
        get('arrive').get(language).format(arrive=path[-2],
                                           direction=DIRECTIONS.get(path[-1]).get(language)) + '\n'

    return result


def _describe_floor(change_floor, direction, language):
    options = change_floor.split('_')
    up_or_down, floor = options[0], options[1]
    return MOVES.get(up_or_down).get(language).format(floor=floor + FLOORS.get(floor).get(language),
                                                      direction=DIRECTIONS.get(direction).get(language))


OFFSET = 127462 - ord('A')


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


def unflag(qwe):
    return (chr(ord(qwe[0]) - OFFSET) + chr(ord(qwe[1]) - OFFSET)).lower()


def unflaggable(qwe):
    return len(qwe) == 2 and ord(qwe[0]) - OFFSET > 0 and ord(qwe[1]) - OFFSET > 0
