"""
task2_theoreticalwine.py

Task 2 - Make a 'perfect' wine.

Required functions:
perfect() - a theoretical wine with as high a predicted quality as
            possible, using the model from winequality.build_model()
awful()   - the converse: the lowest predicted quality possible

Both return (wine, score): wine is a dict of physicochemical properties
keyed for winequality.predict(), score is the predicted quality it gives.

Use winequality.build_model() and winequality.predict() unchanged.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

import winequality

GRID_POINTS = 21   # candidate values tried per feature, per sweep
PASSES = 3         # how many times to sweep through all the features
TSNE_FILE = "task2_tsne.png"


def _search(model, maximise, start_fraction=0.5):
    """
    Greedy coordinate search for an extreme predicted quality score.

    Starts every feature at start_fraction of the way across its range in
    the training file (0 = all at the minimum, 1 = all at the maximum,
    0.5 = the midpoint). Then sweeps through the features one at a time:
    for each, try GRID_POINTS evenly-spaced values across its training
    range and keep whichever gives the best score so far, holding every
    other feature fixed. Repeats this sweep PASSES times.

    maximise - True to search upward for perfect(), False for awful()
    start_fraction - where to start each feature, from 0 to 1

    Returns (wine, score).

    Assumption: candidates are kept within each feature's training-data
    range, since a random forest can't meaningfully extrapolate beyond
    the values it was fitted on.
    """
    # allowed range of each property (its min and max in the training file).
    names = list(model.feature_names_in_)
    data = winequality.load_data(winequality.TRAIN_FILE)
    low = data[:, :len(names)].min(axis=0)
    high = data[:, :len(names)].max(axis=0)

    # starting wine (each property placed between its min and max) and its score.
    wine = {name: float(low[i] + start_fraction * (high[i] - low[i]))
            for i, name in enumerate(names)}
    score = winequality.predict(model, wine)

    # sweep every property PASSES times, trying GRID_POINTS values each
    # with the others held fixed.
    for _ in range(PASSES):
        for i, name in enumerate(names):
            # GRID_POINTS values have GRID_POINTS - 1 gaps between them.
            step = (high[i] - low[i]) / (GRID_POINTS - 1)
            best_value = wine[name]
            for j in range(GRID_POINTS):
                wine[name] = float(low[i] + j * step)
                candidate_score = winequality.predict(model, wine)

                # "Better" means higher for perfect(), lower for awful().
                if maximise:
                    improves = candidate_score > score
                else:
                    improves = candidate_score < score
                if improves:
                    score = candidate_score
                    best_value = wine[name]

            # the loop leaves the property at the last value tried, so reset it to the best.
            wine[name] = best_value

    # return the best wine and its score.
    return wine, score


def _best_of_three_starts(model, maximise):
    """
    Run _search() from three different starting points (all features at
    their minimum, midpoint, and maximum) and keep the best result.

    A greedy coordinate search can only improve on where it starts, so it
    can get stuck at a mediocre score if its single starting point happens
    to sit in a bad spot. Trying three spread-out starts makes that less
    likely, though the result still isn't guaranteed to be the global best.

    Returns (wine, score).
    """
    best_wine, best_score = None, None

    # run the search from each start and keep the best result so far
    # (higher for perfect(), lower for awful()).
    for start_fraction in (0.0, 0.5, 1.0):
        wine, score = _search(model, maximise, start_fraction)
        better = best_score is None or (
            score > best_score if maximise else score < best_score)
        if better:
            best_wine, best_score = wine, score

    return best_wine, best_score


def perfect(model=None):
    """Invent a theoretical wine with a very high predicted quality score.

    model: model from winequality.build_model()

    Returns (wine, score): the physicochemical properties as a dict keyed for
    winequality.predict(), and the quality score it predicts.
    """
    # model=None is optional: build one here if none is passed in
    # (__main__ passes one in, so it is only trained once).
    if model is None:
        model = winequality.build_model()
    # maximise=True looks for the highest predicted quality.
    return _best_of_three_starts(model, maximise=True)


def awful(model=None):
    """Invent a theoretical wine with the worst predicted quality score.

    Returns (wine, score), as perfect() does.
    """
    if model is None:
        model = winequality.build_model()
    # maximise=False looks for the lowest predicted quality.
    return _best_of_three_starts(model, maximise=False)


def plot_theoretical_wines(model, perfect_wine, awful_wine, output_file=TSNE_FILE):
    """
    Mark where perfect_wine and awful_wine fall on a t-SNE plot of the
    real data, the same way task1_exploration.plot_tsne() plots it.

    Assumption: t-SNE has no way to place a new point into an already-fitted
    embedding, so the two theoretical wines are added to the real dataset
    and t-SNE is refit on all of them together. The resulting layout can
    therefore shift slightly from the one saved in task1_tsne.png - this is
    only an approximate view of where they would sit on that plot.

    Saves the plot to output_file.
    """
    # load the real wines.
    values = winequality.load_data(winequality.DATA_FILE)
    properties = values[:, :-1]
    quality = values[:, -1]

    # turn the two invented wines into rows, in the same property order.
    names = list(model.feature_names_in_)
    perfect_row = [perfect_wine[name] for name in names]
    awful_row = [awful_wine[name] for name in names]

    # stack them under the real wines (the last two rows) and standardise together.
    combined = np.vstack([properties, perfect_row, awful_row])
    scaled = StandardScaler().fit_transform(combined)

    # fit t-SNE on all the rows together.
    # init="random" rather than the default "pca": the theoretical wines can
    # be extreme enough on a low-variance feature (e.g. density) to overflow
    # the PCA initialisation step.
    embedding = TSNE(n_components=2, perplexity=60, random_state=0,
                      init="random").fit_transform(scaled)

    # plot the real wines by quality, then perfect (star) and awful (X).
    figure, axes = plt.subplots(figsize=(8, 6))
    points = axes.scatter(embedding[:-2, 0], embedding[:-2, 1], c=quality,
                           cmap="viridis", s=15)
    axes.scatter(*embedding[-2], c="red", marker="*", s=250,
                 edgecolors="black", label="perfect")
    axes.scatter(*embedding[-1], c="black", marker="X", s=150, label="awful")
    axes.set_xlabel("t-SNE dimension 1")
    axes.set_ylabel("t-SNE dimension 2")
    axes.legend()
    figure.colorbar(points, ax=axes, label="quality")

    # save.
    figure.savefig(output_file, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    # build the model once.
    model = winequality.build_model()

    # find the best and worst wines.
    perfect_wine, perfect_score = perfect(model)
    awful_wine, awful_score = awful(model)

    # print them and mark them on the t-SNE plot.
    print("perfect:", perfect_wine, perfect_score)
    print("awful:", awful_wine, awful_score)

    plot_theoretical_wines(model, perfect_wine, awful_wine)