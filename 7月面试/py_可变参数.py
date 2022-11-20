def func(*args,**kwargs):
    # print(args)
    for k,v in kwargs.items():
        print(v)


d1={"a":1,"b":2,"c":3}
func(1,2,3,**d1)

func()