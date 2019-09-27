import random


def cre_asc_seq(n):
    seq = []
    curr = random.randint(-1000, 1000)
    for _ in range(n):
        nxt = curr + random.randint(1, 5)
        seq.append(nxt)
        curr = nxt
    return seq


def cre_desc_seq(n):
    seq = []
    curr = random.randint(-1000, 1000)
    for _ in range(n):
        nxt = curr - random.randint(1, 5)
        seq.append(nxt)
        curr = nxt
    return seq


def merge_seq(seq1, seq2):
    n = len(seq1)
    seq = []
    i1 = 0
    i2 = 0

    while not (i1 == n-1 and i2 == n-1):
        flag = random.randint(0, 1)

        if flag == 0:
            if i1 < n:
                seq.append(seq1[i1])
                i1 += 1
            else:
                seq.append(seq2[i2:])
                break
        else:
            if i2 < n:
                seq.extend(list(seq2[i2]))
                i2 += 1
            else:
                seq.extend(list(seq1[i1:]))
                break
    return seq


seq1 = cre_desc_seq(10)
seq2 = cre_desc_seq(10)
mrg = merge_seq(seq1, seq2)
print(seq1)
print(seq2)
print(mrg)
print(len(mrg))
