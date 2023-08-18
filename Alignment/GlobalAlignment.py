import sys

sys.setrecursionlimit(10000)

f = open("./data/SuperLongTestData.txt", "r") 
mmi = f.readline().strip().split()
v = f.readline().strip()
w = f.readline().strip()
f.close()

MATCH_SCORE = int(mmi[0]) # = 1
MIS_PEN = int(mmi[1])     # = 1 (penalty)
INDEL_PEN = int(mmi[2])   # = 5 (penalty)

# Dynamic Programming Alignment Approach with backtracking pointer recorded in the backtract matrix
# Returns best alignment score with the backtrack matrix
def AlignmentBackTrack(v, w):
    s = [[0 for j in range(len(w)+1)] for i in range(len(v)+1)]
    backtrack = [['' for j in range(len(w)+1)] for i in range(len(v)+1)]
    for i in range(1, len(v)+1):
        s[i][0] = s[i-1][0] - INDEL_PEN
    for j in range(1, len(w)+1):
        s[0][j] = s[0][j-1] - INDEL_PEN
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            m = -1 * MIS_PEN
            if v[i-1] == w[j-1]:
                m = MATCH_SCORE
            s[i][j] = max(s[i-1][j] - INDEL_PEN, s[i][j-1] - INDEL_PEN, s[i-1][j-1] + m)
            if s[i][j] == s[i-1][j] - INDEL_PEN:
                backtrack[i][j] = 'd'
            elif s[i][j] == s[i][j-1] - INDEL_PEN:
                backtrack[i][j] = 'r'
            elif s[i][j] == s[i-1][j-1] + m:
                backtrack[i][j] = 'dr'
    return [s[len(v)][len(w)], backtrack]

# Backtracking to printout the alignment
# Recursively backtrack to print out the alignment
def OutputLCS(backtrack, v, w, i, j):
    if i == 0:
        return ['-'*j + v[:i], w[:j]]
    if j == 0:
        return [v[:i], '-'*i + w[:j]]
    bt = backtrack[i][j]
    if bt == 'd':
        prev = OutputLCS(backtrack, v, w, i-1, j)
        return [prev[0] + v[i-1], prev[1] + '-']
    elif bt == 'r':
        prev = OutputLCS(backtrack, v, w, i, j-1)
        return [prev[0] + '-', prev[1] + w[j-1]]
    elif bt == 'dr':
        prev = OutputLCS(backtrack, v, w, i-1, j-1) 
        return [prev[0] + v[i-1], prev[1] + w[j-1]]
    else:
        print(bt, 'errr!')
        return

f = open("output.txt", "w")
[score, backtrack] = AlignmentBackTrack(v, w)

f.write(str(score) + '\n')
out = OutputLCS(backtrack, v, w, len(v), len(w))
f.write(out[0] + '\n')
f.write(out[1])