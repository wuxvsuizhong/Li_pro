import sys


def calc_fraction_sub(f1,f2):
    z1,m1 = map(int,f1.split('/'))
    z2,m2 = map(int,f2.split('/'))
    if m1 == m2:
        if z1>z2:
            return "{}/{}".format(z1-z2,m1)
        else:
            return "{}/{}".format(z2-z1,m1)
    else:
        nz1,nm1 = z1*m2,m1*m2
        nz2,nm2 = z2*m1,m2*m1
        if nz1>nz2:
            # return "{}/{}".format(z1-z2,m1)
            r,m = divmod(nm1,nz1-nz2)
            if m == 0:
                return "1/{}".format(r)
            else:
                return "{}/{}".format(nz1-nz2,nm1)

        else:
            r, m = divmod(nm1, nz2 - nz1)
            # return "{}/{}".format(z2-z1,m1)
            if m == 0:
                return "1/{}".format(r)
            else:
                return "{}/{}".format(nz2-nz1, nm1)

snums = []
while True:
    n = sys.stdin.readline().strip()
    if n:
        snums.append(n)
    else:
        break

res = []
for i in range(len(snums)):
    v = snums[i]
    while True:
        z,m = map(int,v.split('/'))
        # print("z,m",z,m)
        if z == 1:
            res.append("1/{}".format(m))
            break
        if z-1 != 1 and m%(z-1) == 0:
            res.append("1/{}".format(m))
            res.append("1/{}".format(int(m/(z-1))))
            break
        else:
            new_m = ((m // z) + 1) * z
            sub1 = "1/{}".format(new_m // z)
            sub2 = "{}/{}".format(z, m)
            res.append(sub1)
            ret = calc_fraction_sub(sub1, sub2)
            v = ret
    res.sort(key=lambda x:int(x.split('/')[-1]))
    print('+'.join(res))
    res.clear()

# print(res)
