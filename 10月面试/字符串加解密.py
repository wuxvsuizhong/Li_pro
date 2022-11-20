'''
对输入的字符串进行加解密，并输出。

加密方法为：
当内容是英文字母时则用该英文字母的后一个字母替换，同时字母变换大小写,如字母a时则替换为B；字母Z时则替换为a；

当内容是数字时则把该数字加1，如0替换1，1替换2，9替换0；
其他字符不做变化。

解密方法为加密的逆过程。
数据范围：输入的两个字符串长度满足1≤n≤1000  ，保证输入的字符串都是只由大小写字母或者数字组成
输入描述：
第一行输入一串要加密的密码
第二行输入一串加过密的密码

输出描述：
第一行输出加密后的字符
第二行输出解密后的字符

示例1
输入：
abcdefg
BCDEFGH
输出：
BCDEFGH
abcdefg
'''
pass_map = {}
for i in range(ord('A'),ord('Z')+1):
    pass_map[chr(i)] = chr(i+32+1)
for i in range(ord('a'), ord('z') + 1):
    pass_map[chr(i)] = chr(i - 32+1)
for i in range(10):
    pass_map[str(i)] = str(i+1)
pass_map['9'] = '0'
pass_map['Z'] = 'a'
pass_map['z'] = 'A'
print(pass_map)

decry_map = dict(zip(pass_map.values(),pass_map.keys()))
# print(decry_map)

lines = []
for i in range(2):
    lines.append(input().strip())

res = []
tmp_str = ''
for c in lines[0]:
    tmp_str+=pass_map[c]
res.append(tmp_str)

tmp_str = ''
for c in lines[1]:
    tmp_str+=decry_map[c]
res.append(tmp_str)

for each in res:
        print(each)

