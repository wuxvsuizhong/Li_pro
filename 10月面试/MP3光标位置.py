quantity = int(input().strip())
ops = input().strip()

song_list = []
for i in range(quantity):
    song_list.append(i+1)

start = 0
if quantity > 4:
    end = start+3
else:
    end = start+quantity-1
pos = start

for op in ops:
    if op == 'U':
        if start == 0 and pos == start:
            if quantity >=4:
                start = quantity-4
                end = start+3
                pos = end
            else:
                pos = len(song_list)-1
        elif pos == start:
            if quantity >= 4:
                start,end = start-1,end-1
                pos = start
            else:
                pos = end
        else:
            pos -= 1
    elif op == 'D':
        if end == len(song_list)-1 and pos == end:
            if quantity >=4:
                start = 0
                end = start+3
                pos = start
            else:
                pos = start
        elif pos == end:
            if quantity >=4:
                start,end = start+1,end+1
                pos = end
            else:
                pos = start
        else:
            pos += 1

    # print(op)
    # print(song_list[start:end], song_list[end])
    # print(song_list[pos])

res = list(map(str,song_list[start:end]))
res.append(str(song_list[end]))
print(' '.join(res))
print(song_list[pos])

