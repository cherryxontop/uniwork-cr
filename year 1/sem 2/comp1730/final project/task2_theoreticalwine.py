"""
task2_theoreticalwine.py

Task 2 - Make a 'perfect' wine.

Invents theoretical wines at the extremes of the quality model:

Implements two required functions (but your solution may have
as many others as are necessary):
perfect()
    - a theoretical wine with as high a predicted quality as
    can be reached with the input model provided
awful()
    -  the converse: the worst predicted quality possible with the
    input model provided

Use both use winequality.build_model() and winequality.predict()
without changes.  Although additional helper functions may be
added to the winequality module.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

import winequality

GRID_POINTS = 21   # candidate values tried per feature on each sweep
PASSES = 3         # how many times to sweep through all the features
TSNE_FILE = "task2_tsne.png"


def _feature_bounds(model):
    """
    Smallest and largest value of each feature seen in the training file.

    Used to keep search candidates within a physically plausible range,
    since the forest can't meaningfully extrapolate beyond what it was
    trained on.

    Returns (names, low, high): names in model's feature order, and dicts
    of low/high bounds keyed by the same names.
    """
    names = list(model.feature_names_in_)
    data = winequality.load_data(winequality.TRAIN_FILE)

    low = {}
    high = {}
    for index, name in enumerate(names):
        column = data[:, index]
        low[name] = float(column.min())
        high[name] = float(column.max())
    return names, low, high


def _candidate_values(name, low, high):
    """GRID_POINTS values evenly spaced across name's training range."""
    lo = low[name]
    hi = high[name]
    step = (hi - lo) / (GRID_POINTS - 1)
    return [lo + i * step for i in range(GRID_POINTS)]


def _search(model, maximise):
    """
    Greedy coordinate search for an extreme predicted quality score.

    Starts from the mid-point of every feature's training range, then
    repeatedly sweeps through the features one at a time: for each, try
    every candidate value from _candidate_values() and keep whichever
    gives the best score so far, holding all other features fixed. Stops
    once a full sweep makes no further improvement, or after PASSES
    sweeps, whichever comes first.

    maximise - True to search upward for perfect(), False to search
               downward for awful()

    Returns (wine, score).
    """
    names, low, high = _feature_bounds(model)

    wine = {}
    for name in names:
        wine[name] = (low[name] + high[name]) / 2
    score = winequality.predict(model, wine)

    for _ in range(PASSES):
        improved = False
        for name in names:
            best_value = wine[name]
            best_score = score
            for value in _candidate_values(name, low, high):
                wine[name] = value
                candidate_score = winequality.predict(model, wine)
                if maximise:
                    better = candidate_score > best_score
                else:
                    better = candidate_score < best_score
                if better:
                    best_score = candidate_score
                    best_value = value
            wine[name] = best_value
            if best_score != score:
                improved = True
            score = best_score
        if not improved:
            break

    return wine, score


def perfect(model=None):
    """Invent a theoretical wine with a very high predicted quality score.

    model: model from winequality.build_model()

    Returns (wine, score): the physicochemical properties as a dict keyed for
    winequality.predict(), and the quality score it predicts.
    """
    if model is None:
        model = winequality.build_model()
    return _search(model, maximise=True)


def awful(model=None):
    """Invent a theoretical wine with the worst predicted quality score.

    Returns (wine, score), as perfect() does.
    """
    if model is None:
        model = winequality.build_model()
    return _search(model, maximise=False)


def plot_theoretical_wines(model, perfect_wine, awful_wine, output_file=TSNE_FILE):
    """
    Mark where perfect_wine and awful_wine fall on a t-SNE plot of the
    real data, the same way task1_exploration.plot_tsne() plots it.

    t-SNE has no way to place a new point into an already-fitted embedding,
    so the two theoretical wines are added to the real dataset and t-SNE is
    refit on all of them together. The resulting layout can therefore shift
    slightly from the one saved in task1_tsne.png - this is only an
    approximate view of where they would sit on that plot.

    Saves the plot to output_file.
    """
    values = winequality.load_data(winequality.DATA_FILE)
    properties = values[:, :-1]
    quality = values[:, -1]

    names = list(model.feature_names_in_)
    perfect_row = [perfect_wine[name] for name in names]
    awful_row = [awful_wine[name] for name in names]
    combined_properties = np.vstack([properties, perfect_row, awful_row])

    scaled_properties = StandardScaler().fit_transform(combined_properties)
    perplexity = min(60, len(scaled_properties) - 1)
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=0)
    embedding = tsne.fit_transform(scaled_properties)

    real_embedding = embedding[:-2]
    perfect_point = embedding[-2]
    awful_point = embedding[-1]

    figure, axes = plt.subplots(figsize=(8, 6))
    points = axes.scatter(real_embedding[:, 0], real_embedding[:, 1], c=quality,
                           cmap="viridis", s=15)
    axes.scatter(*perfect_point, c="red", marker="*", s=250,
                 edgecolors="black", label="perfect")
    axes.scatter(*awful_point, c="black", marker="X", s=150, label="awful")
    axes.set_xlabel("t-SNE dimension 1")
    axes.set_ylabel("t-SNE dimension 2")
    axes.legend()
    figure.colorbar(points, ax=axes, label="quality")

    figure.savefig(output_file, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    model = winequality.build_model()
    perfect_wine, perfect_score = perfect(model)
    awful_wine, awful_score = awful(model)

    print("perfect:", perfect_wine, perfect_score)
    print("awful:", awful_wine, awful_score)

    plot_theoretical_wines(model, perfect_wine, awful_wine)
