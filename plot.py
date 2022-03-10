import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import folium

def plot_score_country(df):
    fig = plt.figure(facecolor=plt.cm.Blues(0.2))
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    df = df.loc[df["DEI score"] > 0]
    dei_country = df.groupby("contact_country").mean().reset_index()
    print(dei_country.sort_values(by = ["DEI score"]))
    print(dei_country.sort_values(by = ["DEI score"]).shape)
    world = world.merge(dei_country, left_on="iso_a3", right_on="contact_country")
    world.plot(column="DEI score", legend=True, legend_kwds={'label': "Average DEI scores per country",
                        'orientation': "horizontal"}, cmap="Greens", edgecolor="black")
    plt.savefig("./plots/world_dei.png", dpi=300)

def plot_score_year(df):
    df = df.loc[df["DEI score"] > 0]
    fig = plt.figure()
    df["year"] = pd.DatetimeIndex(df["date_cleaned"]).year
    df.loc[df.year <= 2015, "2015"] = "Before 2015"
    df.loc[df.year > 2015, "2015"] = "After 2015"
    df.groupby("2015")["DEI score"]\
        .apply(lambda x: sns.kdeplot(x, label=x.name))
    plt.xlabel("Score")
    plt.ylabel("kde")
    plt.savefig("./plots/year.png", dpi=300)


def plot_score_dist(df):
    fig = plt.figure()
    df = df.loc[df["DEI score"] > 0]
    plt.xlim(0, 10)
    sns.distplot(a=df["DEI score"], hist=True, kde=True)
    plt.savefig("./plots/DEI_score_distribution.png", dpi=300)

if __name__ == "__main__":
    df = pd.read_csv("scores_dei.csv", index_col=0)
    print(df.sort_values(by=["DEI score"]))

    subset = df.loc[df["DEI score"] > 0]
    print(subset.shape[0] / df.shape[0] * 100)
    print(subset.describe())

    # plot_score_dist(df)
    # plot_score_year(df)
    plot_score_country(df)
