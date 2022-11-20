import sys
def main():
    nums = []
    while True:
        n = sys.stdin.readline().strip()
        if n == '':
            break
        else:
            nums.append(int(n))

    vars =nums[1:]
    result = []
    for i,v in enumerate(vars):
        if vars.index(v) == i:
            result.append(v)

    result.sort()
    return result

if __name__ == '__main__':
    main()