'''
Catcher是MCA国的情报员，他工作时发现敌国会用一些对称的密码进行通信，比如像这些ABBA，ABA，A，123321，但是他们有时会在开始或结束时加入一些无关的字符以防止别国破解。比如进行下列变化 ABBA->12ABBA,ABA->ABAKK,123321->51233214　。因为截获的串太长了，而且存在多种可能的情况（abaaab可看作是aba,或baaab的加密形式），Cathcer的工作量实在是太大了，他只能向电脑高手求助，你能帮Catcher找出最长的有效密码串吗？

数据范围：字符串长度满足1≤n≤2500
输入描述：
输入一个字符串（字符串的长度不超过2500）

输出描述：
返回有效密码串的最大长度

示例1
输入：
ABBA
输出：
4

示例2
输入：
ABBBA
输出：
5

示例3
输入：
12HHHHA

输出：
4
'''


l = input().strip()
maxlen = 0
for i in range(len(l)):
    left,right = i-1,i+1
    while left >=0 and right <len(l):
        if l[left] == l[right]:
            maxlen = max(maxlen,right-left+1)
            left -= 1
            right += 1
        else:
            break

for i in range(0,len(l)):
    left,right = i,i+1
    while left >=0 and right < len(l):
        if l[left] == l[right]:
            maxlen = max(maxlen,right-left+1)
            left -= 1
            right += 1
        else:
            break

print(maxlen)

