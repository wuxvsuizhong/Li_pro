dial_codes=[
    (1,'a'),
    (2,'b'),
    (3,'c'),
    (4,'e'),
    (5,'f')
]
# 字典推导式分为两个部分：
# country:code 是推导后的key:vlue样式
# for code,country in dial_codes 则分别是前者code为key,后者country为value，分别对应可迭代对象的拆包后的位置元素
country_dial={country:code for code,country in dial_codes}
print(country_dial)

# 调整key:value顺序
code_dial={code:country for code,country in dial_codes}
print(dial_codes)

# 推导时把value字符串大写
# 对dial_codes重新排序
# 少选数据code<4的
code_dial ={code:country.upper()
            for code,country in sorted(dial_codes,key=lambda item:item[0],reverse=True) if code < 4}
print(code_dial)

# 字典的推导时可以向列表的调试一样灵活，在推导时进行各种中间处理和转换