## 🧬 Interesting DNA Sequencing Experiment 🧬

**When it comes to our genome, we could be dealing with strings on magnitudes of billions 🤯**

Simple tasks on shorter strings becomes not so simple for longer strings. I took on three common tasks in DNA sequencing

- Read Mapping 🗺️
  - 10,000 short reads, each about 60 chars in length mapped with 1,000 genomes, each 10,000 chars in length
  - To make it fast, I used an idea called minimizers to search for the reads
  - All done in 20 seconds

- Genome Assembly 🛠️
  - First a whole genome is break down, so I can put these small parts back together
  - Whole genome split into 20,000 pieces of 50 - 60 chars
  - Done in under a second

- Global Alignment 📏
  - DNA reads can have mistakes, and also everyone's genome is different based on mutations in some parts
  - So I took two DNA segments and altered each one (insert, delete, subsitute) so that they look the most similar
