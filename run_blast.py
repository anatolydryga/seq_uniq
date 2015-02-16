import subprocess

class At_least_part_seq_aligned:
    """ two sequences are defined similar if at least half of
        the shorter sequence is aligned.
    """
    def __init__(self, percent_aligned):
        self.ids = None
        if (percent_aligned <= 0 or percent_aligned > 100):
            raise ValueError(
            "Percentage of sequence alignment should be >=0 and smaller than 100.00")
        self.percentage = percent_aligned

    def is_similar(self, blast_output):
        """
            Args:
                blast_output is a line from blastn output produced by Blastn class
                (see Blastn for exact format and order of features)
            Return: True if seqs are similar False if not
            Sequences can be retrieved by similar_ids() method
        """
        self.ids = None
        columns = blast_output.split("\t")
        NUMBER_OF_COLUMNS = 6
        if len(columns) != NUMBER_OF_COLUMNS:
            raise ValueError("Incorrect number of columns in blastn output.")
        (qseqid, sseqid, qlen, slen, pident, length)  = columns
        (qseqid, sseqid, qlen, slen, pident, length)  = (
            qseqid, sseqid, int(qlen), int(slen), float(pident), int(length))
        if (self.get_percent(qlen, length) >= self.percentage or 
            self.get_percent(slen, length) >= self.percentage):
            self.ids = (qseqid, sseqid)
            return True
        return False

    def similar_ids(self):
        """ if sequences are similar return tuple with seq ids
            otherwise return None
        """
        return self.ids

    def get_percent(self, seq_len, alignment_length):
        return alignment_length*100.00/seq_len


class Blastn:
    """ run blastn for 2 FASTA files
    """

    def __init__(self, subject_fasta, query_fasta):
        """ run blastn for 2 fasta file(creates blastdb on the fly)
        """
        self.blast_output = "blast_output.data"
        self.subject = subject_fasta
        self.query = query_fasta

        makeblastdb_command = "makeblastdb -in " + self.subject + " -dbtype nucl"
        blast_command = ("blastn -query " + self.query + " -db " + self.subject +
             " -outfmt '6 qseqid sseqid qlen slen pident length' -num_threads 4 -evalue 1e-5 -out " +
             self.blast_output)
        try:
            subprocess.check_call(makeblastdb_command, shell=True)
            subprocess.check_call(blast_command, shell=True)
        except subprocess.CalledProcessError:
            print "Nucleotide BLAST(blastn) failed."
            raise subprocess.CalledProcessError

    def find_similar_seq_ids(self, similarity): 
        """ all sequence ids that are similar to other sequences from different fasta.

            Args:
                similarity object that has methods: is_similar(), similar_ids()
            returns:
                map with key = fasta file name and value is list of sequence ids that are similar
        """
        similar_seqs = {self.query : [], self.subject : []}
        for line in open(self.blast_output):
            if similarity.is_similar(line):
                (qseq, sseq) = similarity.similar_ids()
                similar_seqs[self.query].append(qseq)
                similar_seqs[self.subject].append(sseq)
        return similar_seqs

