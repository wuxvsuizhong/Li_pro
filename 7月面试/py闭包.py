def test(number):
    print('-----1------')
    def test_in():
        print('------------2-------')
        print(number+200)
    print('-------------3---------')

    return test_in

t=test(10)
print('+'*20)
t()

#闭包可以设置一个基准值，然后后续传入不同的入参，可以使用这个基准
print('*'*20)

def func(num1):
    print(num1)
    def func_in(num2):
        val=num1+num2
        print(val)
    return func_in

f=func(10)
f(20)
f(30)