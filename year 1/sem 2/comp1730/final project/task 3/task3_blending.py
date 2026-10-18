"""
task3_blending.py

Task 3 - Improve the quality of a single wine through blending it with one
or more wines from a list of candidates and their physiochemical properties.

Required function:

choose_candidates()

Please choose wines for testing this program from the
winequality_red_260918_TEST.csv file only!

Assumptions:
- Ideal mixing: every physicochemical property is a per-volume quantity
  (a concentration, a volume percentage, or a mass/volume ratio), so
  blending two volumes means taking the volume-weighted average of each
  property. No chemical reaction or volume change on mixing is modelled.
- The estate (primary) wine must stay at least half of the final blend by
  volume (MIN_PRIMARY_FRACTION) - it is never diluted away to nothing.
- Candidates are blended in greedily, one at a time, always keeping
  whichever remaining candidate improves predicted quality the most.
  This is simple and fast, but is not guaranteed to find the single best
  possible combination of candidates and ratios.
"""

import winequality

TEST_FILE = "winequality_red_260918_TEST.csv"

RATIO_STEP = 0.1            # grid search resolution for the blending ratio
MIN_PRIMARY_FRACTION = 0.5  # estate wine must stay at least this much of the blend


def load_pool(model, test_file=TEST_FILE):
    """
    Load every wine in the permitted test file as a list of property dicts.

    model     - a fitted model, as returned by winequality.build_model();
                only used to get the feature names and their order
    test_file - defaults to TEST_FILE; deliberately never set to the full
                dataset or the training file, so the pool this function
                returns can only ever come from the permitted test data

    Returns a list of dicts, one per wine, keyed by the feature names
    winequality.predict() expects (i.e. every column except 'quality').
    """
    # the property names, in the order the model expects
    names = list(model.feature_names_in_)

    # read the TEST file (one row per wine)
    rows = winequality.load_data(test_file)

    # one dict per wine (looping over names leaves quality out)
    pool = []
    for row in rows:
        wine = {}
        for index, name in enumerate(names):
            wine[name] = float(row[index])
        pool.append(wine)
    return pool


def blend_properties(wine_a, wine_b, ratio):
    """
    Blend two wines' physicochemical properties by volume proportion.

    wine_a, wine_b - property dicts with the same keys
    ratio          - fraction of the blend that is wine_a, from 0 to 1
                     (so 1 - ratio is the fraction that is wine_b)

    Assumes ideal mixing: every property here is a per-volume quantity
    (a concentration like g/dm3 or mg/dm3, a volume percentage like
    alcohol, or a mass/volume ratio like density), so blending two
    volumes just means taking the volume-weighted average of each one.
    No chemical reaction or volume change on mixing is modelled.

    Returns a new property dict with the blended values.
    """
    # volume-weighted average of each property, e.g. ratio = 0.7 is 70% wine_a + 30% wine_b.
    blend = {}
    for name in wine_a:
        blend[name] = ratio * wine_a[name] + (1 - ratio) * wine_b[name]
    return blend


def best_ratio_for_pair(model, primary, candidate, step=RATIO_STEP, min_ratio=0.0):
    """
    Find the blending ratio that gives the best predicted quality for one
    candidate wine mixed with the primary wine (or the blend built so far).

    model     - a fitted model, as returned by winequality.build_model()
    primary   - property dict for the estate wine, or the blend so far
    candidate - property dict for the candidate blending wine
    step      - spacing between ratios tried, e.g. 0.1 means ratios 0.1
                apart are tried between min_ratio and 1.0
    min_ratio - the smallest ratio (share of `primary`) allowed. Used by
                choose_candidates() to enforce MIN_PRIMARY_FRACTION, which
                also narrows the search and makes it faster.

    Only one number (the ratio) varies, so a simple grid search is
    already cheap - no need for anything fancier.

    Returns (ratio, blend, score): the best ratio found, the blended
    properties it produces, and its predicted quality.
    """
    # the grid of ratios to try, from min_ratio up to 1.0.
    steps = max(round((1.0 - min_ratio) / step), 0)
    ratios = [min_ratio + i * step for i in range(steps + 1)]
    ratios[-1] = 1.0   # guard against float drift so ratio 1.0 is always tried

    best_ratio = None
    best_blend = None
    best_score = None

    # blend at each ratio, predict the quality, and keep the best.
    for ratio in ratios:
        blend = blend_properties(primary, candidate, ratio)
        score = winequality.predict(model, blend)
        if best_score is None or score > best_score:
            best_ratio = ratio
            best_blend = blend
            best_score = score

    return best_ratio, best_blend, best_score


def choose_candidates(primary, candidates, model):
    """
    Repeatedly blend in whichever remaining candidate improves predicted
    quality the most, until none of them help any more or the estate
    wine's own share of the blend would drop below MIN_PRIMARY_FRACTION.

    primary - physiochemical properties of the wine from your estate
    candidates - list of wines to consider, taken from TEST_FILE
    model - a fitted model, as returned by winequality.build_model()

    Each round calls best_ratio_for_pair() once per remaining candidate
    to see how much it could improve the current blend, and keeps the
    best one found. This greedy approach is simple and fast, but is not
    guaranteed to find the single best possible combination overall.

    Returns a dict describing the winning blend:
        "blend"         - the final blended property dict
        "score"         - the blend's predicted quality
        "candidates"    - candidate wines used, in the order added
        "ratios"        - each used candidate's final share of the blend,
                          parallel to "candidates"
        "primary_ratio" - the estate wine's final share of the blend
    """
    # start from the estate wine. primary_fraction is its share of the
    # current blend, and used / used_fractions record the candidates added.
    current = dict(primary)
    current_score = winequality.predict(model, current)
    primary_fraction = 1.0
    remaining = list(candidates)

    used = []
    used_fractions = []

    # add one candidate per round.
    while remaining:
        # A: smallest ratio of the current blend we can keep, e.g. if the estate
        # wine is 0.8 of the blend we need at least 0.5 / 0.8 = 0.625.
        min_ratio = MIN_PRIMARY_FRACTION / primary_fraction
        if min_ratio >= 1.0 - 1e-9:
            break   # estate wine is already at its 50% floor

        # B: find the candidate (at its best ratio) with the highest predicted quality.
        best_candidate = None
        best_ratio = best_blend = best_score = None
        for candidate in remaining:
            ratio, blend, score = best_ratio_for_pair(
                model, current, candidate, min_ratio=min_ratio)
            if best_score is None or score > best_score:
                best_candidate = candidate
                best_ratio, best_blend, best_score = ratio, blend, score

        # C: stop if it doesn't beat the blend we already have.
        if best_score <= current_score:
            break   # no remaining candidate improves the blend any further

        # D: accept it. earlier shares scale by best_ratio and the new candidate gets 1 - best_ratio.
        primary_fraction *= best_ratio
        used_fractions = [fraction * best_ratio for fraction in used_fractions]
        used.append(best_candidate)
        used_fractions.append(1 - best_ratio)

        current = best_blend
        current_score = best_score
        remaining.remove(best_candidate)

    # return the final blend, its score, the candidates and their shares.
    return {
        "blend": current,
        "score": current_score,
        "candidates": used,
        "ratios": used_fractions,
        "primary_ratio": primary_fraction,
    }


if __name__ == "__main__":
    # build the model once and load the permitted wines.
    model = winequality.build_model()
    pool = load_pool(model)

    # use the first wine in the permitted test file as the estate wine,
    # and every other wine in that same file as a candidate.
    primary = pool[0]
    candidates = pool[1:]

    # predict the estate wine on its own, then find the best blend.
    primary_score = winequality.predict(model, primary)
    result = choose_candidates(primary, candidates, model)

    # print before vs after, the estate share and each candidate's share.
    print("Predicted quality, primary wine alone: %.3f" % primary_score)
    print("Predicted quality, best blend found:   %.3f" % result["score"])
    print()
    print("Estate wine share of final blend: %.2f" % result["primary_ratio"])
    print("Candidates used (in order added):")
    for candidate, ratio in zip(result["candidates"], result["ratios"]):
        print("  share %.2f -> %s" % (ratio, candidate))