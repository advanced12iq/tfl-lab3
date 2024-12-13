import sys
from fuzz import read

def main():
    while True:
        lines = sys.stdin.readlines()
        read(lines)

if __name__ == "__main__":
    main()