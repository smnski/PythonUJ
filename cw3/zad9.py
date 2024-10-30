def sumSeqs(arr):
    result = []
    for i in range(len(arr)):
        result.append(sum(arr[i]))

    return result

if __name__ == "__main__":
    assert sumSeqs([[],[4],(1,2),[3,4],(5,6,7)]) == [0,4,3,7,18]