# Workflow

This directory contains the complete analysis workflow performed for differential gene expression analysis between ER-positive and Triple-Negative Breast Cancer (TNBC) samples.

The workflow was carried out primarily using Galaxy Europe and includes:

- Quality assessment (Falco, MultiQC)
- Read alignment (HISAT2)
- Gene quantification (featureCounts)
- Differential expression analysis (DESeq2)
- Gene annotation (annotateMyIDs)
- Filtering and merging of annotated differentially expressed genes

The detailed workflow diagram and supporting files are included in this directory.
