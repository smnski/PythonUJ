def sum_seq(sequence: list) -> int:
    result = 0
    for item in sequence:
        if isinstance(item, (list, tuple)):
            result += sum_seq(item)
        else:
            result += item
    
    return result

if __name__ == "__main__":
    seq = [1, [1, 2, 3], [1, [2, 3]]]
    assert sum_seq(seq) == 13