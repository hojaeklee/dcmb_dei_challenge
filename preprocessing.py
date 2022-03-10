import pandas as pd
import numpy as np
from pycountry import countries
import ast
from datetime import datetime

def preprocess_sex(df):
    df["sex"].replace(
        dict.fromkeys(["m", "boys", "male"], "male"),
        regex=True,
        inplace=True
    )
    df["sex"].replace(
        dict.fromkeys(["f", "girls", "female"], "female"),
        regex=True,
        inplace=True
    )
    f = lambda x: np.nan if x not in ["male", "female"] else x
    df["sex"] = df["sex"].map(f)
    return df

def preprocess_country(df):
    """Convert country to Alpha 3 Codes for World Map visualization"""
    string2list2string = lambda x: ast.literal_eval(x)[0]
    df["contact_country"] = df["contact_country"].map(string2list2string)

    def name2alpha3(name):
        if name == "USA":
            return "USA"
        if name == "Taiwan":
            return "TWN"
        if name == "South Korea":
            return "KOR"
        if name == "Russia":
            return "RUS"
        try:
            return countries.get(name=name).alpha_3
        except:
            return countries.search_fuzzy(name)[0].alpha_3

    df["contact_country"] = df["contact_country"].map(name2alpha3)
    return df

def preprocess_date(df):
    list2str = lambda x: ast.literal_eval(x)[0]
    df["date_cleaned"] = df["submission_date"].map(list2str)
    str2date = lambda x: datetime.strptime(x, "%b %d %Y")
    df["date_cleaned"] = df["date_cleaned"].map(str2date)
    return df

def preprocess_race(df):
    races = ["white", "hispanic", "black", "asian", "multiple races", "american indian", "pacific islander"]
    # na is unclear whether north american or not available; aa is unclear african american or asian american
    def f(x):
        if not pd.isna(x):
            try:
                if "white" in x or x in ["caucasian", "europeanamerican", "europe", "cau", "cauc", "w"]:
                    return "white"
                elif x in ["hispanic", "hisp", "latino"]:
                    return "hispanic"
                elif "black" in x or x in ["african american", "africanamerican", "african-american", "afr_amer", "b"]:
                    return "black"
                elif "asia" in x or x in ["asian", "ea", "a"]:
                    return "asian"
                elif x in ["american indian or alaska native", "native american", "amer_ind_ak_native"]:
                    return "american indian"
                elif "pacific islander" in x or x in ["native_hw_pac_islkand", "native hawiian or other "]:
                    return "pacific islander"
                elif "multiple" in x or "mixed" in x or x in ["biracial", "two_or_more_races"]:
                    return "multiple"
                elif "other" in x:
                    return "other"
            except:
                return np.nan

    df["race"] = df["race"].map(f)
    return df

def main():
    df = pd.read_csv("raw_dei.csv")
    print(df.shape)
    df = preprocess_country(df)
    print("Countries preprocessed")
    df = preprocess_date(df)
    print("Date preprocessed")
    df = preprocess_sex(df)
    print("Sex preprocessed")
    df = preprocess_race(df)
    print("Race preprocessed")
    df.to_csv("preprocessed_dei.csv", index=False)
    print("Saved")

if __name__ == "__main__":
    main()