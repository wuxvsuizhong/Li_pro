quantity = int(input().strip())
# for i in range(quantity):
trians = input().strip().split()
out,station = [],[]

res=set()

def search(station,trians,out):
    if not station and not trians and not out:
        # print("无进站火车和需要出站的火车,return,out is:",out)
        res.add(' '.join(out))
        return
    if len(out) >= quantity:
        # print("return,火车出站为,out is:",out)
        res.add(' '.join(out))
        return



    trians_copy = trians[:]
    station_copy = station[:]
    out_copy = out[:]
#     火车进站
    while trians:
        trian_pop = trians.pop(0)
        # print("火车进站到station:",trian_pop)
        station.append(trian_pop)
        search(station,trians,out)

#     火车出站
    while station_copy:
        # print("station_copy",station_copy)
        station_copy_pop = station_copy.pop()
        # print("火车出站到out",station_copy_pop)
        out_copy.append(station_copy_pop)
        search(station_copy,trians_copy,out_copy)

search(station,trians,out)

res = list(res)
res.sort()
for each in res:
    print(each)

