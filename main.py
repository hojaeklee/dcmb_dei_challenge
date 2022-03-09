from entrez import entrez as ez
import GEOparse
import pandas as pd
import tqdm
import time
from pathlib import Path

def get_characteristic(gsm, dei_aspect):
    for key, value in gsm.metadata.items():
        if key.startswith("characteristic"):
            for entry in value:
                if dei_aspect in entry.lower():
                    dei_value = entry.split(": ")[1]
                    return dei_value.lower()

def analyze_dei(geo_accession_numbers):
    # Analyzing a Series
    dei_path = Path("./dei.csv")
    dei_aspects = ["sex", "race", "ethnicity", "age"]

    for gsm_id in tqdm.tqdm(geo_accession_numbers):
        if dei_path.is_file():
            dei_df = pd.read_csv(dei_path)
        else:
            dei_df= pd.DataFrame()

        # When reanalyzing, skip the ones that are already in dei_df dataframe
        gsm_id = gsm_id.strip("\n")
        if gsm_id in dei_df["gse_id"].tolist():
            continue

        try:
            gse = GEOparse.get_GEO(geo=gsm_id, destdir=f"./data", silent=True)
        except:
            print(f"{gsm_id} is not a valid GEO Accession number.")
            continue

        # Analyzing Samples within Series
        for gsm_name, gsm in gse.gsms.items():
            results_dict = {}
            results_dict["gse_id"] = gse.name
            results_dict["gsm_id"] = gsm_name
            results_dict["contact_country"] = gsm.metadata["contact_country"]
            if results_dict["contact_country"] == "USA":
                results_dict["contact_state"] = gsm.metadata["contact_state"]
            results_dict["submission_date"] = gsm.metadata["submission_date"]
            for dei_aspect in dei_aspects:
                results_dict[dei_aspect] = get_characteristic(gsm, dei_aspect=dei_aspect)
            dei_df = pd.concat([dei_df, pd.DataFrame([results_dict])])

        dei_df.to_csv("dei.csv", index=False)

def _get_geo_accession_numbers(query):
    elems = ez.eselect(tool="search", db="gds", term=query)
    num_samples = int(elems["Count"])
    print(f"There are {num_samples} samples...")

    # For loops through chunks:
    chunk_size = 10 # 10 queries per second with valid NCBI API key
    for i in tqdm.tqdm(range(0, num_samples, chunk_size)):
        records = ez.equery(tool="summary", db="gds", WebEnv=elems['WebEnv'], query_key=elems['QueryKey'], retstart=i, retmax=chunk_size)

        # Collect Accession Number
        for line in records:
            if line.strip().startswith('<Item Name="Accession" Type="String">GSE'):
                accession_id = line.split('>')[1].split('<')[0]
                with open('./geo_accession_numbers.txt', 'a') as f:
                    f.write(f"{accession_id}\n")

        time.sleep(1)

def get_geo_accession_numbers(query):
    accession_numbers = []
    try:
        with open("./geo_accession_numbers.txt") as f:
            print("File exists...")
            accession_numbers = f.readlines()
    except IOError:
        accession_numbers = _get_geo_accession_numbers(query)

    return accession_numbers

def main():
    # Get GEO Accession Numbers
    query = '"homo sapeins"[Organism] AND ("gse"[Filter] AND "Expression profiling by array"[Filter] AND ("100"[n_samples] : "100000000"[n_samples]))'
    geo_accession_numbers = get_geo_accession_numbers(query)
    analyze_dei(geo_accession_numbers)

if __name__ == "__main__":
    main()
