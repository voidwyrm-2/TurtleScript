from interpreter import run_code
from tcode import run_tcode
from os import path



def turtlescript_playground():
    print('TurtleScript Interactive Playground')
    print("run 'exit' to exit the playground")
    while True:
        inp = input('>>> ')
        exited, v, t = run_code(inp, exitonclick=False)
        print(v)
        print(t)
        if exited == True: return



def show_help():
    print("        =commands=")
    print("'exit/quit': exits the program")
    print("'help': shows these messages")
    print("'run [file path]': runs a TurtleScript file")
    print("'tcode [tcode]': runs the given tcode")
    #print("'playground/play': runs the TurtleScript Interactive Playground")



def main(fpath_prefix: str = '', fpath_extension: str = '.turt', show_help_at_start: bool = True):
    print("==TurtleScript Python Intepreter==")
    if show_help_at_start: show_help()
    while True:
        inp = input('> ').strip()
        if inp.casefold() in ('exit', 'quit'):
            break
        
        elif inp.casefold() == 'help':
            show_help()

        elif inp.startswith('run '):
            fpath = fpath_prefix + '/' + inp.removeprefix('run ').removesuffix('.turt').strip() + fpath_extension
            if not path.exists(fpath):
                print(f"path '{fpath}' does not exist")
                continue
            if not path.isfile(fpath):
                print(f"path '{fpath}' is not a file")
                continue
            with open(fpath, 'rt') as tsf:
                fcontent = tsf.read()
            run_code(fcontent)

        elif inp.startswith('tcode '):
            run_tcode(inp.removeprefix('tcode '))
        #elif inp.casefold() in ('playground', 'play'):
        #    turtlescript_playground()



if __name__ == '__main__':
    main(fpath_prefix='scripts')
