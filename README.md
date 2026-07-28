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

## Analysis Summary

| Step | Outcome |
|------|---------|
| RNA-seq samples analysed | 6 (3 ER+, 3 TNBC) |
| Total genes analysed | 25,702 |
| Read alignment | ~91% overall alignment rate using HISAT2 |
| Differentially expressed genes | 3,735 (padj < 0.05; log₂FC ≥ 1 or ≤ -1) |
| Gene annotation | annotateMyIDs (Galaxy) and MyGene.info (Python) |
| Functional enrichment | GO, KEGG, Reactome and WikiPathways using g:Profiler |

## Data Visualization

The quality and differential expression analyses were assessed using standard RNA-seq visualizations generated in Galaxy.

- **MultiQC Report** – Summarizes sequencing quality metrics across all samples.
- **PCA Plot** – Evaluates sample clustering based on global gene expression patterns.
- **MA Plot** – Displays differential gene expression by comparing log₂ fold changes against mean normalized expression.
- **Heatmap** – Visualizes expression patterns of differentially expressed genes across samples.
- **Volcano Plot** – Highlights significantly upregulated and downregulated genes based on statistical significance and fold change.

## Downstream Data Processing

Following differential expression analysis, the annotated DEG table was exported to Microsoft Excel for downstream processing.

The data were further processed by:

- Separating upregulated (log₂FC ≥ 1) and downregulated (log₂FC ≤ -1) genes.
- Ranking genes based on adjusted p-value (padj).
- Selecting the Top 20 significantly upregulated and Top 20 significantly downregulated genes.
- Automating functional annotation of the selected genes using a custom Python script and the MyGene.info API.
- Performing functional enrichment analysis using g:Profiler.

## Top Differentially Expressed Genes

The analysis identified several genes that clearly distinguished ER-positive and TNBC samples. The Top 20 significantly upregulated and Top 20 significantly downregulated genes were selected based on adjusted p-value and log₂ fold change for further functional analysis.

Gene-level annotation helps us to understand the known biological role of each differentially expressed gene

**Note:** 1) The complete annotated Top 20 upregulated and Top 20 downregulated gene lists, including gene summaries, GO annotations and identifier mappings, are provided in the annotated Excel workbook located in the **results/** directory. 

2) A small number of entries in the Top20 tables show "NA" for GeneSymbol/GeneName, as the corresponding Entrez ID could not be resolved during the Galaxy annotateMyIDs step.

  ## Biological Findings

The functional enrichment analysis highlighted distinct molecular characteristics between the two breast cancer subtypes.

- **ER-positive breast cancer** showed enrichment of oxidative phosphorylation, the tricarboxylic acid (TCA) cycle, and mitochondrial respiratory pathways, indicating a greater dependence on oxidative metabolism.

- **Triple-Negative Breast Cancer (TNBC)** showed enrichment of immune-related signalling pathways, Fc receptor-mediated immune responses, and Rho GTPase-mediated cytoskeletal remodelling, consistent with its immunogenic and invasive phenotype.

These findings are consistent with published molecular characteristics of ER-positive and TNBC breast cancer.

## Skills Demonstrated

- RNA-seq data analysis using Galaxy Europe
- Quality control and alignment of sequencing data
- Differential gene expression analysis using DESeq2
- Gene annotation and identifier mapping
- Functional enrichment analysis (GO, KEGG, Reactome and WikiPathways)
- Python scripting for bioinformatics automation
- Biological interpretation and scientific data presentation

  ## Repository Structure

```
├── data/
├── results/
├── figures/
├── scripts/
└── README.md
```

## Conclusion

This project demonstrates a complete RNA-seq differential expression analysis workflow, from raw sequencing data to biological interpretation, integrating Galaxy Europe with downstream analysis in Microsoft Excel, Python, and g:Profiler.

