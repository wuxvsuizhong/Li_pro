import sys,re,unicodedata
from collections.abc import Iterator

RE_EORD = re.compile(r'\w+')
STOP_CODE = sys.maxunicode + 1

def tokenize(text:str) ->Iterator[str]:
    """返回全大写的单词构成的可迭代对象"""
    for match in RE_EORD.finditer(text):    # 震泽匹配所有的字符串
        yield match.group().upper()

def name_index(start:int=32,end:int = STOP_CODE) ->dict[str,set[str]]:
    index:dict[str,set[str]] = {}
    for char in (chr(i) for i in range(start,end)):
        if name:=unicodedata.name(char,''):         # unicodedata.name 返回字符在unicdode中的描述信息，如+返回'PLUS SIGN' ,a返回'LATIN SMALL LETTER A', 数字返回描述'DIGIT TWO'
            for word in tokenize(name):
                index.setdefault(word,set()).add(char)
    return index

index = name_index(32,65)
print(index)
print(index['SIGN'])    # {'+', '<', '%', '$', '>', '=', '#'}
print(index['DIGIT'])   # {'8', '9', '0', '1', '3', '5', '6', '2', '7', '4'}
print(index['DIGIT'] & index['EIGHT'])  # {'8'}

# name_index，返回传入的数据范围的unicode字符的描述信息，并把字符对应的描述信息的单词split分割后作为键存储到字典中，键建对应的值就是字符本身的集合
# index就是返回的字符映射字典，然可以根据关键字得到对应的字符数据集(其实关键字就是对应的字符的描述词语)