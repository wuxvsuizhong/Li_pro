def get_creators(record: dict) -> list:
    match record:
        case {'type':'book','api':2,'author':[*names]}:
            return names    # 返回匹配到的key为author的值
        case {'type':'book','api':1,'author':name}:
            return [name]   # 以列表形式返回匹配到的key为author的值
        case {'type':'book'}:
            raise ValueError(f"invalid 'boob' recode:{record!r}")
        case _:  # 如果都没有匹配的，返回ValueError
            raise ValueError(f'invalid record:{record!r}')


b1=dict(api=1,author='doug',type='book',title='Godel,Escher,Bach')
print(get_creators(b1))  # 返回匹配到的author


