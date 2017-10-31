"""
Kattis Problem: https://open.kattis.com/problems/anewalphabet
Accepted Submission: https://open.kattis.com/submissions/2251455
"""
import sys


new_alpha = {
    'a' : "@",
    'b' : "8",
    'c' : "(",
    'd' : "|)",
    'e' : "3",
    'f' : "#",
    'g' : "6",
    'h' : "[-]",
    'i' : "|",
    'j' : "_|",
    'k' : "|<",
    'l' : "1",
    'm' : "[]\\/[]",
    'n' : "[]\\[]",
    'o' : "0",
    'p' : "|D",
    'q' : "(,)",
    'r' : "|Z",
    's' : "$",
    't' : "']['",
    'u' : "|_|",
    'v' : "\\/",
    'w' : "\\/\\/",
    'x' : "}{",
    'y' : "`/",
    'z' : "2"
}


def convert(ch):
    if ch.lower() in new_alpha:
        return new_alpha[ch.lower()]
    else:
        return ch


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    for line in lines:
        print(''.join(map(convert, line[:-1])))
