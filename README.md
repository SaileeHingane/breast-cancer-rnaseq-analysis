# Breast Cancer RNA-Seq Differential Expression Analysis

End-to-end RNA-seq differential expression analysis of ER-positive and Triple-Negative Breast Cancer using Galaxy Europe, Python, and functional enrichment analysis.

## Project Overview

This project presents an end-to-end RNA-seq differential expression analysis comparing **Estrogen Receptor-positive (ER+)** and **Triple-Negative Breast Cancer (TNBC)** samples from NCBI using the Galaxy Europe platform. The workflow includes quality assessment, read alignment, gene quantification, differential expression analysis, gene annotation, functional enrichment analysis, and biological interpretation. Downstream analyses were further performed using Microsoft Excel, Python, and g:Profiler to identify biologically relevant genes and pathways associated with breast cancer subtypes.

## Biological Question

1. Which genes are differentially expressed between ER-positive and Triple-Negative Breast Cancer (TNBC)?

2. Which biological processes and molecular pathways are enriched among these differentially expressed genes?

## Dataset

- **Data Source:** NCBI Sequence Read Archive (SRA)
- **Platform:** Illumina RNA-Seq
- **Samples:** 6 (3 ER+, 3 TNBC)
- **Bioproject:** PRJNA251383
- **Layout:** PAIRED

| Sample ID | Breast Cancer Subtype |
|------------|----------------------|
| SRR1313124 | ER+ |
| SRR1313125 | ER+ |
| SRR1313126 | ER+ |
| SRR1313132 | TNBC |
| SRR1313133 | TNBC |
| SRR1313134 | TNBC |

## Workflow

The analysis was performed using the Galaxy Europe platform, followed by downstream processing in Microsoft Excel, Python, and g:Profiler.

```
NCBI SRA RNA-Seq Dataset
            │
            ▼
Quality Assessment (Falco)
            │
            ▼
Quality Summary (MultiQC)
            │
            ▼
Read Alignment (HISAT2, hg19)
            │
            ▼
Gene Quantification (featureCounts)
            │
            ▼
Differential Expression Analysis (DESeq2)
            │
            ▼
Filtering
• Adjusted p-value (padj < 0.05)
• Log₂ Fold Change ≥ 1 or ≤ -1
            │
            ▼
Gene Annotation (annotateMyIDs)
            │
            ▼
Join DESeq2 Results with Gene Annotation
            │
            ▼
Export to Excel
            │
            ▼
Split into Upregulated and Downregulated Genes
            │
            ▼
Select Top 20 Genes
            │
            ▼
Python Annotation (MyGene.info API)
            │
            ▼
Functional Enrichment Analysis
(GO, KEGG, Reactome & WikiPathways)
            │
            ▼
Biological Interpretation
```
## Tools Used

| Category | Tool |
|----------|------|
| Quality Control | Falco |
| QC Summary | MultiQC |
| Read Alignment | HISAT2 |
| Gene Quantification | featureCounts |
| Differential Expression | DESeq2 |
| Gene Annotation | annotateMyIDs |
| Spreadsheet Processing | Microsoft Excel |
| Functional Annotation | Python (MyGene.info API) |
| Functional Enrichment | g:Profiler |

## Key Results

| Analysis | Result |
|----------|--------|
| Samples Analysed | 6 RNA-seq samples (3 ER+, 3 TNBC) |
| Read Alignment | ~91% overall alignment rate (HISAT2) |
| Differential Expression | 25,702 differentially expressed genes (DEGs) |
| Filtering Criteria | padj < 0.05 and log₂FC ≥ 1 or ≤ -1 |
| Differential Expression_Filtered | 4,042 differentially expressed genes (DEGs) |
| Gene Annotation | annotateMyIDs (Galaxy) + MyGene.info (Python) |
| Functional Enrichment | GO, KEGG, Reactome and WikiPathways (g:Profiler) |

