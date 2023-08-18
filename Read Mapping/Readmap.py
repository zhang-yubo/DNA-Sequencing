import time, json

start_time = time.time()

genomes = []
for i in range(1000):
    filename = "./data/readmapping_10000_genome_" + str(i) + ".fasta"
    f_genome = open(filename, "r")
    f_genome.readline()
    genome = f_genome.readlines()
    genome = [x.strip() for x in genome]
    genome = ''.join(genome)
    genomes.append(genome)

f_reads = open("./data/readmapping_10000_reads.fasta", "r")
reads = f_reads.readlines()
reads = [x.strip() for x in reads][1::2]

w = 30 # 21
k = 21 # 15

def ComputeGenomeMinimizers(minimap, genome, genome_no, w, k):
    for i in range(len(genome) - w + 1):
        window = genome[i:i+w]
        mini = window[:k]
        for j in range(w - k + 1):
            kmer = window[j:j+k]
            if kmer < mini:
                mini = kmer
        current_match = minimap.get(mini)
        if current_match and genome_no not in current_match:
            current_match.append(genome_no)
            minimap.update({mini : current_match})
        else:
            minimap.update({mini : [genome_no]})

def ComputeReadMinimizers(read, w, k):
    minimizers = []
    for i in range(len(read) - w + 1):
        window = read[i:i+w]
        mini = window[:k]
        for j in range(w - k + 1):
            kmer = window[j:j+k]
            if kmer < mini:
                mini = kmer
        if mini not in minimizers:
            minimizers.append(mini)
    return minimizers

# match each minimizer in each whole genome with findings in each reads
minimap = {}
for i, g in enumerate(genomes):
    ComputeGenomeMinimizers(minimap, g, i, w, k)

# f = open("zdumps.txt", "w")
# f.write(json.dumps(minimap))
# f.close()

# f = open("zoutput.txt", "w")
# f_read = open("zdumps.txt", "r")
# minimap = f_read.readline().strip()
# minimap = json.loads(minimap)

# count the number of reads matched with each genome
genome_to_reads = {}
# f_debug = open("zdebug.txt", "w")
for i, r in enumerate(reads):
    minimizers = ComputeReadMinimizers(r, w, k)
    matches = []
    for m in minimizers:
        match = minimap.get(m)
        if match is not None:
            for genome_no in match:
                matches.append(genome_no) # add the genomes which contain such a minimizer in the read
        # else:
        #     f_debug.write(m + " no match" + '\n')
    for most_match in set(matches):
        count_most_match = matches.count(most_match)
        if count_most_match >= (len(minimizers) * 0.3): # filter, include if more than 30% of minimizers in the read is present in the genome
            current_count = genome_to_reads.get(most_match)
            if current_count:
                genome_to_reads.update({most_match : current_count + 1})
            else:
                genome_to_reads.update({most_match : 1})

f_out = open("genome_popularity.txt", "w")
genome_sorted_by_matches = reversed(sorted(genome_to_reads.keys(), key=lambda x : genome_to_reads.get(x)))
for g in genome_sorted_by_matches:
    f_out.write(str(g) + '\t' + str(genome_to_reads.get(g)) + '\n')
    
f_out.write(json.dumps(genome_to_reads))


end_time = time.time()
print("runtime: " + str(end_time - start_time) + "s")