import math

def make_hash_iter(inp: str, mul_coef: int):
    def reverse(i: int):
        return str(i)[::-1]

    numb = [int(l) for l in inp]
    hash_str = [reverse(math.trunc(math.radians(i)*mul_coef)) for i in numb]

    # ['355401161', '6058802461', '86549711'] складываем посимвольно
    hash_len = [len(i) for i in hash_str]
    hash_base = []
    for i in range(0, max(hash_len)):
        base = 0
        for one_str in hash_str:
            try:
                n = int(one_str[i])
            except:
                n = 0
            base += n
        hash_base.append(str(base))

    return ''.join(hash_base)

def make_hash(numb: int, amount: int):
    n_str = str(numb)

    mul_coef = 1
    for i in range(0, amount):
        mul_coef *= 10

    for i in range(0, 1):
        n_str = make_hash_iter(n_str, mul_coef)[:amount]

    return n_str

print(make_hash(5433, 15))
