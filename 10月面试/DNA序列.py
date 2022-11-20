s = input().strip()
lenght = int(input().strip())

i,j=0,1

cnt_map = {
    "C":0,
    "G":0,
}

i=0
start = i
res = []
while i < len(s) and start < len(s):
    if s[i] in cnt_map:
        cnt_map[s[i]] += 1
    i+=1
    if i-start >= lenght:
        # print(s[start:i])
        if cnt_map['G'] !=0 or cnt_map['C'] != 0:
            res.append(s[start:i])
        start +=1
        # while start < len(s) and  s[start] not in cnt_map:start += 1
        cnt_map['G'] = 0
        cnt_map['C'] = 0

print(res)
res_count=[]
for v in res:
    res_count.append((v.count('C') + v.count('G')) / len(v))
print(res_count)

if res and len(res) > 1:
    print(res[res_count.index(max(res_count))])
else:
    print(res[0])


