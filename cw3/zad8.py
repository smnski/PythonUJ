def getUnion(seq1, seq2):
    return list(set(seq1) | set(seq2))
    

def getIntersection(seq1, seq2):
    return list(set(seq1) & set(seq2))

if __name__ == "__main__":
    assert sorted(getIntersection("abcde12345", "bde24")) == ["2", "4", "b", "d", "e"]
    assert sorted(getUnion("ab12", "bc23")) == ["1", "2", "3", "a", "b", "c"]