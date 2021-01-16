import pprint
import re

stack = []
with open("files/newfile.txt", "rt") as fh:
    for i in fh:
        if i != "\n" and re.match(r"^http://wikipedia\.org//wiki/[\w0-9]+$", i):
            stack.append(i.strip("\n"))
dict = {i: stack.count(i) for i in l}
data = sorted(dict.items(), key=lambda x: x[1], reverse=True)
pprint.pprint(data, width=1)
print(len(stack))
