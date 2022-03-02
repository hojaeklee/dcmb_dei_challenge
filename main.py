from entrez import entrez as ez
import GEOparse
import logging
import pprint
logging.basicConfig(filename="main.log", level=logging.INFO)

# GEO is in Entrez GEO DataSets (db=gds)
def main():
    """
    Idea:
    1. Get list of GSEs to for-loop

    2. For each gse, for loop through `gse.gsms.items()`
    3. For each gsm, for loop through key-value pairs in `gsm.metadata`
    4. Read gsm.column data
    """
    gse = GEOparse.get_GEO(geo="GSE1563", destdir="./", silent=True)

    logging.info("GSM example:")
    for gsm_name, gsm in gse.gsms.items():
        logging.info(f"Name: {gsm_name}")
        logging.info("Metadata:")
        for key, value in gsm.metadata.items():
            """
            gsm.metadata["description"]
            ['Clinical status: con...lood donor', 'Age: unknown', 'Sex: unknown', 'Immunosupression: none', 'Histopathology: none', 'Donor type: NA', 'Scr (mg/dL): unknown', 'Days post transplant: NA', 'Abbreviations used i...osclerosis', 'Keywords = DNA micro...transplant']
            """
            logging.info(f" - {key} : {', '.join(value)}")
        logging.info("Table data: ")
        logging.info(gsm.table.head())
        logging.info(gsm.columns.head())

# query = ((human[Organism]) AND "expression profiling by high throughput sequencing"[DataSet Type])
# Use the qualifier fields in Entrez GEO DataSets to fine-tune a search
# Construct the appropriate eSearch query in your script/program
# Run the query, retrieve the results in the form of UIDs or history parameters (query_key and WebEnv) as needed
# Run eSummary or eFetch and/or eLink depending on your needs to retrieve the final metadata or accessions.
# If you need to download full records or supplVementary files, use the accession information to construct an FTP URL and download the data.
def sample_query():
    query = '((human[Organism]) AND "expression profiling by high throughput sequencing"[DataSet Type])'
    entrez_record_uids = []
    for line in ez.equery(tool="search", db="gds", term=query, usehistory="y"):
        if line.strip().startswith('<Id>'):  # like:  <Id>6714</Id>
            entrez_record_uids.append(line.split('>')[1].split('<')[0])
    pprint.pprint(entrez_record_uids)
    return entrez_record_uids

if __name__ == "__main__":
    # main()
    """
    uids = sample_query()
    elems = ez.eselect(tool="post", db="gds", id=uids)
    test = ez.eapply(tool="summary", db="gds", elems=elems)
    for i, line in enumerate(test):
        print(line)
    """

    query = '((human[Organism]) AND "expression profiling by high throughput sequencing"[DataSet Type])'
    elems = ez.eselect(tool="search", db="gds", term=query)
    num_samples = int(elems["Count"])

    accession_ids = []
    # For loops through chunks:
    chunk_size = 10
    for i in range(0, num_samples, chunk_size):
        records = ez.equery(tool="summary", db="gds", WebEnv=elems['WebEnv'], query_key=elems['QueryKey'], retstart=i, retmax=chunk_size)

        # Collect Accession Number
        for line in records:
            if line.strip().startswith('<Item Name="Accession" Type="String">'):
                accession_id = line.split('>')[1].split('<')[0]
                accession_ids.append(accession_id)
                break
        break
    # elems = ez.eselect(tool="link", dbfrom="gds", db="gds", id=uids)
    print(accession_ids)
