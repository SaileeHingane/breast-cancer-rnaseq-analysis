"""
===========================================================
Gene Annotation Pipeline using MyGene.info API
Author: Sailee Hingane
Project: Breast Cancer RNA-seq Differential Expression Analysis

Description:
------------
Reads the Top20_Positive and Top20_Negative sheets from an
Excel workbook, annotates Gene Symbols using MyGene.info,
adds new annotation columns, and saves a new workbook.

Input:
    D:\RNA_Seq\final_DEGs_dataset.xlsx

Output:
    D:\RNA_Seq\final_DEGs_dataset_annotated.xlsx
===========================================================
"""

import time
import requests
import pandas as pd
from tqdm import tqdm

INPUT_FILE = r"D:\RNA_Seq\final_DEGs_dataset.xlsx"
OUTPUT_FILE = r"D:\RNA_Seq\final_DEGs_dataset_annotated.xlsx"

SHEETS_TO_ANNOTATE = [
    "Top20_Positive",
    "Top20_Negative"
]

API_URL = "https://mygene.info/v3/query"

# --------------------------------------------------------
# Cache to avoid repeated API requests
# --------------------------------------------------------

cache = {}

# --------------------------------------------------------
# Function to query MyGene.info
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

    except Exception:

        return {}

# --------------------------------------------------------
# Read Workbook
# --------------------------------------------------------

print("\nReading workbook...")

excel = pd.ExcelFile(INPUT_FILE)

writer = pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
)

# --------------------------------------------------------
# Process every sheet
# --------------------------------------------------------

for sheet in excel.sheet_names:

    print(f"\nProcessing sheet: {sheet}")

    df = pd.read_excel(INPUT_FILE, sheet_name=sheet)

    if sheet not in SHEETS_TO_ANNOTATE:

        df.to_excel(
            writer,
            sheet_name=sheet,
            index=False
        )

        continue

    if "GeneSymbol" not in df.columns:

        print("GeneSymbol column not found.")

        df.to_excel(
            writer,
            sheet_name=sheet,
            index=False
        )

        continue

    annotations = []

    for gene in tqdm(df["GeneSymbol"]):

        annotations.append(
            annotate_gene(gene)
        )

    annotation_df = pd.DataFrame(annotations)

    df = pd.concat(
        [df, annotation_df],
        axis=1
    )

    df.to_excel(
        writer,
        sheet_name=sheet,
        index=False
    )

writer.close()

print("\n====================================")
print("Annotation completed successfully.")
print(f"Output saved to:\n{OUTPUT_FILE}")
print("====================================")