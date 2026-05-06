<div align="center">

# MapReduce Search Engine

**Distributed TF-IDF indexing over a Wikipedia corpus on Hadoop**

[![Python](https://img.shields.io/badge/Python-3.8-3776AB?logo=python&logoColor=white)](https://python.org)
[![Hadoop](https://img.shields.io/badge/Apache_Hadoop-3.3-66CCFF?logo=apachehadoop&logoColor=black)](https://hadoop.apache.org)
[![MapReduce](https://img.shields.io/badge/MapReduce-Streaming-FF6D00)](https://hadoop.apache.org/docs/stable/hadoop-streaming/HadoopStreaming.html)

Builds a TF-IDF weighted inverted index over a Wikipedia article corpus using three chained Hadoop MapReduce jobs. Each job runs independently and passes its output to the next stage via HDFS.

</div>

---

## Table of Contents

- [Overview](#overview)
- [Pipeline](#pipeline)
- [How TF-IDF is Computed](#how-tf-idf-is-computed)
- [Input Format](#input-format)
- [Running the Jobs](#running-the-jobs)
- [Project Structure](#project-structure)

---

## Overview

The pipeline processes a CSV corpus of Wikipedia article sections. Each row contains an article ID and section text. Three MapReduce jobs run in sequence to build a full TF-IDF inverted index:

1. **Enumeration**: assigns a unique integer ID to every term in the corpus
2. **IDF**: counts how many documents each term appears in
3. **Indexer**: computes normalized TF per article then multiplies by IDF

The output of each job feeds into the next. After Jobs 1 and 2, `vocabulary.py` merges their outputs into a single lookup file (`vocab_out.txt`) that the Indexer uses at runtime.

All mappers strip stopwords and lowercase tokens before emitting. The IDF formula used is smoothed: `log((N / (1 + df)) + 1)`.

---

## Pipeline

```
┌─────────────────────────────────────────────────────────┐
│  Input: Wikipedia CSV corpus (HDFS)                     │
│  Columns: article_id, ..., section_text                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Job 1: Enumeration                                     │
│  mapper_enumeration.py                                  │
│    Tokenize, lowercase, strip stopwords                 │
│    Emit: word -> 1                                      │
│  reducer_enumeration.py                                 │
│    Assign sequential integer ID to each unique word     │
│    Output: word  ID                          (en_out)   │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Job 2: IDF                                             │
│  mapper_idf.py                                          │
│    Tokenize, lowercase, strip stopwords                 │
│    Emit: word -> article_id                             │
│  reducer_idf.py                                         │
│    Count unique documents per term                      │
│    Output: word  doc_count                  (idf_out)   │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  vocabulary.py (local)                                  │
│    Merge en_out + idf_out                               │
│    Output: vocab_out.txt  (word -> ID, doc_count)       │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  Job 3: Indexer                                         │
│  mapper_indexer.py                                      │
│    Load vocab_out.txt                                   │
│    Compute normalized TF per article                    │
│    Emit: term_id,article_id -> tf                       │
│  reducer_indexer.py                                     │
│    Aggregate TF, compute IDF, multiply to get TF-IDF    │
│    Output: article_id  tf_idf_score                     │
└─────────────────────────────────────────────────────────┘
```

---

## How TF-IDF is Computed

| Component | Formula |
|:---|:---|
| TF (normalized) | `term_count_in_doc / total_terms_in_doc` |
| IDF (smoothed) | `log((N / (1 + df)) + 1)` |
| TF-IDF | `TF * IDF` |

Where `N` is the total number of documents and `df` is the document frequency of the term. Smoothing prevents division by zero for unseen terms.

---

## Input Format

The corpus is a CSV file where each row represents one article section:

```
article_id, col2, col3, section_text
```

The mappers read `columns[0]` as `article_id` and `columns[3]` as `section_text`. All other columns are ignored.

---

## Running the Jobs

Make sure the corpus CSV is uploaded to HDFS before starting.

**Job 1: Enumeration**
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /input/corpus.csv \
  -output /output/enumeration \
  -mapper mapper_enumeration.py \
  -reducer reducer_enumeration.py \
  -file mapper_enumeration.py \
  -file reducer_enumeration.py
```

**Job 2: IDF**
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /input/corpus.csv \
  -output /output/idf \
  -mapper mapper_idf.py \
  -reducer reducer_idf.py \
  -file mapper_idf.py \
  -file reducer_idf.py
```

**Build vocabulary (local)**
```bash
# Copy job outputs from HDFS
hdfs dfs -getmerge /output/enumeration en_out.txt
hdfs dfs -getmerge /output/idf idf_out.txt

# Merge into vocab_out.txt
python vocabulary.py > vocab_out.txt
```

**Job 3: Indexer**
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /input/corpus.csv \
  -output /output/index \
  -mapper mapper_indexer.py \
  -reducer reducer_indexer.py \
  -file mapper_indexer.py \
  -file reducer_indexer.py \
  -file vocab_out.txt
```

---

## Project Structure

```
Search-Engine-MapReduce-Hadoop/
├── mapper_enumeration.py  <- tokenize, strip stopwords, emit word -> 1
├── reducer_enumeration.py <- assign unique integer ID per term
├── mapper_idf.py          <- emit word -> article_id per occurrence
├── reducer_idf.py         <- count unique documents per term
├── mapper_indexer.py      <- compute normalized TF, look up term ID
├── reducer_indexer.py     <- aggregate TF, compute IDF, output TF-IDF
├── vocabulary.py          <- merges en_out + idf_out into vocab_out.txt
└── out/                   <- sample job outputs
```
