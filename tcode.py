"""
An old project rebuilt as an easily accessible module(with some extra features)

tcode looks like this:
```
# tcode square example
0,100/100,100/100,0/0,0

# tcode moves the turtle without respect to its direction by default

# if you want the turtle to move by offset, do:
# ~o 0,100/100,0/0,-100/,-100,0

# if you want the turtle to move directionally, do:
# ~d f100/r90/f100/r90/f100/r90/f100
```
"""
import turtle



def run_instructions(instructions: list[tuple[int, int | float, int | float | None, tuple[int, int, int] | str]], turtle_instance: turtle.Turtle = turtle):
    if type(turtle_instance).__name__ == 'module' and not turtle_instance.isvisible():
        turtle_instance.showturtle()
    
    iprevious = 0, 0, (0, 0, 0)
    
    for i in instructions:
        mode, x, y, color = i
        if isinstance(color, str): turtle_instance.color(color)
        else: turtle_instance.color(*color)
        match mode:
            case 1:
                new_x, new_y = x + iprevious[0], y + iprevious[1]
                turtle_instance.goto(new_x, new_y)
                iprevious = new_x, new_y, color
            case 2:
                turtle_instance.forward(x)
                iprevious = x, y, color if y else x, 0, color
            case 3:
                turtle_instance.back(x)
                iprevious = x, y, color if y else x, 0, color
            case 4:
                turtle_instance.left(x)
                iprevious = x, y, color if y else x, 0, color
            case 5:
                turtle_instance.right(x)
                iprevious = x, y, color if y else x, 0, color
            case z:
                turtle_instance.goto(x, y)
                iprevious = x, y, color



def convert_snippet(snippet: str, mode: int, line_num: int, previous: tuple[int, int, int, tuple[int, int, int]]) -> tuple[tuple[int, int, int, tuple[int, int, int]], str | None]:
    xyc = snippet.split(',')
    if len(xyc) == 2:
        x, y = xyc
        try: x = int(x)
        except ValueError:
            return None, f"(line {line_num}) expected number for X, but got '{x}' instead"
        try: y = int(y)
        except ValueError:
            return None, f"(line {line_num}) expected number for Y, but got '{y}' instead"
        return (mode, x, y, previous[3]), None
    elif len(xyc) == 3:
        x, y, color_str = xyc
        try: x = int(x)
        except ValueError:
            return None, f"(line {line_num}) expected number for X, but got '{x}' instead"
        try: y = int(y)
        except ValueError:
            return None, f"(line {line_num}) expected number for Y, but got '{y}' instead"
        return (mode, x, y, color_str), None
    elif len(xyc) == 5:
        x, y, r, g, b = xyc
        try: x = int(x)
        except ValueError:
            return None, f"(line {line_num}) expected number for X, but got '{x}' instead"
        try: y = int(y)
        except ValueError:
            return None, f"(line {line_num}) expected number for Y, but got '{y}' instead"
        try:
            r = int(r)
            if r > 255 or r < 0: raise ValueError()
        except ValueError:
            return None, f"(line {line_num}) expected number in 0-255 for R, but got '{r}' instead"
        try:
            g = int(g)
            if g > 255 or g < 0: raise ValueError()
        except ValueError:
            return None, f"(line {line_num}) expected number in 0-255 for G, but got '{g}' instead"
        try:
            b = int(b)
            if b > 255 or b < 0: raise ValueError()
        except ValueError:
            return None, f"(line {line_num}) expected number in 0-255 for B, but got '{b}' instead"
        return (mode, x, y, (r, g, b)), None
    else: return None, f"(line {line_num}) invalid instruction '{snippet}'"


def process_tcode_snippet(snippet: str, mode: str, line_num: int, previous: tuple[int, int, int, tuple[int, int, int]]) -> tuple[tuple[int, int, int | None, tuple[int, int, int]], str | None]:
    if mode == 2:
        get_move_dir = lambda x: (3, x.removeprefix('r')) if x.startswith('r') else (1, x.removeprefix('b')) if x.startswith('b') else (2, x.removeprefix('l')) if x.startswith('l') else (0, x.removeprefix('f'))
        xyc = snippet.split(',')
        if len(xyc) == 1:
            dist = xyc[0]
            dir, dist = get_move_dir(dist)
            mode += dir
            try: dist = int(dist)
            except ValueError:
                return None, f"(line {line_num}) expected number for Distance, but got '{dist}' instead"
            return (mode, dist, None, previous[3]), None
        
        elif len(xyc) == 2:
            dist, color_str = xyc
            dir, dist = get_move_dir(dist)
            mode += dir
            try: dist = int(dist)
            except ValueError:
                return None, f"(line {line_num}) expected number for Distance, but got '{dist}' instead"
            return (mode, dist, None, color_str), None
        
        elif len(xyc) == 4:
            dist, r, g, b = xyc
            dir, dist = get_move_dir(dist)
            mode += dir
            try: dist = int(dist)
            except ValueError:
                return None, f"(line {line_num}) expected number for Distance, but got '{dist}' instead"
            try:
                r = int(r)
                if r > 255 or r < 0: raise ValueError()
            except ValueError:
                return None, f"(line {line_num}) expected number in 0-255 for R, but got '{r}' instead"
            try:
                g = int(g)
                if g > 255 or g < 0: raise ValueError()
            except ValueError:
                return None, f"(line {line_num}) expected number in 0-255 for G, but got '{g}' instead"
            try:
                b = int(b)
                if b > 255 or b < 0: raise ValueError()
            except ValueError:
                return None, f"(line {line_num}) expected number in 0-255 for B, but got '{b}' instead"
            return (mode, dist, None, (r, g, b)), None
        else: return None, f"(line {line_num}) invalid instruction '{snippet}'"

    else:
        res, err = convert_snippet(snippet, mode, line_num, previous)
        if err: return None, err
        return res, None

def run_tcode(text: str, turtle_instance: turtle.Turtle = turtle, exitonclick: bool = True) -> bool:
    'The bool returned is `True` if an error occured, else `False`'
    tcode = ([l.split('#')[0].strip() for l in text.split('\n') if not l.startswith('#') and l != ''])
    for ln, t in enumerate(tcode):
        instructions = []
        if t.startswith('~d '):
            t = t.removeprefix('~d ').strip()
            mode = 2
        elif t.startswith('~o '):
            t = t.removeprefix('~o ').strip()
            mode = 1
        else: mode = 0
        previous = mode, 0, 0, (0, 0, 0)
        for s in t.split('/'):
            res, err = process_tcode_snippet(s.strip(), mode, ln+1, previous)
            if err: print(err); return
            instructions.append(res)
            previous = res
        run_instructions(instructions, turtle_instance)
    if exitonclick:
        print("click the turtle window to exit...")
        turtle.exitonclick()
    return False
            

if __name__ == '__main__':
    turtle.hideturtle()
    t = turtle.Turtle()
    scuttleray = """0,100/-80,40/-25,0/0,0/0,100/80,40/25,0/0,0/-13,0/0,-100/13,0/0,0
0,75/-7,75/-7,70/0,70/0,75/7,75/7,70/0,70/0,0
0,65/-10,65/-10,60/0,60/0,65/10,65/10,60/0,60
0,55/-14,55/-14,50/0,50/0,55/14,55/14,50/0,50
0,45/-14,45/-14,40/0,40/0,45/14,45/14,40/0,40
0,35/-24,35/-24,30/0,30/0,35/24,35/24,30/0,30
0,25/-36,25/-36,20/0,20/0,25/36,25/36,20/0,20
0,-20/0,0"""
    boxes = """4,-4/-24,-4/-24,24/4,24/4,-4/64,54/64,94/104,94/104,54/64,54/34,-54/14,-54/-4,-74/-4,-94/14,-114/34,-114/54,-94/54,-74/34,-54/-114,-34/-184,-34/-184,-104/-114,-104/-114,-34"""
    square_normal = '0,100/100,100/100,0/0,0'
    square_offset = '~o 0,100/100,0/0,-100/-100,0'
    square_directional = '~d f100/r90/f100/r90/f100/r90/f100'
    run_tcode(square_directional, t)