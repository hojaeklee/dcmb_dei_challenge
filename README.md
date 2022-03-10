# 2020 DCMB DEI Challenge

To reproduce results from the report, please run the following scripts in order:

```
python dataset.py
python preprocessing.py
python score.py
```

### Instructions

Investigate if Gene Expression Omnibus datasets are biased relative to the US population using DEI criteria (sex,  ethnicity, ancestry)

Participants to this challenge will process metadata from Gene Expression Omnibus datasets that are publicly available https://www.ncbi.nlm.nih.gov/geo/

You will select datasets that meet the following criteria:
The type of experiment is: expression profiling by array AND
The organism they study is: homo sapiens AND
They have at least 100 samples
There should be 2500-2600 datasets.

Search details look like this:
"homo sapeins"[Organism] AND ("gse"[Filter] AND "Expression profiling by array"[Filter] AND ("100"[n_samples] : "100000000"[n_samples]))
This search retrieves 2563 series.
https://www.ncbi.nlm.nih.gov/gds
Use the advanced search to set the criteria.
You can make the criteria more stringent and select US datasets.

You can use any approach to retrieve and process that metadata existing software like the R package GEOquery to retrieve the metadata https://www.bioconductor.org/packages/release/bioc/html/GEOquery.html

Start with one dataset and then expand to the rest in small increments to make sure all works well. Analyze as many datasets as possible from the selected ones. Please submit a report even if you did not analyze all of them.

A simple approach:
Count how many female and male samples there are and make the ratio, a ratio > 1 is a good ratio, a ratio close to 0 is not a good ratio.

Make sure this works then you can add more criteria or add complexity to computing a score.

Rank the datasets from the most biased to the least biased and discuss the results.

If you want to go further, you can look at datasets before and after 2015. This threshold renders a similar number of datasets with the above criteria.
Compare the DEI bias scores for datasets before and after 2015, do they increase.
Look at the distribution.
