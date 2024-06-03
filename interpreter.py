from turtle import Turtle
import turtle
from typing import Any
from random import randint
from time import sleep
turtle.hideturtle()



def strsub(string: str, start: int, end_at: int = None) -> str:
    if not end_at: end_at = len(string)
    else: end_at = start+end_at
    #if start > len(string) or end_at > len(string): return string
    return string[start:end_at]

def revstrsub(string: str, start: int, end_at: int = None, return_as_tuple: bool = False) -> str | tuple[str, str]:
    if not end_at: end_at = len(string)
    else: end_at = start+end_at
    if start > len(string) or end_at > len(string):
        if return_as_tuple: return string, ''
        return string
    if return_as_tuple: return string[0:start], string[end_at:len(string)]
    return string[0:start] + string[end_at:len(string)]



class Error:
    def __init__(self, type: str, details: str = None, ln: int = None, sect: str = None):
        self.__type = str(type)
        self.__details = str(details) if details else None
        self.__ln = ln
        self.__sect = sect
    
    def get_type(self): return self.__type
    
    def error(self):
        out = self.__type
        if self.__details: out += ': ' + self.__details
        if self.__sect:
            out += f"; sect '{self.__sect}'"
        if self.__ln:
            if self.__sect: out += f', on line {self.__ln}'
            else: out += f'; line {self.__ln}'
        return out


class Nil:
    def __repr__(self): return 'Nil'

    def __eq__(self, value: object) -> bool: return None == value

    def __ne__(self, value: object) -> bool: return None != value



def get_turtle_info(turtle_name: str, turtle: Turtle):
    return '\n'.join([f"--turtle {turtle_name}--",
                         f"visible?: {turtle.isvisible()}",
                         f"color?: {turtle.color()}"])



def get_value(turtles: dict[str, Turtle], vars: dict[str, Any], value: str, ln: int) -> tuple[str | float | int | Nil | None, Error | None]:
    if value.startswith('"') and value.endswith('"'):
        return value.removeprefix('"').removesuffix('"'), None
    
    elif value.removeprefix('-').replace('.', '', 1).isdigit():
        if '.' in value: return float(value), None
        return int(value), None
    
    elif value == 'false': return False, None

    elif value == 'true': return True, None
    
    elif value == 'nil': return Nil(), None

    elif value in list(vars): return vars[value], None

    elif value in list(turtles): return get_turtle_info(value, turtles[value]), None

    elif ' == ' in value:
        r, l = value.split(' == ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '==', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' != ' in value:
        r, l = value.split(' != ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '!=', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif 'not ' in value:
        l = value.split('not ', 1)
        expr_res, expr_err = process_expression(turtles, vars, '~', 'not', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' and ' in value:
        r, l = value.split(' and ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, 'and', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' or ' in value:
        r, l = value.split(' or ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, 'or', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' < ' in value:
        r, l = value.split(' < ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '<', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' > ' in value:
        r, l = value.split(' > ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '>', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' ^ ' in value:
        r, l = value.split(' ^ ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '^', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None

    elif ' & ' in value:
        r, l = value.split(' & ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '&', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' | ' in value:
        r, l = value.split(' | ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '|', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' ** ' in value:
        r, l = value.split(' ** ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '**', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' / ' in value:
        r, l = value.split(' / ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '/', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' % ' in value:
        r, l = value.split(' % ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '%', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' // ' in value:
        r, l = value.split(' // ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '//', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' * ' in value:
        r, l = value.split(' * ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '*', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' - ' in value:
        r, l = value.split(' - ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '-', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    elif ' + ' in value:
        r, l = value.split(' + ', 1)
        expr_res, expr_err = process_expression(turtles, vars, r, '+', l, ln)
        if expr_err: return None, expr_err
        return expr_res, None
    
    else: return None, Error('UnknownValueError', f"unknown value '{value}'", ln)



def process_expression(turtles: dict[str, Turtle], vars: dict[str, Any], right: str, op: str, left: str, ln: int) -> tuple[Any, Error | None]:
    right_converted, right_err = get_value(turtles, vars, right, ln)
    if right_err: return None, right_err

    left_converted, left_err = get_value(turtles, vars, left, ln)
    if left_err: return None, left_err

    try:
        match op:
            case '+': return right_converted + left_converted, None
            case '-': return right_converted - left_converted, None
            case '*': return right_converted * left_converted, None
            case '**': return right_converted ** left_converted, None
            case '/': return right_converted / left_converted, None
            case '//': return right_converted // left_converted, None
            case '%': return right_converted % left_converted, None

            # binary operations
            case '&': return right_converted & left_converted, None
            case '|': return right_converted | left_converted, None
            case '^': return right_converted ^ left_converted, None

            # boolean operations
            case 'and': return right_converted and left_converted, None
            case 'or': return right_converted or left_converted, None
            case 'not': return not left_converted, None
            case '==': return right_converted == left_converted, None
            case '!=': return right_converted != left_converted, None
            case '>': return right_converted > left_converted, None
            case '<': return right_converted < left_converted, None
    except ValueError as e: return None, Error('ExpressionError', e, ln)



def create_variable(turtles: dict[str, Turtle], vars: dict[str, Any], varname: str, value: str, ln: int) -> Error | None:
    if varname in list(vars):
        return Error('AlreadyCreatedVariableError', f"variable '{varname}' has already been created", ln)
    elif varname == '': return Error('InvalidIdentifierError', "variable identifier can't be empty", ln)
    
    converted, err = get_value(turtles, vars, value, ln)
    if err: return err

    vars[varname] = converted
    return None


def assign_variable(turtles: dict[str, Turtle], vars: dict[str, Any], varname: str, value: str, ln: int) -> Error | None:
    if varname not in list(vars):
        return Error('UnknownVariableError', f"variable '{varname}' does not exist", ln)
    
    converted, err = get_value(turtles, vars, value, ln)
    if err: return err

    vars[varname] = converted
    return None


def delete_variable(vars: dict[str, Any], varname: str, ln: int) -> Error | None:
    if varname not in list(vars):
        return Error('UnknownVariableError', f"variable '{varname}' does not exist", ln)
    else:
        del vars[varname]
    return None


def create_turtle(turtles: dict[str, Turtle], turtlename: str, ln: int) -> Error | None:
    if turtlename in list(turtles):
        return Error('AlreadyExistingTurtleError', f"turtle '{turtlename}' has already been created", ln)
    elif turtlename == '': return Error('InvalidIdentifierError', "turtle identifier can't be empty", ln)

    turtles[turtlename] = Turtle()
    return None


def delete_turtle(turtles: dict[str, Turtle], turtlename: str, ln: int) -> Error | None:
    if turtlename not in list(vars):
        return Error('UnknownTurtleError', f"turtle '{turtlename}' does not exist", ln)
    else:
        del turtles[turtlename]
    return None


def print_value(turtles: dict[str, Turtle], vars: dict[str, Any], value: str, ln: int) -> Error | None:
    value_converted, err = get_value(turtles, vars, value, ln)
    if err: return err
    print(value_converted)
    return None



def process_turtle_command(turtles: dict[str, Turtle], turtlename: str, command: str, inputs: list[str], ln: int) -> Error | None:
    if turtlename not in list(turtles):
        return Error('UnknownTurtleError', f"turtle '{turtlename}' does not exist", ln)
    res = getattr(turtles[turtlename], command, None)
    if res != None:
        inputs_converted = []
        for i in inputs:
            converted, err = get_value(turtles, vars, i, ln)
            if err: return err
            inputs_converted.append(converted)
        try:
            if len(inputs_converted): res(*inputs_converted)
            else: res()
            return None
        except Exception as e: return Error('CommandError', e, ln)
    
    return Error('UnknownCommandError', f"unknown command '{command}'", ln)



def process_line(turtles: dict[str, Turtle], vars: dict[str, Any], line: str, ln: int) -> Error | None:
    valid = False
    repcode = '{' + f'{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}' + '}'
    # get all starts and ends of all strings in the line
    spos = []
    pcache = None
    ignore_next = False
    for i, c in enumerate(line):
        if c == '"':
            if ignore_next: ignore_next = False; continue
            if pcache:
                spos.append((pcache, (i-pcache)+1))
                pcache = None
            else: pcache = i
        elif c == '\\': ignore_next = True
        elif ignore_next: ignore_next = False
    
    # isolate strings from line before strings
    strings = []
    for p in spos:
        start, end = p
        strings.append(strsub(line, start, end))
        t = revstrsub(line, start, end, True)
        line = t[0] + repcode + t[1]

    l = line.split(' ') # split line by spaces

    # re-add strings to split line
    idx = 0
    for i, il in enumerate(l):
        if il == repcode:
            l[i] = strings[idx]
            idx += 1
    
    # remove any trailing or leading whitespace that may be left over from something
    l = [i.strip() for i in l]

    try:
        if l[0] == 'print':
                err = print_value(turtles, vars, ' '.join(l[1:]), ln)
                if err: return err
                valid = True

        elif l[0] == 'var' and l[2] == '=':
            err = create_variable(turtles, vars, l[1], ' '.join(l[3:]), ln)
            if err: return err
            valid = True

        elif l[1] == '=':
            err = assign_variable(turtles, vars, l[0], ' '.join(l[2:]), ln)
            if err: return err
            valid = True

        elif (l[0], l[1]) == ('new', 'turtle'):
            err = create_turtle(turtles, l[2], ln)
            if err: return err
            valid = True
        elif l[0] == 'exit':
            try:
                l1_converted, err = l[1]
                if err: return err
                return Error('ExitError', l1_converted, ln)
            except IndexError:
                return None
        
        elif l[0] in ('wait', 'sleep'):
            if len(l) < 2: return Error('MissingArgumentError', "expected argument 'time' for action 'wait/sleep'", ln)
            converted_time, err = get_value(turtles, vars, l[1], ln)
            if err: return err
            if not isinstance(converted_time, (int, float)): return Error('InvalidArgumentError', "argument 'time' must be a number", ln)
            valid = True
            sleep(converted_time)

        elif l[0] in list(turtles):
            args = l[2:] if len(l) > 2 else []
            err = process_turtle_command(turtles, l[0], l[1], args, ln)
            if err: return err
            valid = True
    except IndexError: pass

    if not valid: return Error('UnkownMeaningError', f'meaning of "{" ".join(l)}" is unknown', ln)
    return None



def run_code(text: str, exitonclick: bool = True, import_stack: list[str] = [], is_imported: bool = False, injected_vars: dict[str, Any] = None, injected_turtles: dict[str, Turtle] = None) -> bool:
    vars: dict[str, Any] = injected_vars if injected_vars else {}

    turtles: dict[str, Turtle] = {}

    lines = [l.split('#')[0].strip() for l in text.replace('; ', '\n').replace(';', '\n').split('\n')]


    for ln, l in enumerate(lines):
        if l == '' or l.startswith('#'): continue

        err = process_line(turtles, vars, l, ln+1)
        
        if err:
            print(err.error())
            if err.get_type() == 'ExitError':
                return True
            return False
    print("click the turtle window to exit...")
    if exitonclick: turtle.exitonclick()
    return False



if __name__ == '__main__':
    run_code('''var x = "Hello, Catdog!"
print x
var y = 42
print y / 2
new turtle Turt
print Turt
Turt speed 1
Turt forward 100
sleep 1
print "EIXHENXBD"''')