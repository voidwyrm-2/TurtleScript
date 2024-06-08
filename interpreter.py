from turtle import Turtle
import turtle
from typing import Any
from random import randint
from time import sleep
from tcode import run_tcode
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

    def get_ln(self): return self.__ln
    
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


class TSFunction:
    def __init__(self, name: str, code: list[str], args: list[tuple[type, str, bool, Any]] | None = None):
        self.__name: str = name
        self.__code: list[str] = code
        self.__args: list[tuple[type, str, bool, Any]] | None = args
    
    def get_name(self): return self.__name

    def get_args(self): return self.__args
    
    def run(self, turtles: dict[str, Turtle], vars: dict[str, Any], funcs: dict[str, Any], ln: int, inputs: list[Any]) -> tuple[Error | None, int, dict[str, Any] | dict, dict[str, Turtle] | dict, dict[str, Any] | dict]:
        if len(inputs) > len(self.__args):
            return Error('ArgumentError', f"function {self.__name} expects {len(self.__args)} arguments, but was given {len(inputs)} arguments instead", ln), {}, {}, {}
        for ni, i in enumerate(inputs):
            pass

        return None, *run_code(self.__code, False, injected_vars=vars, injected_turtles=turtles, injected_funcs=funcs)



def get_turtle_info(turtle_name: str, turtle: Turtle):
    return '\n'.join([f"--turtle {turtle_name}--",
                         f"visible?: {turtle.isvisible()}",
                         f"color?: {turtle.color()}"])



def get_value(turtles: dict[str, Turtle], vars: dict[str, Any], value: str, ln: int) -> tuple[str | float | int | Nil | None, Error | None]:
    
    # basic data types
    if value.startswith('"') and value.endswith('"'):
        return value.removeprefix('"').removesuffix('"'), None
    elif value.removeprefix('-').replace('.', '', 1).isdigit():
        if '.' in value: return float(value), None
        return int(value), None
    
    # constant data types
    elif value == 'false': return False, None
    elif value == 'true': return True, None
    elif value == 'nil': return Nil(), None

    # turtle constants
    elif value in [t + '._SCREEN_WIDTH' for t in list(turtles)]:
        return turtles[value.removesuffix('._SCREEN_WIDTH')].screen.window_width(), None
    elif value in [t + '._SCREEN_HEIGHT' for t in list(turtles)]:
        return turtles[value.removesuffix('._SCREEN_HEIGHT')].screen.window_height(), None

    # variables and turtles
    elif value.removeprefix('-') in list(vars):
        if value.startswith('-'):
            value = value.removeprefix('-')
            if not isinstance(vars[value], (int, float)):
                return None, Error('InvalidOperationError', f"negatation is not a valid operation for type {type(vars[value]).__name__.casefold()}")
            return -vars[value], None
        return vars[value], None
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


def create_turtle(turtles: dict[str, Turtle], vars: dict[str, Any], turtlename: str, ln: int) -> Error | None:
    converted_turtlename, err = get_value(turtles, vars, turtlename, ln)
    if not err: turtlename = str(converted_turtlename)

    if turtlename in list(turtles):
        return Error('AlreadyExistingTurtleError', f"turtle '{turtlename}' has already been created", ln)
    elif turtlename == '': return Error('InvalidIdentifierError', "turtle identifier can't be empty", ln)

    turtles[turtlename] = Turtle()
    return None


def delete_turtle(turtles: dict[str, Turtle], vars: dict[str, Any], turtlename: str, ln: int) -> Error | None:
    converted_turtlename, err = get_value(turtles, vars, turtlename, ln)
    if not err: turtlename = str(converted_turtlename)

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


def process_function(turtles: dict[str, Turtle], vars: dict[str, Any], function: str, lines: list[str], ln: int) -> Error | None:
    funccodeblock_lines, funccodeblock_end_index, funccodeblock_err = collect_until_end(lines[ln:], ln, '!func')
    if funccodeblock_err: return funccodeblock_err



def process_turtle_command(turtles: dict[str, Turtle], vars: dict[str, Any], turtlename: str, command: str, inputs: str, ln: int) -> Error | None:
    if turtlename not in list(turtles):
        return Error('UnknownTurtleError', f"turtle '{turtlename}' does not exist", ln)

    res = getattr(turtles[turtlename], command, None)
    if res != None:
        inputs_converted = []
        if inputs:
            for i in inputs.replace(', ', ',').split(','):
                converted, err = get_value(turtles, vars, i, ln)
                if err: return err
                inputs_converted.append(converted)
        try:
            if len(inputs_converted): res(*inputs_converted)
            else: res()
            return None
        except Exception as e: return Error('CommandError', e, ln)
    
    return Error('UnknownCommandError', f"unknown command '{command}'", ln)


def collect_until_end(lines: list[str], start_ln: int, starttoken: str, endtoken: str = '!end') -> tuple[list[str], int, Error | None]:
    out = []
    endnest = 0
    for ln, l in enumerate(lines):
        if l == '' or l.startswith('#'): continue
        if l == endtoken and endnest == 0: break
        if l.startswith(('!loop', '!runtcode')): endnest += 1
        if l.startswith('!end'): endnest -= 1
        out.append(l)

    if ln == len(lines)-1 and lines[-1] != endtoken:
        return [], 0, Error('IncompleteStatementError', f"expected '{endtoken}' to end '{starttoken}' but found end of file", start_ln-1)
    
    return out, ln + start_ln, None

def process_line(turtles: dict[str, Turtle], vars: dict[str, Any], funcs: dict[str, TSFunction], line: str, lines: list[str], import_stack: list[str], ln: int) -> Error | None:
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

        elif l[0] == 'exit':
            try:
                l1_converted, err = get_value(l[1])
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
            args = ' '.join(l[2:]) if len(l) > 2 else ''
            err = process_turtle_command(turtles, vars, l[0], l[1], args, ln)
            if err: return err
            valid = True

        elif l[0] in ['++' + v for v in list(vars)] or l[0] in [v + '++' for v in list(vars)]:
            gotten_var, err = get_value(turtles, vars, l[0].removeprefix('++').removesuffix('++'), ln)
            if err: return err
            if not isinstance(gotten_var, (int, float)):
                return Error('InvalidOperationError', f"incrementation is not a valid operation for type {type(vars[l[0]]).__name__.casefold()}")
            vars[l[0].removeprefix('++').removesuffix('++')] = gotten_var + 1
            valid = True
        
        elif l[0] in ['--' + v for v in list(vars)] or l[0] in [v + '--' for v in list(vars)]:
            gotten_var, err = get_value(turtles, vars, l[0].removeprefix('--').removesuffix('--'), ln)
            if err: return err
            if not isinstance(gotten_var, (int, float)):
                return Error('InvalidOperationError', f"decrementation is not a valid operation for type {type(vars[l[0]]).__name__.casefold()}")
            vars[l[0].removeprefix('--').removesuffix('--')] = gotten_var - 1
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
            err = create_turtle(turtles, vars, ' '.join(l[2:]), ln)
            if err: return err
            valid = True
        
        elif l[0] == 'delete':
            if l[1] in list(turtles):
                err = delete_turtle(turtles, vars, ' '.join(l[2:]), ln)
            elif l[1] in list(vars):
                err = delete_variable(vars, l[1], ln)
            else: return Error('UnknownVariableError/UnknownTurtleError', f"unknown variable/turtle '{l[1]}'")
            if err: return err
            valid = True
            
        elif l[0] == '!loop':
            if len(l) < 2:
                return Error('MissingArgumentError', "expected argument for '!loop'", ln)
            converted_time, err = get_value(turtles, vars, l[1], ln)
            if err: return err
            if not isinstance(converted_time, int):
                return Error('InvalidArgumentError', "argmuent of '!loop' must be a whole number", ln)
            loop_index_varname = ''
            if len(l) >= 4:
                if l[2] == 'as': loop_index_varname = l[3]
                else:
                    return Error('InvalidArgumentError', f"expected 'as' or nothing, but found '{l[2]}' instead", ln)
            loop_lines, loop_end_index, loop_err = collect_until_end(lines[ln:], ln, '!loop')
            if loop_err:
                return loop_err
            for loop_index in range(converted_time):
                new_vars = vars.copy()
                if loop_index_varname != '' and isinstance(loop_index_varname, str):
                    new_vars[loop_index_varname] = loop_index
                loop_code_err, va, tur, fun = run_code(loop_lines, exitonclick=False, injected_vars=new_vars, injected_turtles=turtles.copy())
                if loop_code_err: return Error('DoNotPrintError')
                for v in va:
                    if v in list(vars): vars[v] = va[v]
                for tu in tur:
                    if tu in list(turtles): turtles[tu] = tur[tu]
                for fn in fun:
                    if fn in list(funcs): funcs[fn] = fun[fn]
            return Error('JumpToLineNumber', ln=loop_end_index+1)

        elif l[0] == '!runtcode':
            if len(l) < 2: return Error('MissingArgumentError', "expected arguments 'turtle' for action '!runtcode'", ln)
            if l[1] not in list(turtles):
                return Error('UnknownTurtleError', f"turtle '{l[1]}' does not exist", ln)
            tcodeblock_lines, tcodeblock_end_index, tcodeblock_err = collect_until_end(lines[ln:], ln, '!runtcode')
            if tcodeblock_err: return tcodeblock_err
            try:
                tcode_runtime_err = run_tcode('\n'.join(tcodeblock_lines), turtles[l[1]], False)
                if tcode_runtime_err: return Error('DoNotPrintError')
            except Exception as e:
                return Error('TcodeRuntimeError', e, ln)
            return Error('JumpToLineNumber', ln=tcodeblock_end_index+1)
        
        elif l[0] == '!func':
            return Error('UnimplementedFeatureError', "sorry, functions haven't been implemented yet!")
            #err = process_function(turtles, vars, ' '.join(l[1:]), lines, ln)
            #if err: return err
            #valid = True
    except IndexError: pass

    if not valid:
        #print(vars)
        #print([v + '++' for v in list(vars)])
        #print(l[0] in [v + '++' for v in list(vars)])
        return Error('UnknownMeaningError', f'meaning of "{" ".join(l)}" is unknown', ln)
    return None



def run_code(text: str | list[str], exitonclick: bool = True, import_stack: list[str] = [], is_imported: bool = False, injected_vars: dict[str, Any] = None, injected_turtles: dict[str, Turtle] = None, injected_funcs: dict[str, TSFunction] = None) -> tuple[int, dict[str, Any] | dict, dict[str, Turtle] | dict, dict[str, TSFunction] | dict]:
    vars: dict[str, Any] = injected_vars if isinstance(injected_vars, dict) else {}

    turtles: dict[str, Turtle] = injected_turtles if isinstance(injected_turtles, dict) else {}

    funcs: dict[str, TSFunction] = injected_funcs if isinstance(injected_funcs, dict) else {}

    lines = [l.split('#')[0].strip() for l in text.replace('; ', '\n').replace(';', '\n').split('\n')] if isinstance(text, str) else list(text)

    ln = 0
    while ln < len(lines):
        l = lines[ln]
        #print(ln, l)
        if l == '' or l.startswith('#'): ln += 1; continue

        err = process_line(turtles, vars, funcs, l, lines, import_stack, ln+1)
        
        if err:
            if err.get_type() == 'JumpToLineNumber': ln = err.get_ln(); continue
            elif err.get_type() == 'DoNotPrintError': return 1, {}, {}, {}
            else:
                print(err.error())
                if err.get_type() == 'ExitError':
                    return 2, {}, {}, {}
                return 1, {}, {}, {}
        ln += 1
    if exitonclick:
        print("click the turtle window to exit...")
        turtle.exitonclick()
    return 0, vars, turtles, funcs



"""if __name__ == '__main__':
    run_code('''var x = "Hello, Catdog!"
print x
var y = 42
print y / 2
new turtle Turt
print Turt
Turt speed 1
Turt forward 100
wait 1
print "EIXHENXBD"''')"""