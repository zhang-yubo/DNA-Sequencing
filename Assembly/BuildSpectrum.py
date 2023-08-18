import json

f = open("./data/assembly_20000_reads_without_positions.fasta", "r")
reads = f.readlines()
f.close()

reads = [x.strip() for x in reads]
reads = reads[1::2]

k = 20
ERR_FILTER_LEN = 5
REPEAT_LEN = 10

kmers = {}
for i, r in enumerate(reads):
    for j in range(len(r) - k + 1):
        kmer = r[j:j+k]
        index = kmers.get(kmer)
        if index:
            index.append(i)
            kmers.update({kmer : index})
        else:
            kmers.update({kmer : [i]})

keys = list(kmers.keys())
for k in keys:
    v = kmers.get(k)
    if len(v) < ERR_FILTER_LEN:
        del kmers[k]


f = open("spectrum.txt", "w")
counts = {}
keys = list(kmers.keys())
for k in keys:
    v = kmers.get(k)
    # f.write(k + '\t' + json.dumps(v) + '\n')
    # write_times = max(1, min(int(len(v) / REPEAT_LEN), 2))
    for i in range(1):
        f.write(k + '\n')
    c = counts.get(len(v))
    if c:
        c += 1
        counts.update({len(v) : c})
    else:
        counts.update({len(v) : 1})

# for i in range(80):
#     c = counts.get(i)
#     if c:
#         f.write(str(i) + '\t' + str(c) + '\n')

f.close()

