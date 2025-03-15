arr = []

n = int(input())

for i in range(n):
    text = input().split()
    if text[0] == "insert":
        i = int(text[1])
        e = int(text[2])
        arr.insert(i, e)
    if text[0] == "print":
        print(arr)
    if text[0] == "remove":
        e = int(text[1])
        arr.remove(e)
    if text[0] == "append":
        e = int(text[1])
        arr.append(e)
    if text[0] == "sort":
        arr.sort()
    if text[0] == "pop":
        arr.pop()
    if text[0] == "reverse":
        arr.reverse()
