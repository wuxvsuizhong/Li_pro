'''
定义一个单词的“兄弟单词”为：交换该单词字母顺序（注：可以交换任意次），而不添加、删除、修改原有的字母就能生成的单词。
兄弟单词要求和原来的单词不同。例如： ab 和 ba 是兄弟单词。 ab 和 ab 则不是兄弟单词。
现在给定你 n 个单词，另外再给你一个单词 x ，让你寻找 x 的兄弟单词里，按字典序排列后的第 k 个单词是什么？
注意：字典中可能有重复单词。

数据范围：1≤n≤1000 ，输入的字符串长度满足1≤len(str)≤10，1≤k<n
输入描述：
输入只有一行。 先输入字典中单词的个数n，再输入n个单词作为字典单词。 然后输入一个单词x 最后后输入一个整数k
输出描述：
第一行输出查找到x的兄弟单词的个数m 第二行输出查找到的按照字典顺序排序后的第k个兄弟单词，没有符合第k个的话则不用输出。
示例1
输入：
3 abc bca cab abc 1

输出：
2
bca

示例2
输入：
6 cab ad abcd cba abc bca abc 1

输出：
3
bca

说明：
abc的兄弟单词有cab cba bca，所以输出3
经字典序排列后，变为bca cab cba，所以第1个字典序兄弟单词为bca
'''
line = input().strip().split()
quantity = int(line[0])
chars = line[1:quantity+1]
pattern = line[quantity+1]
find_index = int(line[-1])-1

# print(chars)

rec_map = {}
for c in pattern:
    if c in rec_map:
        rec_map[c] += 1
    else:
        rec_map[c] = 1

res = []
for each in chars:
    if(len(each)!=len(pattern)):
        # res.append(False)
        continue
    rec_map_cp = rec_map.copy()
    flag = False
    for c in each:
        if c in rec_map_cp:
            if rec_map_cp[c] >= 0:
                rec_map_cp[c] -= 1
            if rec_map_cp[c] < 0:
                # res.append(False)
                flag = True
                break
        else:
            # res.append(False)
            flag = True
            break
    if not flag and each != pattern:
        # res.append(True)
        res.append(each)

res.sort()
print(res)
print(len(res))
if len(res) >= find_index+1:
    print(res[find_index])





