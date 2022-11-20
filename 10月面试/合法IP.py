import sys

ipstr = input().strip()
ipsegs = ipstr.split('.')
if len(ipsegs) != 4:
    print("NO")
    sys.exit(0)

valid=True
for i,each in enumerate(ipsegs):
    if not each or not each.isdigit() or (len(each)>1 and each.startswith('0')):
        # print('NO')
        valid = False
        break
    each = int(each)
    if each <0 or each >254:
        # print('NO')
        valid = False
        break

if valid:
    print("YES")
else:
    print("NO")



