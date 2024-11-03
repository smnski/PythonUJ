def flatten(sequence: list) -> list[int]:
    result = []
    for item in sequence:
        if isinstance(item, (list, tuple)):
            result.extend(flatten(item))
        else:
            result.append(item) 
    return result

if __name__ == '__main__':
    seq = [1, [1, 2, 3], [1, [2, 3]]]
    assert flatten(seq) == [1, 1, 2, 3, 1, 2, 3]