prices = {
    "A": 0.01, "B": 0.02, "C": 0.03, "D": 0.04, "E": 0.05, "F": 0.06, "G": 0.07, "H": 0.08, "I": 0.09, "J": 0.10,
    "K": 0.11, "L": 0.12, "M": 0.13, "N": 0.14, "O": 0.15, "P": 0.16, "Q": 0.17, "R": 0.18, "S": 0.19, "T": 0.20,
    "U": 0.21, "V": 0.22, "W": 0.23, "X": 0.24, "Y": 0.25, "Z": 0.26
}


def sort_key(item):
    group = item.group
    name = group.name
    number = int(name[0:-2]) + prices[name[-1]]
    return number


def sort_teachingS(lst):
    return sorted(lst, key=sort_key, reverse=True)
