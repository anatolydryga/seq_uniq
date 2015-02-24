# Extract sequences

For 2 FASTA files creates 2 files with sequences that are unique
and 2 files for sequences that are similar between original FASTA files.

## How to run

``` bash
./seq_uniq.py seq1.fasta seq2.fasta 
```

creates 5 files:
* unique_seq1.fasta sequences from seq1.fasta that are NOT similar to seq2.fasta
* unique_seq2.fasta sequences from seq2.fasta that are NOT similar to seq1.fasta

* shared_seq1.fasta sequences from seq1.fasta that are similar to seq2.fasta
* shared_seq2.fasta sequences from seq2.fasta that are similar to seq1.fasta

* summary.txt counts of total, similar and unique sequences

## Similarity definition

We define 2 nucleotide sequences to be similar if:

1. alignment length is at least half(>=50%) of the shorter sequence

## Example
``` bash
./seq_uniq.py sample_contigs.fa sample_contigs_first_2_seq_similar_with_repeat.fa
```
creates 5 files:
* unique_sample_contigs.fa has 2 seqs
* shared_sample_contigs.fa has 2 seqs
* unique_sample_contigs_first_2_seq_similar_with_repeat.fa has 1 seqs
* shared_sample_contigs_first_2_seq_similar_with_repeat.fa has 3 seqs
* summary for the run(created in current folder)

