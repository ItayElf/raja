import sys

from raja.actions import handle_command


def main():
    if len(sys.argv) < 2:
        print("Too few arguments.")
        exit(-1)
    cmd = sys.argv[1]
    params = sys.argv[2:]
    handle_command(cmd, params)


if __name__ == '__main__':
    main()
