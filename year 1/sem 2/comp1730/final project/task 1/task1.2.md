# Q1

1. first, read the data with winequality.load_data() and split the 9 properties from the quality column.
2. scale the properties with StandardScaler so big-valued ones like total sulfur dioxide don't swamp small ones like chlorides.
3. run sklearn's TSNE to squash the 9 properties down to 2 dimensions, trying different perplexity values and keeping the one that shows the structure best (60).
4. plot_tsne() draws one dot per wine on a matplotlib scatter, coloured by quality (quality isn't fed into tSNE), with axis labels and a colour bar.
5. save as task1_tsne.png.

# Q2

prompts:

1. (continuing task 1.1 prompts) "now a function named plot_tsne() that transforms the physicochemical features of the red wine dataset using scikit-learn's TSNE and saves a plot as task1_tsne.png. implement the function using the supplied scaffold and dataset. alter the 'perplexity' parameter when instantiating the sklearn.manifold.TSNE class as required."

2. (review of the whole task): "i need to complete task 1, which involves exploring the red wine quality dataset. task 1.1 requires a pearson correlation matrix... task 1.2 requires a 2d tsne plot that shows the structure of the data using colours and labels to represent wine quality, saved as task1_tsne.png. review my existing code against these requirements, identify anything missing or incorrect, and fix it while keeping the code simple. briefly explain the changes and how each part meets the requirements."

edits:

no major code changes. doctrings and comments were tweaked a bit.

# Q3

for the tSNE plot i took the 9 physicochemical properties and scaled them first. tSNE works on distances between wines, so without scaling a property with big numbers like total sulfur dioxide would overpower tiny numbers like chlorides. then i used scikit-learn's TSNE to squash the 9 dimensions down to 2 so that similar wines end up close together, and coloured each wine by its quality score. quality isn't an input to tSNE, only the colour, so any pattern in the colours comes from the chemistry alone.

perplexity makes a big difference, so i tried a few values. turns out it's roughly how many neighbours each wine pays attention to. at a low value like 5 the plot broke into lots of tiny clumps with no clear pattern, and at higher values the clumps merged into broader regions. at 60 the low quality wines sat mostly on one side and the high quality wines on the other, so i used 60. at much higher values the plot got blurrier.

the groups still overlap a lot, with a big mixed middle, so the properties tell us something about quality but not enough to separate the wines cleanly. that fits the correlations from the heatmap, where no single property was strongly linked to quality (alcohol was the highest at about 0.48).

i wouldn't read too much into the exact shapes. the layout changes with perplexity and the random seed, and the distances between groups on a tSNE plot aren't meaningful. quality is also a subjective score from tasters, so some of the overlap could be down to that.