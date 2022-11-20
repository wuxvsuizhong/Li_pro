# 短除法进制转换
import sys


def main():
    num, role = sys.stdin.readline().strip().split()
    num = int(num)
    role = int(role)

    flag = num*role // abs(num*role)
    num,role = abs(num),abs(role)


    hexmap = {10: "A", 11: "B", 12:"C", 13: "D", 14: "E", 15: "F"}

    rec = []
    ret = num//role
    while ret:
        mod = num%role
        if mod > 9:
            rec.append(hexmap[mod])
        else:
            rec.append(mod)
        ret = num//role
        num = ret
    mod = num%role
    if mod:
        if mod > 9:
            rec.append(hexmap[mod])
        else:
            rec.append(mod)
    if flag > 0:
        print(''.join(map(str,rec[::-1])))
    else:
        print('-'+''.join(map(str,rec[::-1])))

if __name__ == '__main__':
        main()
