from scipy.spatial import KDTree

tree = KDTree([(1,2), (3,4), (1,4)])
print(tree.query((1,5)))
