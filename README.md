

# periscope_multi

A modified version of periscope : https://github.com/sheffield-bioinformatics-core/periscope
A tool to quantify sub-genomic RNA (sgRNA) expression in SARS-CoV-2 artic network amplicon sequencing data.

# Citing

TODO

# Requirements
periscope runs Linux. 

* conda
* Your raw fastq files from the artic protocol
* Install periscope_multifasta

# Installation
```
git clone https://github.com/ThomasBaudeau/periscope_multifasta && cd periscope_multifasta
conda env create -f environment.yml
conda activate periscope_multifasta
pip install .
```


# Quick Running (test sample)

A fastq file is provided for use as an example to launch the tool.


```
conda activate periscope_multifasta

periscope_multi --fastq tests/ont/test.fastq --gff periscope_multi/resources/covid.gff

```



# Execution

```
conda activate periscope_multifasta

periscope_multi \
    --fastq-dir <PATH_TO_DEMUXED_FASTQ> \ (ont only)
    OR
    --fastq <FULL_PATH_OF_FASTQ_FILE(s)> \ (space separated list of fastq files, you MUST use this for Illumina data)
    --output-prefix <PREFIX> \
    --sample <SAMPLE_NAME> \
    --artic-primers <ASSAY_VERSION; V1,V2,V3,V4,2kb,midnight> \
    --resources <PATH_TO_PERISCOPE_RESOURCES_FOLDER> \
    --technology <SEQUECNING TECH; ont or illumina> \
    --threads <THREADS>
    --gff <PATH_OF_GFF_FILE>
```

For custom primers use `--artic-primers` argument followed by:
* path to the custom amplicons file
* path to the custom primers file

To view the requirements for these files and advice on how to generate them, go to [Custom amplicons and primers section](#custom123).

`output-prefix` will be the directory and start of the filename for the output.

So if you put `./SAMPLE1` for this argument outputs will go in the current working directory prefixed by "SAMPLE1". 

***Note*** - for illumina data please use --fastq <FASTQ_R1>.fastq.gz <FASTQ_R2>.fastq.gz and --technology illumina


## Counting

_This step takes roughly 1minute per 10k reads_
_Our median read count is ~250k and this will take around 25minutes_

* Read bam file
* Filter unmapped and secondary alignments
* Assign amplicon to read (using artic align_trim.py)
* Assign read to ORF (using the different references)
* Classify read 
* Normalise a few ways

## Outputs:

#### <OUTPUT_PREFIX>.fastq

A merge of all files in the fastq directory specified as input.

#### <OUTPUT_PREFIX>_periscope_counts.csv

The counts of genomic, sub-genomic and normalisation values for known ORFs

#### <OUTPUT_PREFIX>_periscope_amplicons.csv

The amplicon by amplicon counts, this file is useful to see where the counts come from. Multiple amplicons may be represented more than once where they may have contributed to more than one ORF.

#### <OUTPUT_PREFIX>_periscope_novel_counts.csv

The counts of genomic, sub-genomic and normalisation values for non-canonical ORFs

#### <OUTPUT_PREFIX>.bam

minimap2 mapped reads and index with no adjustments made.

#### <OUTPUT_PREFIX>_periscope.bam

This is the original input bam file and index created by periscope with the reads specified in the fastq-dir. This file, however, has tags which represent the results of periscope:

- XA is the amplicon number
- XC is the assigned class (gDNA or sgDNA)
- XO is the orf assigned

These are useful for manual review in IGV or similar genome viewer. You can sort or colour reads by these tags to aid in manual review and figure creation.


#### <OUTPUT_PREFIX>_base_counts.csv

Counts of each base at each position

#### <OUTPUT_PREFIX>_base_counts.png

Plot of each position and base composition

# Running Tests

We provide a sam file for testing the main module of periscope.

reads.sam contains 19 reads which have been manually reviewed for the truth

```
cd <INSTALLATION_PATH>/periscope/tests

pytest test_search_for_sgRNA.py 
```

# <a id="custom123"></a>Custom Amplicons and Primers

## Custom Amplicons File
Each line must be an amplicon entry with 4, tab-delimited, features:
* Chrom - name for the reference sequence
* Start - zero-based starting position of the amplicon in the ref seq
* End - one-based ending position of the amplicon in the ref seq
* Name - name for the amplicon

Example amplicons.bed file:

```
MN908947.3	30  410 nCoV-2019_1
MN908947.3	320	726	nCoV-2019_2
MN908947.3	642	1028	nCoV-2019_3
MN908947.3	943	1337	nCoV-2019_4
MN908947.3	1242	1651	nCoV-2019_5
MN908947.3	1573	1964	nCoV-2019_6
```

## Custom Primers File
Each line must be a primer entry with 5, tab-delimited, features:
* Chrom - name for the reference sequence
* Start - zero-based starting position of the primer in the ref seq
* End - one-based ending position of the primer in the ref seq
* Primer ID - ID of the primer, including the amplicon number (inbetween underscores) and the primer direction (LEFT or RIGHT)
* Primer Pool - primer pool assignment

Example primers.bed file:

```
MN908947.3	30	54	nCoV-2019_1_LEFT	nCoV-2019_1
MN908947.3	385	410	nCoV-2019_1_RIGHT	nCoV-2019_1
MN908947.3	320	342	nCoV-2019_2_LEFT	nCoV-2019_2
MN908947.3	704	726	nCoV-2019_2_RIGHT	nCoV-2019_2
MN908947.3	642	664	nCoV-2019_3_LEFT	nCoV-2019_1
MN908947.3	1004	1028	nCoV-2019_3_RIGHT	nCoV-2019_1
```
