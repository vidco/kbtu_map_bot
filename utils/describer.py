ACTIONS = {
    'leave': {
        'eng': 'From {departure} turn {direction}'
    },
    'arrive': {
        'eng': '{arrive} will be on the {direction}'
    },
    'up': {
        'eng': 'Go upstairs to {floor} floor and go {direction}'
    },
    'down': {
        'eng': 'Go downstairs to {floor} floor and go {direction}'
    },
    'left': {
        'eng': 'On the cross turn left'
    },
    'right': {
        'eng': 'On the cross turn right'
    },
    'straight': {
        'eng': 'On the cross go straight'
    }
}


def count_floor(floor):
    result = floor

    if floor == '0':
        result += ""
    elif floor == '1':
        result += "st"
    elif floor == '2':
        result += "nd"
    elif floor == '3':
        result += "rd"
    else:
        result += "th"

    return result


def describe(path, lang, level):

    if level <= 0 or level > 3:
        return ''

    result = '1. ' + ACTIONS.get('leave').get(lang).format(departure=path[0], direction=path[1]) + '\n'
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
                result += _describe_floor(path[i], path[i+1], lang)
                i += 1
            else:
                result += ACTIONS.get(path[i]).get(lang)

        result += '\n'
        counter += 1
        i += 1

    result += str(counter) + '. ' + ACTIONS.get('arrive').get(lang).format(arrive=path[-2], direction=path[-1]) + '\n'

    return result


def _describe_floor(change_floor, direction, lang):
    options = change_floor.split('_')
    up_or_down, floor = options[0], options[1]
    return ACTIONS.get(up_or_down).get(lang).format(floor=count_floor(floor), direction=direction)
