'''
密码要求:
1.长度超过8位
2.包括大小写字母.数字.其它符号,以上四种至少三种
3.不能有长度大于2的包含公共元素的子串重复 （注：其他符号不含空格或换行

输入：
021Abc9000
021Abc9Abc1
021ABC9000
021$bc9000
输出：
OK
NG
NG
OK
'''
import sys

def main():
    line_list = []
    while True:
        line = sys.stdin.readline().strip()
        if line:
            line_list.append(line)
        else:
            break

    result=[]
    for i,s in enumerate(line_list):
        if len(s) <= 8:
            result.append("NG")
            continue
        rec = {}
        for c in s:
            if c.isdigit():
                rec["digit"] = True
            elif c.isalpha():
                if 'A' <= c <= 'Z':
                    rec["Upalpha"] = True
                else:
                    rec["Lowalpha"] = True
            else:
                if c not in ('\n', ' '):
                    rec["other"] = True

        mpart = [s[i:i+3] for i in range(len(s)-3)]
        for each in mpart:
            if mpart.count(each) > 1 and abs(s.index(each)-s.rindex(each)) > 1:
                result.append("NG")
                break
        if len(result)-1 >= i:
            continue

        count = 0
        for val in rec.values():
            if val:
                count += 1
        if count >= 3:
            result.append('OK')
        else:
            result.append("NG")

    print(result)

if __name__ == '__main__':
    main()
