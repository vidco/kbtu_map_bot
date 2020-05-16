OFFSET = 127462 - ord('A')


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


def unflag(_flag):
    return (chr(ord(_flag[0]) - OFFSET) + chr(ord(_flag[1]) - OFFSET)).lower()


def unflaggable(_flag):
    return len(_flag) == 2 and ord(_flag[0]) - OFFSET > 0 and ord(_flag[1]) - OFFSET > 0
