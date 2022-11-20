'''
请实现一个函数用来匹配包括'.'和'*'的正则表达式。
1.模式中的字符'.'表示任意一个字符
2.模式中的字符'*'表示它前面的字符可以出现任意次（包含0次）。
在本题中，匹配是指字符串的所有字符匹配整个模式。例如，字符串"aaa"与模式"a.a"和"ab*ac*a"匹配，但是与"aa.a"和"ab*a"均不匹配

数据范围:
1.str 只包含从 a-z 的小写字母。
2.pattern 只包含从 a-z 的小写字母以及字符 . 和 *，无连续的 '*'。
3. 0 <=str.length <=26
4. 0 <=pattern.length <=26  c

输入：
"aaa","a*a"
返回值：
true
说明：
中间的*可以出现任意次的a，所以可以出现1次a，能匹配上

示例2
输入：
"aad","c*a*d"
返回值：
true
说明：
因为这里 c 为 0 个，a被重复一次， * 表示零个或多个a。因此可以匹配字符串 "aad"。

示例3
输入：
"a",".*"
返回值：
true
说明：
".*" 表示可匹配零个或多个（'*'）任意字符（'.'）

示例4
输入：
"aaab","a*a*a*c"
返回值：
false

'''
import sys


def main():
    vars = sys.stdin.readline().strip().split()
    s = vars[0]
    pattern = vars[1]

    dp = [[None for _ in range(len(s) + 1)] for _ in range(len(pattern) + 1)]
    for i in range(len(dp[0])):
        dp[0][i] = True if i == 0 else False
    for j in range(len(pattern) + 1):
        if j == 0:
            dp[j][0] = True
        elif pattern[j - 1] == '.':
            dp[j][0] = True
        elif pattern[j - 1] == '*':
            dp[j][0] = dp[j - 2][0]
        else:
            dp[j][0] = False

    for iv in range(len(pattern)):
        ivi = iv + 1
        for jv in range(len(s)):
            jvj = jv + 1
            if pattern[iv] == '.':
                dp[ivi][jvj] = dp[ivi-1][jvj-1]
            elif pattern[iv] == '*':
                if pattern[iv - 1] == s[jv]:
                    ret = dp[ivi - 1][jvj] or dp[ivi][jvj - 1] or dp[ivi - 2][jvj - 1]
                    dp[ivi][jvj] = ret
                elif pattern[iv - 1] == '.':
                    print(ivi,jvj)
                    ret = dp[ivi - 2][jvj - 1] or dp[ivi - 1][jvj] or dp[ivi-1][jvj-1] or dp[ivi][jvj-1]
                    print(ret)
                    dp[ivi][jvj] = ret
                else:
                    dp[ivi][jvj] = dp[ivi - 2][jvj]
            else:
                if pattern[iv] == s[jv]:
                    dp[ivi][jvj] = dp[ivi - 1][jvj - 1]
                else:
                    dp[ivi][jvj] = False

    print(dp)


if __name__ == '__main__':
    main()
