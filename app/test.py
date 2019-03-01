from collections import OrderedDict
childList = {}

childList[(2,3)] = [3, 25]
childList[(2,1)] = [2, 40]
childList[(1,2)] = [3, 50]
childList[(1,3)] = [2, 19]
#childList = {(2,3): [3, 25], (2,1): [2, 40], (1,2): [3, 50], (1,3):[2, 19]}
sorted_childre = OrderedDict(sorted(childList.items(), key=lambda x: x[1], reverse = True))
print(sorted_childre)
print(sorted_childre.keys())