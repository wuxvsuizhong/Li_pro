'''
描述
给出一组区间，请合并所有重叠的区间。
请保证合并后的区间按区间起点升序排列。

数据范围：区间组数 0 <= n <= 2 * 10^5,区间内 的值都满足 0 <= val <= 2 * 10^5

要求：空间复杂度 O(n)O(n)，时间复杂度 O(nlogn)O(nlogn)
进阶：空间复杂度 O(val)O(val)，时间复杂度O(val)O(val)

示例1
输入：
[[10,30],[20,60],[80,100],[150,180]]
返回值：
[[10,60],[80,100],[150,180]]

示例2
输入：
[[0,10],[10,20]]
返回值：
[[0,20]]
'''

def main():
    # grps = [[10,30],[20,60],[80,100],[150,180]]
    grps = [[2,3],[4,5],[6,7],[8,9],[1,10]]
    grps.sort()

    left,right = grps[0][0],grps[0][1]
    res = [[left,right]]
    for head,tail in grps[1:]:
        if head > right or tail < left:
            left = head
            right = tail
            res.append([left,right])
            continue
        else:
            tmpl = [left,right,head,tail]
            tmpl.sort()
            res.remove([left,right])
            left,right = tmpl[0],tmpl[-1]
            res.append([left,right])

    print(res)



if __name__ == '__main__':
    main()