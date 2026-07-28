"""
===========================================================
Gene Functional Annotation using MyGene.info API
Author: Sailee Hingane
Project: Breast Cancer RNA-seq Differential Expression Analysis

Description:
------------


Input:
    final_DEGs_dataset.xlsx   

Output:
    top_genes_functional_annotation.xlsx   
===========================================================
"""

import time
import requests
import pandas as pd
from tqdm import tqdm

# --------------------------------------------------------
# Configuration
# --------------------------------------------------------

INPUT_FILE = "final_DEGs_dataset.xlsx"

# Separate output file -- the input file above is never written to.
OUTPUT_FILE = "top_genes_functional_annotation.xlsx"

# Sheet names to read from the input and annotate.
# Update this list if you rename to Top30_Positive / Top30_Negative,
# or add more sheet names -- the script just annotates whichever
# rows are present in each sheet.
SHEETS_TO_ANNOTATE = [
    "Top20_Positive",
    "Top20_Negative"
]

GENE_ID_COLUMN = "GeneSymbol"

API_URL = "https://mygene.info/v3/query"

# --------------------------------------------------------
# Cache to avoid repeated API requests for the same gene
# --------------------------------------------------------

cache = {}


# --------------------------------------------------------
# Function to query MyGene.info for a single gene symbol
# --------------------------------------------------------

def annotate_gene(symbol):

    if pd.isna(symbol):
        return {}

    symbol = str(symbol).strip()

    if symbol in cache:
        return cache[symbol]

    params = {
        "q": symbol,
        "species": "human",
        "size": 1,
        "fields":
            "summary,"
            "entrezgene,"
            "ensembl.gene,"
            "go.BP.term,"
            "go.MF.term,"
            "go.CC.term"
    }

    try:

        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()

        if "hits" not in data or len(data["hits"]) == 0:
            cache[symbol] = {}
            return {}

        hit = data["hits"][0]

        def extract_go(go_field):

            if go_field is None:
                return ""

            if isinstance(go_field, list):
                return "; ".join(
                    x.get("term", "")
                    for x in go_field
                    if isinstance(x, dict)
                )

            if isinstance(go_field, dict):
                return go_field.get("term", "")

            return ""

        annotation = {

            "Gene_Summary":
                hit.get("summary", ""),

            "Entrez_ID":
                hit.get("entrezgene", ""),

            "Ensembl_ID":
                hit.get("ensembl", {}).get("gene", "")
                if isinstance(hit.get("ensembl"), dict)
                else "",

            "GO_Biological_Process":
                extract_go(
                    hit.get("go", {}).get("BP")
                    if isinstance(hit.get("go"), dict)
                    else None
                ),

            "GO_Molecular_Function":
                extract_go(
                    hit.get("go", {}).get("MF")
                    if isinstance(hit.get("go"), dict)
                    else None
                ),

            "GO_Cellular_Component":
                extract_go(
                    hit.get("go", {}).get("CC")
                    if isinstance(hit.get("go"), dict)
                    else None
                )
        }

        cache[symbol] = annotation

        time.sleep(0.25)

        return annotation

    except Exception as e:

        print(f"  Warning: lookup failed for '{symbol}' ({e})")
        return {}


# --------------------------------------------------------
# Read only the target sheets from the input workbook
# --------------------------------------------------------

print(f"\nReading '{INPUT_FILE}' (read-only, will not be modified)...")

excel = pd.ExcelFile(INPUT_FILE)

writer = pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
)

for sheet in SHEETS_TO_ANNOTATE:

    if sheet not in excel.sheet_names:
        print(f"\nSheet '{sheet}' not found in {INPUT_FILE} -- skipping.")
        continue

    print(f"\nProcessing sheet: {sheet}")

    df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

    if GENE_ID_COLUMN not in df.columns:
        print(f"  '{GENE_ID_COLUMN}' column not found -- skipping.")
        continue

    annotations = []

    for gene in tqdm(df[GENE_ID_COLUMN]):

        annotations.append(
            annotate_gene(gene)
        )

    annotation_df = pd.DataFrame(annotations).reset_index(drop=True)
    df = df.reset_index(drop=True)

    out_df = pd.concat(
        [df, annotation_df],
        axis=1
    )

    out_df.to_excel(
        writer,
        sheet_name=sheet,
        index=False
    )

    n_missing = annotation_df["Gene_Summary"].isna().sum() if "Gene_Summary" in annotation_df.columns else 0
    print(f"  {len(df) - n_missing} of {len(df)} genes annotated successfully.")

writer.close()

print("\n====================================")
print("Annotation completed successfully.")
print(f"Input file (untouched):  {INPUT_FILE}")
print(f"New annotated output:    {OUTPUT_FILE}")
print("====================================")
