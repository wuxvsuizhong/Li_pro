import re


def func():
    with open('test','r') as f:
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                break

it = func()
result_list = []
for each in it:
    ret = re.findall(r'login',str(each))
    if ret:
        result_list.append(ret)

print(result_list)



result_dict = {}
for each in result_set:
    result_dict[each] = result_list.count(each)

print(result_dict)