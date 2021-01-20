import pprint
import re
import os

"""
running 'wikiscraper.main' yields a directory containing
a .txt file for each sub-tree. The filenames correspond to the root
nodes of each sub-tree. So, each tree is a directory.
Each sub-tree is a within that directory. Each filename is a root node.
The urls contained within each file are branches of a sub-tree. 
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
