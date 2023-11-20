import functools
import json
import inspect

# 根据json文件的内容动态的创建类中的属性

JSON_PATH = './osconfeed.json'

class Record:
    """保存json中的各属性数据的类"""
    __index = None

    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)    # self.__dict__对应的是类的实例属性，在__dict__中的值，都可以通过类实例.属性名，来获得其属性对应的值
        # 这里使用dict的update方法，一次性的把传入的具名入参更新到Record类实例的__dict__属性字典中

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        """根据传入的key，从Record中获取其值"""
        if Record.__index is None:
            Record.__index = load()     # 调用load函数，解析json文件内容
        return Record.__index[key]

def load(path = JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection,raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]   # 提取json最外层的Schedule的键，并截掉最后一个字符
        cls_name = record_type.capitalize() #把键的字符串首字母大写，如event改写为Event,返回给cls_name作为类名
        cls = globals().get(cls_name,Record)    # 从全局作用域获取类名cls_name,如果获取不到，就返回Record
        if inspect.isclass(cls) and issubclass(cls,Record): # 判断cls如果是一个类，而且是Record的子类
            factory = cls
        else:
            factory = Record

        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)    # 创建json中 键值.Serial编号 为key的键值对，放入records字典中
    return records
    # records是一个dict,里面的键值对，其中的键是由json中的 key.序列号serial 重新组成的key
    # records中的值是，Record类的实例对象，而Record类里面包含了json中数据的各种属性(存在__dict__中)


class Event(Record):
    def __init__(self,**kwargs):
        self.__speaker_objs = None  # 这里因为Schedule.events这部分在osconfeed.json中比较特殊，其speakers键值对的值，是引用的Schedule.speakers的对应编号的部分
        super().__init__(**kwargs)

    def __repr__(self):
        try:
            # 这里先尝试从Event本身获取属性name(对应的是json中event键值下的各个子级中的name属性)
            return f'<{self.__class__.__name__} {self.name!r}'
        except AttributeError:
            # 如果Event本身没有name属性，那么就从Record中获取
            return super().__repr__()

    # @property
    @functools.cached_property      # 使用functools.cached_property 缓存特性，该他和property的差别在于，property默认阻止属性写入，除非定义了设值方法。而cached_property允许写入
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)   # self.__class__，从类实例中获取类对象，作用和type(self)一样

    @property
    def speakers(self):
        if self.__speaker_objs is None:
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            # return [fetch(f'speaker.{key}' for key in spkr_serials)]
            self.__speaker_objs = [fetch(f'speaker.{key}' for key in spkr_serials)]
        return self.__speaker_objs

    # 针对Schedule.events中，venue_serial和speakers这两个属性，是引用的Scheduile.venue和Schedule.venues
    # 这里这对这两个引用的属性，使用property装饰器并定义属性的同名方法来获取其最终的属性值
    # 获取这两个最终的属性值，其实也是调用的是Event的父类的Record的fetch方法，从Record的__index中通过key获取


if __name__ == "__main__":
    records = load(JSON_PATH)
    speaker = records['speaker.3471']
    print(speaker)  # <Record serial=3471>
    print(speaker.name,speaker.twitter) # Anna Martelli Ravenscroft annaraven

    event = Record.fetch('event.33950')
    print(event)    # <Event 'There *Will* Be Bugs'
    print(event.venue)  # <Record serial=1449>
    print(event.venue.name,event.venue_serial)  # Portland 251 1449