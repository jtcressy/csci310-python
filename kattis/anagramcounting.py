"""
Kattis Problem: https://open.kattis.com/problems/anagramcounting
Accepted Submission: https://open.kattis.com/submissions/2250790
"""
import sys
import math


def process(l):
    counts = {}
    for c in l[0:-1]:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    ans = math.factorial(len(l)-1)
    for c in counts:
        ans /= math.factorial(counts[c])
    return int(ans)


if __name__ == "__main__":
    for line in sys.stdin.readlines():
        print(process(line))
