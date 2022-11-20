'''
原理：ip地址的每段可以看成是一个0-255的整数，把每段拆分成一个二进制形式组合起来，然后把这个二进制数转变成一个长整数。
举例：一个ip地址为10.0.3.193
每段数字             相对应的二进制数
10                   00001010
0                    00000000
3                    00000011
193                  11000001
组合起来即为：00001010 00000000 00000011 11000001,转换为10进制数就是：167773121，即该IP地址转换后的数字就是它了。
数据范围：保证输入的是合法的 IP 序列

示例1
输入：
10.0.3.193
167969729
输出：
167773121
10.3.3.193
'''
import sys

def main():
    lines = []
    while True:
        line = sys.stdin.readline().strip()
        if line:
            lines.append(line)
        else:
            break

    for l in lines:
        tmpl = []
        for n in l.split('.'):
            tmpl.append(bin(int(n)).replace('0b',''))
        if len(tmpl) ==1:
            # 数字转IP
            bstr=tmpl[0].rjust(32,'0')
            ipseg=[]
            for i in range(0,len(bstr),8):
                ipseg.append(str(int(bstr[i:i+8],2)))

            print('.'.join(ipseg))
        else:
            #IP转数字
            s=''
            for bn in tmpl:
                s += bn.rjust(8,'0')
            # print(s)
            sum = 0
            for i,v in enumerate(s):
                sum += int(v)*(2**(len(s)-i-1))
            print(sum)


if __name__ == '__main__':
    main()