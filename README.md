# QB-iQ

<br>
QB-iQ aims to quantify the decisions a quarterback makes by estimating the Expected Points Added and compltion percentage for all eligable receivers on the field between the time when the ball was snapped and when a forward pass was made.
<br><br>

## Source Data
- [NFL NextGen Stats](https://www.kaggle.com/c/nfl-big-data-bowl-2021/data)
- 15 million+ rows of data
- 250+ games from the 2018 season
- Only includes passing plays
<br><br>

## Problem Statement
    Traditional football metrics only measure player’s performance as it happened on the field – which can be measured and recorded in a “box score.”
    
    However, no metrics currently exist that measure a quarterback’s decision making.

An ensemble of machine learning algorithms will be trained to estimate the catch percentage of all receivers by leveraging player tracking data released by the NFL in the yearly Kaggle competition, "Big Data Bowl."
<br><br>

## Expected Points Added
It is important to understand the concept of Expected Points Added (EPA) before diving into QB-iQ. The key takeaways from EPA are as follows:
- All yards are not valued equally
- As the distance to the opponent's end zone decreases, the average number of points a team is expected to score on a given drive will increase.
- Assuming the distance to the end zone remains constant, as distance to the line to gain increase EPA will decrease.
- Assuming the distance to the end zone and the distance to the line to gain remain constant, as the down increases EPA will decrease.

To illustrate this point, take a look at the series of graphs shared by [nfelo](www.nfeloapp.com).

![Expected Outcomes](/submissions/projects/Capstone/Presentation_Images/expected_outcomes.png)
Expected points are calculated by averaging the the number of points expected to be scored on a given drive relative to all possible outcomes.

![EPA Slopes](/submissions/projects/Capstone/Presentation_Images/epa_slopes.png)
Expected Points will change drastically depending on the down. The expected number of points on 4th down is lower than the expected number of points on 1st down.

![Example A](/submissions/projects/Capstone/Presentation_Images/epa_a.png)
Expected points from the 50 yard line on a 5 yard gain with 4 yards needed for a 1st down is positive.
![Example B](/submissions/projects/Capstone/Presentation_Images/epa_b.png)
Expected points from the 50 yard line on a 5 yard gain with 6 yards needed for a 1st down is negative.
<br><br>

# Modeling
The first step is to model a quarterback's completion percentage.

## Baseline
An average quarterback is expected to complete roughly 64% of forward passes. This means the data set will have a 2:1 imbalance and a Balanced Accuracy Score will be the best option for judging model performance. There is no advantage for specifically predicting the positive class or the negative class.

## Logistic Regression
Logistic regression consistently performed worse than decision tree models and neural networks. For this reason, it was not included in the final ensemble model.

## Decision Trees
Decision Trees performed nicely on this data set. There are enough observations (number of plays) to allow for the depth of the trees to go reasonably deep, but still generalize on unseed data well. The highest performing models were fit tightly to the training data, but also performed well on the testing data.

It should be noted, the optimal test scores were achived with the model being tightly fit to the training data. Having more observations to train the models on would likely go a long way. Decision trees are prone to overfitting, by nature.

Grid searching hyperparameters was used to tune these models.

## Deep Learning
Given the complexity of the coordinate data, distance to the ball, and distance to the nearest opponent, neural networks were a natural fit for this project. Dozens of iterations of neural networks were fit and ultimately performed the best on the test set. More regularization was applied to these models. This helped reduce the overfitting relative to the decision trees.

## Ensemble Classifier
A combination of decision trees and neural networks returned the highest balanced accuracy score. The difference between the train and test set error scores was reduced drastically. This approach appears to find a nice balance between bias and variance.
