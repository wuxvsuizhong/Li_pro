import sys

def main():
    coins = map(int,sys.stdin.readline().strip().split())
    money = int(sys.stdin.readline().strip())

    dp = [0 for _ in range(money)]
    for i in range(1,money):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i-coin]+1,dp[i]) if



if __name__ == "__main__":
    main()