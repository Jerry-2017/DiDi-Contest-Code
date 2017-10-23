# DiDi-Contest-Code
In the DiDi Machine learning contest 2016, we use MDS , Random Forest Regression Tree , and time expansion to achieve top 50 out of 1000 teams

## Details

The details of competition could be found in #Chinese Language# 2016_06_Week3_Report.pdf

## Methods 

> Final Rank: 33 out of 775 (50 threshold) 0.253671 (0.245202 best)

1.Enlarge Dataset, by resplitting data set to achieve 10 times more data

2. Combine linear combinatorics of raw feature as input feature

3. Let the invert of predictive to be Decision Tree's output to fine tune the loss function.

4. Let Random Regression Forest be the learning model, loss function be mse.
