import random

if __name__ == "__main__":
    random.seed(10)
    locs = [[input(), _] for _ in range(int(input()))]
    txt = ''
    # for n in locs:
    #     txt += f"{n[1]} {n[0]}\n"
    for i, n1 in enumerate(locs[:-1]):
        for n2 in locs[i+1:]:
            txt += f"{n1[0]} {n2[0]} {random.randint(0, 100)}\n"
    with open(r'utils/temp.txt', "w+") as f:
        f.write(txt)