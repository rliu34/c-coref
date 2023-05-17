from stat_parser import Parser, display_tree
import nltk
# import recoref

parser = Parser()

sentence = "John knows that he saw himself."
tree = parser.parse(sentence)

#print(tree.treepositions())

# paths = []
# for path in tree.treepositions():
#     if isinstance(tree[path], nltk.tree.tree.Tree):
#         print("--")
#         print(path)
#         print(len(path))
#         print(tree[path].label())
#         print(tree[path].leaves())
#         paths.append(path)

display_tree(tree)

# print(recoref.c_command(sentence, "Mary", "she"))

