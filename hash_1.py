
def get_sum(i: int):
    return sum([int(s) if s != '0' else 3 for s in str(i)])

def flat_ord(n_str: str):
    n_str_rot = n_str[1:] + n_str[:1]

    n_ord = [get_sum(ord(lit)) for lit in n_str_rot]
    n_flat = []
    n = 1
    for i in n_ord:
        n_flat.append(str(i*n).replace('0', ''))
        n *= 10


    return ''.join(n_flat)

def make_hash(numb: int):
    n_str = str(numb)
    for i in range(0, 5):
        n_str = flat_ord(n_str)

    return n_str

print(make_hash(543))

