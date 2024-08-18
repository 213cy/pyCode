import sys

from notebook.notebookapp import main

breakpoint()
if __name__ == '__main__':
    sys.argv[0] = sys.argv[1]
    breakpoint()
    sys.exit(main())
