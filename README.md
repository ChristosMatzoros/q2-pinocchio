# q2-pinocchio: PaIrwise alignment of long-read NucleOtide sequence data for Classification and quality Control in HIgh-thrOughput

## QIIME 2 Plugin for quality control and taxonomic classification of long sequences


## Installation
#### Step 1: Create q2-pinocchio environment
```shell
mamba create -n q2-pinocchio -c conda-forge -c bioconda -c https://packages.qiime2.org/qiime2/2024.10/metagenome/passed/ -c defaults q2cli q2-types q2-feature-classifier minimap2 bs4 samtools gzip chopper nanoplot
```

#### Step 2: Activate q2-pinocchio environment
```shell
conda activate q2-pinocchio
```

#### Step 3: Installing python package
```shell
pip install .
```
<br>

## Provided Actions


1. **build-index**

    Build a Minimap2 index database from reference sequences.

2. **minimap2-search**

    Search for top hits in a reference database using alignment between the query sequences and reference database sequences using Minimap2. Returns a report of the top M hits for each query (where M=maxaccepts).

3. **filter-reads**

    This method aligns long-read sequencing data (from a FASTQ file) to a set of reference sequences, identifying sequences that match or do not match the reference within a specified identity percentage. The alignment is performed using Minimap2, and the results are processed using Samtools.

4. **extract-reads**

    This method aligns long-read sequencing data (from a FASTA file) to a set of reference sequences, identifying sequences that match or do not match the reference within a specified identity percentage. The alignment is performed using Minimap2, and the results are processed using Samtools.

5. **classify-consensus-minimap2**

    Assign taxonomy to query sequences using Minimap2. Performs alignment between query and reference reads, then assigns consensus taxonomy to each query sequence.


6. **trim**

    Trim long demultiplexed sequences using Chopper tool.


7. **stats**

    Quality control statistics of long-read sequencing data using NanoPlot.
<br>

## How to use it
### Download input data
[Datasets]()



### Examples

* build-index
  - Build Minimap2 index database
  ```shell
  qiime pinocchio build-index --i-reference reference.qza --o-index index.qza --verbose
  ```

<br>

* minimap2-search
  - Generate both hits and no hits for each query. Keep a maximum of one hit per query (primary).
  ```shell
  qiime pinocchio minimap2-search --i-query fasta_reads.qza --i-index index.qza --o-search-results paf.qza --verbose
  ```

  - Generate only hits for each query. Keep a maximum of one hit per query (primary mappings).
  ```shell
  qiime pinocchio minimap2-search --i-query fasta_reads.qza --i-index index.qza --o-search-results paf_only_hits.qza --p-output-no-hits false --verbose
  ```

  - Generate only hits for each query, limiting the number of hits to a maximum of 3 per query. Ensure that each hit has a minimum similarity percentage of 90% to be considered valid.
  ```shell
  qiime pinocchio minimap2-search --i-query fasta_reads.qza --i-index index.qza --o-search-results paf_only_hits_ma3.qza --p-maxaccepts 3 --p-output-no-hits false --verbose
  ```

<br>

* filter-reads
  - Keep mapped (single-end reads)
  ```shell
  qiime pinocchio filter-reads --i-query single-end-reads.qza --i-index index.qza --o-filtered-query mapped_se.qza --verbose
  ```

  - Keep unmapped (single-end reads)
  ```shell
  qiime pinocchio filter-reads --i-query single-end-reads.qza --i-index index.qza --p-keep unmapped --o-filtered-query unmapped_se.qza --verbose
  ```

  - Keep mapped (paired-end reads)
  ```shell
  qiime pinocchio filter-reads --i-query paired-end-reads.qza --i-index index.qza --o-filtered-query mapped_pe.qza --verbose
  ```

  - Keep mapped reads with mapping percentage >= 98% (paired-end reads)
  ```shell
  qiime pinocchio filter-reads --i-query paired-end-reads.qza --i-index index.qza --p-min-per-identity 0.98  --o-filtered-query mapped_pe_over_98p_id.qza --verbose
  ```

<br>

* extract-reads
  - Extract mapped
  ```shell
  qiime pinocchio extract-reads --i-sequences fasta_reads.qza --i-index index.qza --o-extracted-reads mapped_fasta.qza --verbose
  ```
  - Extract unmapped
  ```shell
  qiime pinocchio extract-reads --i-sequences fasta_reads.qza --i-index index.qza --p-extract unmapped --o-extracted-reads unmapped_fasta.qza --verbose
  ```
  - Extract mapped reads with mapping percentage >= 87%
  ```shell
  qiime pinocchio extract-reads --i-sequences fasta_reads.qza --i-index index.qza --p-min-per-identity 0.87 --o-extracted-reads mapped_fasta_ido_ver_87.qza --verbose
  ```

<br>

* classify-consensus-minimap2
  - Assign taxonomy to query sequences using Minimap2
  ```shell
  qiime pinocchio classify-consensus-minimap2 --i-query n1K_initial_reads_SILVA132.fna.qza --i-index ccm_index.qza --i-reference-taxonomy raw_taxonomy.qza --p-n-threads 8 --output-dir classification_output --verbose
  ```

<br>

* trim
  - Filter based on the quality (min)
  ```shell
  qiime pinocchio trim --i-query single-end-reads.qza --p-min-quality 7 --o-filtered-query filt_qual_min.qza --verbose
  ```
  - Filter based on the quality (max)
  ```shell
  qiime pinocchio trim --i-query single-end-reads.qza --p-max-quality 7 --o-filtered-query filt_qual_max.qza --verbose
  ```
  - Headcrop of all sequences ()
  ```shell
  qiime pinocchio trim --i-query single-end-reads.qza --p-headcrop 10 --o-filtered-query headcrop.qza --verbose
  ```
  - Filter based on the length of the sequences (min)
  ```shell
  qiime pinocchio trim --i-query single-end-reads.qza --p-min-length 3000 --o-filtered-query filt_len_min.qza --verbose
  ```

<br>

* stats
  - Generate a visualization to display statistics about the sequences
  ```shell
  qiime pinocchio stats --i-sequences single-end-reads.qza --o-visualization stats.qzv
  ```
  To open:
  ```shell
  qiime tools view stats.qzv
  ```
