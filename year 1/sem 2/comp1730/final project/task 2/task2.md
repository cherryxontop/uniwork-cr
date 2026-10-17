# Q1

1. call winequality.build_model() once and pass it to everything, so it's only trained once.
2. for each of the 9 properties, find its lowest and highest value in the training file, so invented wines stay in the range the model has seen.
3. give a dict of the 9 values to winequality.predict() and get back a predicted quality.
4. trying every combination is impossible (21 values for each of 9 properties), so use a greedy search. Take one property at a time, try 21 evenly spaced values with the others fixed, keep the best, and sweep through all properties 3 times.
5. run the search from three starting wines (all minimums, midpoints, all maximums) and keep the best.
6. perfect() and awful() share one search, flipped between highest and lowest score, and return (wine, score).
7. add the two wines to the real data, refit tSNE (it can't place new points), and mark them on the plot.

# Q2

GIMME MY PROMPTS BACK HELLO


# Q3

for perfect() I treated the wine as 9 numbers (the properties) and asked the model's predict() what score each combination would get, searching for the combination with the highest score. trying every combination is impossible, so i used a greedy search: take one property at a time, try 21 evenly spaced values between the lowest and highest seen in the training file while holding the others fixed, keep the best and repeat across all properties three times.

the first version started every property at its midpoint and only reached about 7.09. the problem is that the search changes one property at a time, so it can get stuck where no single change helps even though a better wine exists that needs several properties to change together. Starting from three places (all minimums, midpoints, all maximums) and keeping the best fixed it, and the maximum predicted quality I reached was about 7.63. it can't get close to 10 because the model only learned from wines scored between 3 and 8, and a random forest predicts averages of what it has seen.

awful() is the same search flipped to look for the lowest score, and it got down to about 3.61, which is close to the lowest quality in the training data.

on my tSNE plot the awful wine lands at the lower right, among the darker, lower quality wines. The perfect wine ends up near the upper right edge among mid quality wines, not inside the high quality area. I think that's because the perfect wine is an extreme mix of settings that may not resemble any real wine, and because tSNE can't place new points, so I had to refit it with the two wines included, which changes the layout a bit compared with Task 1.

The "perfect" wine is only perfect according to this model, not to real tasters, and combining extreme values of every property may give a wine that couldn't actually be made. The search also isn't guaranteed to find the true best wine, since a different search might find a higher score.