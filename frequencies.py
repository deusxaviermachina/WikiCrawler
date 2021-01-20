import pprint
import re
import os

<<<<<<< HEAD
"""
running 'wikiscraper.main' yields a [root node].txt file for each sub-tree.
So, each tree is a directory. Each sub-tree is a file within that directory.
The urls contained within each [root node] file are branches (which may themselves be
roots to other sub-trees)
"""
tree = os.listdir("files")

nodes= []
for subtree_root in tree:
    with open(f"files/{subtree_root}", "rt") as fh:
        for subtree_branch in fh:
            if subtree_branch != "\n" and re.match(r"^http://wikipedia\.org//wiki/[\w0-9]+$",subtree_branch):
                nodes.append(subtree_branch.strip("\n"))

"""
map nodes to frequencies and sort in ascending order of frequencies--strongly connected 
nodes will rank higher than weakly connected nodes, with "connectedness"
the assumption is that the stronger connections is a reliable proxy for
a semantic connection between the subjects of the articles
"""
data = {node.strip("\n"): nodes.count(node) for node in nodes}
data = sorted(data.items(), key=lambda x:x[1], reverse=True)
pprint.pprint(data)
=======
stack = []
with open("files/newfile.txt", "rt") as fh:
    for i in fh:
        if i != "\n" and re.match(r"^http://wikipedia\.org//wiki/[\w0-9]+$", i):
            stack.append(i.strip("\n"))
dict = {i: stack.count(i) for i in l}
data = sorted(dict.items(), key=lambda x: x[1], reverse=True)
pprint.pprint(data, width=1)
print(len(stack))
>>>>>>> b789532c21a449dec41a91b10bc4beddc938bf7c
