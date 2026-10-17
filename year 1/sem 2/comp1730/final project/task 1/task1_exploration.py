"""
task1_exploration.py

Task 1 - Data exploration of the red wine quality dataset.

Task 1.1  correlation_matrix()  
    - Pearson correlations of the physicochemical properties, 
    drawn as a matplotlib heatmap with dendrograms at the sides,
    saved to task1_heatmap.png
Task 1.2  plot_tsne()           
    - tSNE transform of the data, plotted with colour and labelling 
    that make the quality structure readable, saved to task1_tsne.png
    
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

import winequality

HEATMAP_FILE = "task1_heatmap.png"
TSNE_FILE = "task1_tsne.png"


def correlation_matrix(input):
    """
    Calculate Pearson correlations between all properties and quality.

    Returns the correlation matrix.

    Assumption: every column in the data file is numeric (true for this
    dataset), so all of them go into the correlation.
    """
    # Read with pandas (rather than winequality.load_data())
    # column names survive and can label the heatmap.
    table = pd.read_csv(input, sep=winequality.SEP)
    return table.corr(method="pearson")

def plot_heatmap(correlation_matix, output_file=HEATMAP_FILE):
    """
    Plot correlation matrix as a heatmap with a dendrogram
    on each side and save to output_file

    Assumption: correlation_matix is a square pandas DataFrame with
    matching row/column labels, as returned by correlation_matrix().
    """
    labels = list(correlation_matix.columns)
    correlations = correlation_matix.to_numpy()

    # 1 - |r| turns strongly correlated properties (whether positively or
    # negatively) into near neighbours, which is what should drive the
    # clustering, rather than raw signed correlation.
    distance = squareform(1 - np.abs(correlations), checks=False)
    linkage_matrix = linkage(distance, method="average")
    order = dendrogram(linkage_matrix, no_plot=True)["leaves"]
    ordered_labels = [labels[i] for i in order]
    ordered_correlations = correlations[np.ix_(order, order)]

    figure = plt.figure(figsize=(8, 8))
    grid = figure.add_gridspec(2, 2, width_ratios=(1, 4), height_ratios=(1, 4),
                                wspace=0.02, hspace=0.02)

    top_axes = figure.add_subplot(grid[0, 1])
    dendrogram(linkage_matrix, ax=top_axes)
    top_axes.axis("off")

    left_axes = figure.add_subplot(grid[1, 0])
    dendrogram(linkage_matrix, ax=left_axes, orientation="left")
    left_axes.invert_yaxis()  # leaves then read top-to-bottom, matching the heatmap rows
    left_axes.axis("off")

    heatmap_axes = figure.add_subplot(grid[1, 1])
    image = heatmap_axes.imshow(ordered_correlations, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    heatmap_axes.set_xticks(range(len(ordered_labels)))
    heatmap_axes.set_xticklabels(ordered_labels, rotation=90)
    heatmap_axes.set_yticks(range(len(ordered_labels)))
    heatmap_axes.set_yticklabels(ordered_labels)
    heatmap_axes.yaxis.tick_right()

    figure.colorbar(image, ax=heatmap_axes, fraction=0.046, pad=0.3, label="Pearson r")
    figure.savefig(output_file, bbox_inches="tight")
    plt.close(figure)

def plot_tsne(data_file=winequality.DATA_FILE, perplexity=60,
              output_file=TSNE_FILE):
    """
    Transform the data with tSNE and plot the result.

    perplexity - sklearn.manifold.TSNE parameter; the default is 30, but 60
                  may separate this dataset better

    Saves the plot to output_file.

    Assumption: the last column of data_file is the quality score (per
    winequality.load_data()); it colours the points but is not fed into
    t-SNE as an input feature. perplexity is capped below the sample count,
    since TSNE requires that.
    """
    values = winequality.load_data(data_file)
    properties = values[:, :-1]
    quality = values[:, -1]

    # t-SNE uses distances between points, so properties on larger scales
    # (e.g. total sulfur dioxide) would otherwise dominate ones on smaller
    # scales (e.g. chlorides).
    scaled_properties = StandardScaler().fit_transform(properties)

    valid_perplexity = min(perplexity, len(scaled_properties) - 1)
    tsne = TSNE(n_components=2, perplexity=valid_perplexity, random_state=0)
    embedding = tsne.fit_transform(scaled_properties)

    figure, axes = plt.subplots(figsize=(8, 6))
    points = axes.scatter(embedding[:, 0], embedding[:, 1], c=quality,
                           cmap="viridis", s=15)
    axes.set_xlabel("t-SNE dimension 1")
    axes.set_ylabel("t-SNE dimension 2")
    figure.colorbar(points, ax=axes, label="quality")

    figure.savefig(output_file, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    correlations = correlation_matrix(winequality.DATA_FILE)
    plot_heatmap(correlations)
    plot_tsne()
