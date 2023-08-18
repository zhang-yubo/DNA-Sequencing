import statistics

genomes_no = [489, 622, 146, 358, 377] 
# chosen based on output in genome_popularity.txt, 
# these genomes have significantly more minimizers that match with reads

genomes = []
for g in genomes_no:
    f = open("./data/readmapping_10000_genome_" + str(g) + ".fasta", "r")
    f.readline()
    genome = f.readlines()
    genome = [x.strip() for x in genome]
    genome = ''.join(genome)
    genomes.append(genome)

f = open("./data/readmapping_10000_reads.fasta", "r")
reads = f.readlines()
reads = [x.strip() for x in reads][1::2]

k = 14

readmap = {}
for g_no, g in enumerate(genomes):
    for i in range(len(g) - k + 1):
        kmer = g[i:i+k]
        current_match = readmap.get(kmer)
        if current_match is None:
            readmap.update({kmer : [g_no]})
        else:
            if g_no not in current_match:
                current_match.append(g_no)
                readmap.update({kmer : current_match})

reads_to_genome = []
for i, r in enumerate(reads):
    segments = []
    for i in range(3):
        segments.append(r[i*k:i*k+k])
    segments.append(r[len(r)-k:])
    matches = []
    for seg in segments:
        m = readmap.get(seg)
        if m is not None:
            matches.append(statistics.mode(m))
    if len(matches) == 0:
        matches.append(i % 4)
    reads_to_genome.append(matches)
    
f = open("output.txt", "w")
for i, m in enumerate(reads_to_genome):
    best_match = statistics.mode(m)
    f.write(">read_" + str(i) + "\t matched to Genome Number " + str(genomes_no[best_match]) + '\n')
