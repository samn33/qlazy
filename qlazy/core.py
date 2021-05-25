import os
import subprocess
import sys

def main():
    args = sys.argv
    os.environ['LD_LIBRARY_PATH'] = os.path.dirname(__file__) + '/lib'
    os.environ['PATH'] = '~/.local/bin'
    raise SystemExit(subprocess.call([os.path.dirname(os.path.abspath(__file__)) + '/qlazy'] + args[1:]))
    
if __name__ == '__main__':
    main()
