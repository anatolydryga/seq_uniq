from Bio import SeqIO

def split_fasta_files_on_seq_ids(seq_ids, fasta_files, fasta_files_w_seq_ids, fasta_files_w_no_seq_ids):
    """ for list of fasta files and list of seq ids
        split each file into two files: one with seq ids and one with rest of seq ids.
    
        Args:
            seq_ids is a map w key is fasta file name and value is list of seq ids

            fasta_files list of fasta for split on seq_ids

            fasta_files_w_seq_ids map w key is a  fasta file and value is fasta file name
            with sequence id from seq_ids

            fasta_files_w_no_seq_ids map w key is a  fasta file and value is fasta file name
            with sequence id NOT from seq_ids(rest of ids from fasta file)
        Return:
            list of filename, number of sequence, number of similar sequnces and number of unique seq
            for each filename.
    """
    summary = []
    for fasta in fasta_files:
        if len(seq_ids[fasta]) > 0:
            (n_total, n_similar, n_unique) = split_fasta_on_seq_ids(seq_ids[fasta], fasta, 
                fasta_files_w_seq_ids[fasta], fasta_files_w_no_seq_ids[fasta])
            print "FASTA file " + fasta + " has:"
            print "\ttotal   # of sequences: " + str(n_total)
            print "\tsimilar # of sequences: " + str(n_similar)
            print "\tunique  # of sequences: " + str(n_unique)
            summary.append(fasta)
            summary.append(n_total)
            summary.append(n_similar)
            summary.append(n_unique)
        else:
            print "FASTA file :" + fasta + " has only unique ids. NO additional files are created."
            summary.append(fasta)
            n_total = number_of_seqs(fasta) 
            summary.append(n_total)
            summary.append(0)
            summary.append(n_total)
    return summary

def number_of_seqs(fasta):
    """yet another counter for number of sequences in FASTA.
    """
    ids = SeqIO.index(fasta_file, "fasta")
    n_total = len(ids)
    ids.close()
    return n_total

def split_fasta_on_seq_ids(seq_ids, fasta_file, with_seq_ids, without_seq_ids):
    """ split fasta file into 2 fasta files: one with sequence identifiers
        and one without.

        Args:
            seq_ids list of fasta identifiers that will be extracted to with_seq_ids file
            fasta_file file name for fasta that has all ids
            with_seq_ids filname to be written with seq ids
            without_seq_ids filname to be written withOUT seq ids
        Raises:
            VelueError if seq_ids list is empty
            VelueError if some ids from seq_ids list are not present in fasta_file
        Return:
        tuple with 3 elements: # of records in fasta file,
           # of records with seq ids( should be equal to # of seq_ids),
           # of records without seq_ids
    """
    if not seq_ids:
        raise ValueError("seq_ids list should have at least one id from fasta file.")

    ids = SeqIO.index(fasta_file, "fasta")
    n_total = len(ids)
    if not set(seq_ids).issubset(set(ids)):
        raise ValueError("all seq_ids should be from fasta file.")
    ids.close()

    w_ids = open(with_seq_ids, 'w')
    w_no_ids = open(without_seq_ids, 'w')
    num_w_ids = 0
    num_w_no_ids = 0
    for record in SeqIO.parse(fasta_file, "fasta"):
        if record.id in seq_ids:
            SeqIO.write(record, w_ids, "fasta")
            num_w_ids += 1
        else:
            SeqIO.write(record, w_no_ids, "fasta")
            num_w_no_ids += 1
    w_ids.close()
    w_no_ids.close()
    assert n_total == num_w_no_ids + num_w_ids
    return (n_total, num_w_ids, num_w_no_ids)

