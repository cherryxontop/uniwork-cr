# Q1

1. first load the red wine CSV with pandas with all 9 physicochemical columns and quality being numeric entries.
2. `correlation_matrix` computes the pearson correlations between every pair of columns.
3. convert correlations to distances (1-|r|); strongly related features, positive or negative sit together
4. then we group similar features with hierarchical clustering using scipy and take the order they fall into on the dendrogram.
5. re-ordering the table into that order so related features sit together.
6. `plot_heatmap` makes. matplotlib grid with a dendogram along the top and left, and the re-ordered table in the middle drawn with imshow on a blue-red scale fixed from -1 to 1.
7. the axes are labeled, a color bar is added and is saved as `task1_heatmap.png`

# Q2

prompts:

1. i need to create a pearson correlation matrix of the wine physicochemical properties and quality. fill in plot_heatmap() in my file. use scipy hierarchical clustering with 1 − |r| as the distance to reorder the features, draw the heatmap with imshow and a diverging colourmap centred on 0, and put a dendrogram on the top and left. this is what i have in mind:
loading and checking the dataset
selecting the numerical physicochemical features and quality column
calculating pearson correlations
grouping similar features using hierarchical clustering
plotting the heatmap, labels, colour scale and dendrograms
saving the figure to the required filename
keep it as short and simple as possible; no features beyond the docstring
- libraries: numpy, pandas, scipy, matplotlib, scikit-learn only
- do not change winequality.py or any function signatures.
- keep the existing docstring and add a one-line note for any assumption.
- descriptive variable names; comments only where the "why" isn't obvious.
after the code, list the assumptions you made and any limitations.

2. i need to complete task 1, which involves exploring the red wine quality dataset. task 1.1 requires a pearson correlation matrix of the physicochemical properties, displayed as a heatmap with dendrograms and saved as task1_heatmap.png. task 1.2 requires a 2d tsne plot that shows the structure of the data using colours and labels to represent wine quality, saved as task1_tsne.png.
review my existing code against these requirements, identify anything missing or incorrect, and fix it while keeping the code simple. briefly explain the changes and how each part meets the requirements.

edits:
- no changes made in code, added/subracted or modified comments and docstrings

# Q3

to build the heatmap i read the wine data with pandas and calculated the Pearson correlation between every pair of columns, so the 9 properties plus quality. if I'd just plotted that table, the features would be in a random order and hard to read, so i used 1 - |r| as a distance (strongly related features count as close, whether the link is positive or negative) and ran hierarchical clustering to group similar ones. i re-ordered the table by that grouping and computed it with dendrograms on the top and left.

the top three correlates of quality are alcohol (about +0.48), volatile acidity (about -0.40) and sulphates (about +0.25). so higher alcohol and sulphates go with better wines, and more volatile acidity goes with worse ones. The most correlated pairs are fixed acidity with density and with citric acid (both about +0.67). the most anti-correlated are volatile acidity with citric acid (about -0.55) and density with alcohol (about -0.5). the most unrelated pair is volatile acidity and residual sugar (about 0) and residual sugar is barely related to quality either.

i don't think the strongly correlated features are really redundant. even at r = 0.67 the pairs share less than half of their variation, so each one still carries its own information. correlation also only picks up straight-line relationships, so a feature that looks unimportant could still matter in a more complicated way.
