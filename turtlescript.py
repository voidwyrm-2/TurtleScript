from interpreter import run_code
from tcode import run_tcode
from run import main
import argparse
import os



parser = argparse.ArgumentParser()

parser.add_argument('-r', '--run', nargs='?', required=False, dest='run', type=str)

parser.add_argument('-t', '--tcode', nargs='?', required=False, dest='tcode', type=str)


args = parser.parse_args()


run = args.run

tcode = args.tcode


if not (run and tcode):
    main()
    raise SystemExit()

