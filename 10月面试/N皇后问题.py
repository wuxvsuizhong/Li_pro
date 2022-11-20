size = int(input().strip())
book = [0 for _ in range(size)]

def is_valid(x,y,book):
    for i in range(0,x):
        if book[i] == y:
            return False
        if x+y == i+book[i] or x-y == i-book[i]:
            return False
    return True



def search(x,book):
    if x == len(book):
        global cnt
        cnt+=1
        return

    for i in range(size):
        if(is_valid(x,i,book)):
            book[x] = i;
            search(x+1,book)
            book[x] = 0;

cnt=0
search(0,book)
print(cnt)



