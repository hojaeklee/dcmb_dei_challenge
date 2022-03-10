import pandas as pd
import numpy as np
import scipy
import scipy.stats as stats
import math

def race_distribution(df):
    # https://www.npr.org/2021/08/13/1014710483/2020-census-data-us-race-ethnicity-diversity
    us_2020_race_distribution = {
        "white": 0.578,
        "hispanic": 0.187,
        "black": 0.121,
        "asian": 0.059,
        "multiple": 0.041,
        "american indian": 0.0007,
        "other": 0.0005,
        "pacific islander": 0.0002
    }
    us_2020_race_distribution = us_2020_race_distribution.values()
    table = df.pivot_table(index="gse_id", columns=["race"], aggfunc="size", fill_value=0)
    cols = ["white", "hispanic", "black", "asian", "multiple", "other", "pacific islander"]
    table["race_distribution"] = table[cols].values.tolist()
    normalize = lambda x: list(x / np.array(x).sum())
    table["race_distribution"] = table["race_distribution"].map(normalize)
    def normalized_wasserstein(x):
        max_wasserstein = stats.wasserstein_distance([0] * len(us_2020_race_distribution), list(us_2020_race_distribution))
        normalized_wasserstein_dist = stats.wasserstein_distance(x, list(us_2020_race_distribution)) / max_wasserstein
        return normalized_wasserstein_dist
    table["race_dist_score"] = table["race_distribution"].map(normalized_wasserstein)

    return table

def sex_ratio(df):
    table = df.pivot_table(index="gse_id", columns=["sex"], aggfunc="size", fill_value=0)
    table["f/m ratio"] = table["female"] / table["male"]

    standard_lognorm = stats.lognorm(s = 0.5, scale=1)
    table["sex_ratio"] = 1 - 2 * abs(0.5 - standard_lognorm.cdf(table["f/m ratio"]))
    return table

def existence(df, dei_aspect):
    existence = df.groupby("gse_id").apply(lambda x: x.notnull().mean())
    return existence[dei_aspect]

def main():
    df = pd.read_csv("preprocessed_dei.csv")
    score_df = df[["gse_id", "contact_country", "date_cleaned"]].drop_duplicates(subset=["gse_id"])
    score_df.set_index("gse_id", inplace=True)

    sex_existence = existence(df, "sex")
    race_existence = existence(df, "race")
    score_df = pd.merge(score_df, sex_existence, left_index=True, right_index=True)
    score_df = pd.merge(score_df, race_existence, left_index=True, right_index=True)
    sex_ratio_score = sex_ratio(df)
    race_distribution_score = race_distribution(df)
    score_df = score_df.join(sex_ratio_score[["sex_ratio"]])
    score_df = score_df.join(race_distribution_score[["race_dist_score"]])
    score_df = score_df.fillna(0)

    score_df["DEI score"] = 3 * score_df["sex"] + 2 * score_df["sex_ratio"] + \
        4 * score_df["race"] + 1 * score_df["race_dist_score"]

    score_df.to_csv("scores_dei.csv")

if __name__ == "__main__":
    main()