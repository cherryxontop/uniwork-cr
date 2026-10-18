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

# logic flow:
#   1. correlation_matrix() reads the csv and returns a table of correlations
#   2. plot_heatmap() groups similar properties together using clustering,
#      then draws that table as a heatmap with a dendrogram on the top and left
#   3. plot_tsne() squashes the 9 properties down to 2 numbers
#      per wine and plots each wine as a dot coloured by its quality


def correlation_matrix(input):
    """
    Calculate Pearson correlations between all properties and quality.

    Returns the correlation matrix.

    Assumption: every column in the data file is numeric (true for this
    dataset), so all of them go into the correlation.
    """
    # read the csv with pandas so the column
    # names survive and can label the heatmap
    table = pd.read_csv(input, sep=winequality.SEP)

    # pairwise Pearson correlations, giving a 10 x 10 matrix
    return table.corr(method="pearson")
 
def plot_heatmap(correlation_matix, output_file=HEATMAP_FILE):
    """
    Plot correlation matrix as a heatmap with a dendrogram
    on each side and save to output_file
 
    Assumption: correlation_matix is a square pandas DataFrame with
    matching row/column labels, as returned by correlation_matrix().
    """
    # keep the labels and the raw values
    labels = list(correlation_matix.columns)
    correlations = correlation_matix.to_numpy()
 
    # order the properties with hierarchical clustering.
    # 1 - |r| turns strongly correlated properties (whether positively or
    # negatively) into near neighbours- basis of clustering
    # squareform gives linkage the flat array of unique pairs it needs, and
    # no_plot=True just returns the leaf order without drawing.
    distance = squareform(1 - np.abs(correlations), checks=False)
    linkage_matrix = linkage(distance, method="average")
    order = dendrogram(linkage_matrix, no_plot=True)["leaves"]
 
    # re-order the labels and matrix (np.ix_ re-orders rows and columns together)
    ordered_labels = [labels[i] for i in order]
    ordered_correlations = correlations[np.ix_(order, order)]
 
    # 2 x 2 grid with dendrograms on the top and left and the heatmap bottom-right
    figure = plt.figure(figsize=(8, 8))
    grid = figure.add_gridspec(2, 2, width_ratios=(1, 4), height_ratios=(1, 4),
                                wspace=0.02, hspace=0.02)
 
    # dendrograms: the same linkage, once for columns and once for rows
    top_axes = figure.add_subplot(grid[0, 1])
    dendrogram(linkage_matrix, ax=top_axes)
    top_axes.axis("off")
 
    left_axes = figure.add_subplot(grid[1, 0])
    dendrogram(linkage_matrix, ax=left_axes, orientation="left")
    left_axes.invert_yaxis()  # leaves then read top-to-bottom, matching the heatmap rows
    left_axes.axis("off")
 
    # draw the heatmap. The colour range is fixed to [-1, 1] (0 = white),
    # and aspect="auto" keeps the rows aligned with the left dendrogram.
    heatmap_axes = figure.add_subplot(grid[1, 1])
    image = heatmap_axes.imshow(ordered_correlations, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
 
    # add the labels and colour bar, then save.
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
    # split into properties (all but the last column) and quality (the last).
    values = winequality.load_data(data_file)
    properties = values[:, :-1]
    quality = values[:, -1]
 
    # standardise the properties.
    # t-SNE uses distances between points, so properties on larger scales
    # (e.g. total sulfur dioxide) would otherwise dominate ones on smaller
    # scales (e.g. chlorides).
    scaled_properties = StandardScaler().fit_transform(properties)
 
    # fit t-SNE to 2D (random_state=0 makes the result repeatable).
    valid_perplexity = min(perplexity, len(scaled_properties) - 1)
    tsne = TSNE(n_components=2, perplexity=valid_perplexity, random_state=0)
    embedding = tsne.fit_transform(scaled_properties)
 
    # plot, coloured by quality (quality is not an input to t-SNE).
    figure, axes = plt.subplots(figsize=(8, 6))
    points = axes.scatter(embedding[:, 0], embedding[:, 1], c=quality,
                           cmap="viridis", s=15)
    axes.set_xlabel("t-SNE dimension 1")
    axes.set_ylabel("t-SNE dimension 2")
    figure.colorbar(points, ax=axes, label="quality")
 
    # save.
    figure.savefig(output_file, bbox_inches="tight")
    plt.close(figure)
 
 
if __name__ == "__main__":
    # correlations -> heatmap -> t-SNE plot.
    correlations = correlation_matrix(winequality.DATA_FILE)
    plot_heatmap(correlations)
    plot_tsne()