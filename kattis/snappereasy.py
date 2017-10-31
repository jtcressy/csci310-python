"""
Snapper Chain (easy)
Kattis Problem: https://open.kattis.com/problems/snappereasy
Accepted submission: https://open.kattis.com/submissions/2250640

ALSO Passes Snapper Chain (hard) (has larger numbers, such as 1 <= N <= 30 and 0 <= K <= 10^8)
Kattis Problem: https://open.kattis.com/problems/snapperhard
Accepted submission: https://open.kattis.com/submissions/2250981
"""


def process(N, K):
    N = int(N)
    K = int(K)
    if N % (2**K) == (2**K)-1:
        return "ON"
    else:
        return "OFF"


if __name__ == "__main__":
    for idx in range(0, int(input())):
        line = input()
        K, N = line.split()
        print("Case #{}: {}".format(idx+1, process(N,K)))
