import random

def is_sorted(x):
    for i in range(len(x)-1):
        if x[i] > x[i+1]:
            return False
    return True

def bogo_sort(x):
    shuffles = 0
    while not is_sorted(x):
        shuffles += 1
        random.shuffle(x)
    return shuffles

def big_bogo(num):
    num_list = []
    for i in range(num):
        num_list.append(i)
    random.shuffle(num_list)
    return bogo_sort(num_list)

