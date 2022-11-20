'''
有6条配置命令，它们执行的结果分别是：

命   令	执   行
reset	reset what
reset board	board fault
board add	where to add
board delete	no board at all
reboot backplane	impossible
backplane abort	install first
he he	unknown command
注意：he he不是命令。

为了简化输入，方便用户，以“最短唯一匹配原则”匹配（注：需从首字母开始进行匹配）：

1、若只输入一字串，则只匹配一个关键字的命令行。例如输入：r，根据该规则，匹配命令reset，执行结果为：reset what；输入：res，根据该规则，匹配命令reset，执行结果为：reset what；
2、若只输入一字串，但匹配命令有两个关键字，则匹配失败。例如输入：reb，可以找到命令reboot backpalne，但是该命令有两个关键词，所有匹配失败，执行结果为：unknown command

3、若输入两字串，则先匹配第一关键字，如果有匹配，继续匹配第二关键字，如果仍不唯一，匹配失败。
例如输入：r b，找到匹配命令reset board 和 reboot backplane，执行结果为：unknown command。
例如输入：b a，无法确定是命令board add还是backplane abort，匹配失败。
4、若输入两字串，则先匹配第一关键字，如果有匹配，继续匹配第二关键字，如果唯一，匹配成功。例如输入：bo a，确定是命令board add，匹配成功。
5、若输入两字串，第一关键字匹配成功，则匹配第二关键字，若无匹配，失败。例如输入：b addr，无法匹配到相应的命令，所以执行结果为：unknow command。
6、若匹配失败，打印“unknown command”

注意：有多组输入。
数据范围：数据组数：1≤t≤800 ，字符串长度1≤s≤20 
进阶：时间复杂度：O(n)\O(n) ，空间复杂度：O(n)\O(n) 
输入描述：
多行字符串，每行字符串一条命令

输出描述：
执行结果，每条命令输出一行

示例1
输入：
reset
reset board
board add
board delet
reboot backplane
backplane abort

输出：
reset what
board fault
where to add
no board at all
impossible
install first
'''
import sys

cmds = []
while True:
    l = sys.stdin.readline().strip()
    if l:
        cmds.append(l)
    else:
        break

cmd_map={}
cmd_map["reset"]="reset what"
cmd_map["reset board"]="board fault"
cmd_map["board add"]="where to add"
cmd_map["board delete"] ="no board at all"
cmd_map["reboot backplane"] = "impossible"
cmd_map["backplane abort"] = "install first"

# for each in cmds:
class Trie():
    def __init__(self):
        self.root = {}
        self.end_word = '#'
        # self.possible_res=[]

    def insert(self,s):
        node = self.root
        for c in s:
            node = node.setdefault(c,{})
        node[self.end_word] = self.end_word

    def show(self):
        print(self.root)

    def search(self,s):
        node = self.root
        for c in s:
            if c not in node:
                return ''
            node = node[c]
        if self.end_word in node:
            return s

        c_str = s
        while len(node) == 1:
            k = list(node.keys())[0]
            if k == self.end_word:
                break
            c_str += k
            node = node[k]
        return c_str

    def search_all_possible(self,s):
        node = self.root
        for c in s:
            if c not in node:
                return
            node = node[c]

        if self.end_word in node:
            return [s]

        result = []
        def recur_search(d,ks):
            if not isinstance(d,dict) and d == self.end_word:
                result.append(ks.strip(self.end_word))
                return
            for kw in d:
                recur_search(d[kw],ks+kw)

        recur_search(node,s)
        return result

t=Trie()
for kw in cmd_map.keys():
    for each in kw.split(' '):
        t.insert(each)

for each in cmds:
    cmd_sp = each.split(' ')
    print("------")
    if len(cmd_sp) > 1:
        kw = []
        for c_str in cmd_sp:
            # ret = t.search(c_str)
            # print(c_str)
            ret = t.search_all_possible(c_str)
            if not ret:
                # print("unknown command")
                kw.clear()
                break
            else:
                if not kw: kw.extend(ret)
                else:
                    new_kw = []
                    for w in kw:
                        for r in ret:
                            new_kw.append(w+' '+r)
                    kw = new_kw
                # print(kw)
        find_key=[]
        for cmd_key in kw:
            # if cmd_key in cmd_map:print(cmd_map[cmd_key])
            if cmd_key in cmd_map:
                find_key.append(cmd_key)
        if len(find_key) != 1:
            print("unknown command")
        else:
            print(cmd_map[find_key[0]])
    elif len(cmd_sp) == 1:
        # ret = t.search(each)
        ret = t.search_all_possible(each)
        # print("ret->",ret)
        ret_len = len(ret)
        if ret_len == 1:
            if ret[0] in cmd_map:
                print(cmd_map[ret[0]])
            else:
                print("unknown command")
        elif ret_len == 0:
            print("unknown command")
        else:
            find_key = []
            for r in ret:
                if r in cmd_map:
                    find_key.append(r)
            if len(find_key) == 1:
                print(cmd_map[find_key[0]])
            else:
                print("unknown command")

