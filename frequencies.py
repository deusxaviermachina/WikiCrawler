import pprint
import re
import os

"""
running 'wikiscraper.main' yields a [root node].txt file for each sub-tree.
So, each tree is a directory. Each sub-tree is a file within that directory.
The urls contained within each [root node] file are its branches (which may themselves be
roots of other sub-trees)
"""

tree = os.listdir("files")

nodes= []
for subtree_root in tree:
    root_name = subtree_root.replace("httpwikipediaorgwiki", "").replace(".txt", "")
    with open(f"files/{subtree_root}", "rt") as fh:
        for subtree_branch in fh:
            if subtree_branch != "\n" and re.match(r"^http://wikipedia\.org//wiki/[\w0-9]+$",subtree_branch):
                nodes.append(subtree_branch.split("wiki/")[1])
    nodes.append(root_name)


"""
map nodes to frequencies and sort in ascending order of frequencies--strongly connected 
nodes will rank higher than weakly connected nodes.
"""
data = {node.strip("\n"): nodes.count(node) for node in nodes}
data = sorted(data.items(), key=lambda x:x[1], reverse=True)
pprint.pprint(data)
