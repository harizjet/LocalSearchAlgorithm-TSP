import random

if __name__ == "__main__":
    locs = [input() for _ in range(int(input()))]
    txt = ''
    for i, n1 in enumerate(locs[:-1]):
        for n2 in locs[i+1:]:
            txt += f"{n1} {n2} {random.randint(0, 100)}\n"
    with open('temp.txt', "w+") as f:
        f.write(txt)