# Q1

1. call winequality.build_model() once and pass it on, so it's only trained once.
2. find each property's min and max in the training file, so invented wines stay within the model's range.
3. pass a dict of the 9 values to winequality.predict() for a predicted quality.
4. trying every combination is impossible (21 values for 9 properties), so use a greedy search: for each property in turn, try 21 evenly spaced values with the others fixed, keep the best, and sweep all properties 3 times.
5. run the search from three starting wines (all minimums, midpoints, all maximums) and keep the best.
6. perfect() and awful() share one search (highest vs lowest) and return (wine, score).
7. add the two wines to the real data, refit tSNE (it can't place new points) and mark them.

# Q2

1. implement perfect() and awful() with build_model() and predict() as-is. Before coding, explain the model, feature names, a simple search design, how to compare candidates and report results, and how to find the wines on the t-SNE plot, with limitations.
2. redo the searches and check for credibility of the results
3. remove the out-of-scope checks (_tree_spread, _nearest_real_wine, _report, start_spread, extra printing); keep only perfect(), awful(), the max score and tSNE placement.
4. review my code against the requirements, fix bugs, keep it simple, explain the search and testing, check the tsne plot.
5. improve and shorten it in the same style, keeping only what the task asks, simple enough to explain in a viva; keep comments and docstrings.
6. it dropped the three starting wines: add back _search(start_fraction) and _best_of_three_starts (0, 0.5, 1), noting it isn't guaranteed global; perfect()/awful() call it; keep the rest and report the scores.

# Q3

for perfect() i treated the wine as 9 numbers and used the model's predict() to score each combination, searching for the highest. trying every combination is impossible, so i used a greedy search: take one property at a time, try 21 evenly spaced values between the lowest and highest seen in the training file while holding the others fixed, keep the best, and repeat over all properties three times.

the first version started every property at its midpoint and only reached about 7.09. the search changes one property at a time, so it can get stuck where no single change helps even though a better wine exists that needs several properties to change together. starting from three places (all minimums, midpoints, all maximums) and keeping the best fixed it, and the maximum predicted quality i reached was about 7.63. it can't get close to 10 because the model only learned from wines scored 3 to 8 and a random forest predicts averages. awful() is the same search flipped to find the lowest score, about 3.61, close to the lowest training score (3).

on my tSNE plot the awful wine lands at the lower right, among the darker, lower quality wines. the perfect wine ends up near the upper right edge among mid quality wines, not inside the high quality area. probably because it is an extreme mix of settings that may not resemble any real wine, and because tSNE can't place new points, so i refit it with the two wines included, shifting the layout from Task 1.