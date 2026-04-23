

8

## B. *Queue Prioritization Experiment*

We tested our method for prioritizing the crawling queue using Bengali language Twitter users. In order to properly compare the various methods we first collected a data set of 10,785 Twitter users. (5,684 users came from our search queries and an additional 5,103 came from those users' social connections.) The way the queue ranking works is to first download a small set of users and use that as training data to learn a ranking for the rest of the download queue. We randomly selected 300 users for our training set. The ranking methods were used to order the remaining 10,000+ users in the simulated download queue.

In Figure 2, we show the cumulative in-vocabulary tokens obtained as an additional 500 users are processed from the download queue for each of the three prioritization strategies. The predictive ranking provides three times as many in-vocabulary tokens as either the edge count ranking or the random baseline. Figure 3 is similar but shows the cumulative vocabulary coverage (types) where the vocabulary is taken from a held-out dev set different from the text used to produce the Twitter queries. The horizontal line represents the type coverage of the in-domain training data. The predictive ranking covers an additional 10% of the dev-set vocabulary compared to either of the other strategies. More than 53% of the vocabulary types and about 9% of the tokens in the dev-set are not found in the in-domain training data. The Twitter data downloaded using the predictive ranking covers 56% of these previously unseen vocabulary types, substantially outperforming the edge count ranking and the random baseline. The match between the vocabulary of the data obtained with the predictive ranking with the in-domain data is an indication of the value of the predictive ranking strategy.

The most important features for the predictive ranking (as measured by the average decrease in node impurity in the random forest regression model) are average number of reverse followers in the training set, average sentence count after filtering among followers in the training set and average sentence count after filtering among mentioners in the training set. Even though edge features highly influence the predictive ranking model, the edge count ranking is worse than the predictive ranking on both of the type coverage and the cumulative IV token metrics. This is because there are high edge count connections from Bengali speaking Twitter users to international celebrities, which fools the edge count ranking strategy but not the random forest regression. (The top followed Twitter user by Bengali speakers is @BarackObama followed by @BillGates.)

We created language models from the downloaded data to compare the effectiveness of the ranking strategies. The language models used the data from the 300 users in the training set as well as the additional users selected by each of the respective ranking strategies. Table VI lists the resulting perplexities on the held-out in-domain data. The predictive ranking LM achieved a 17% reduction in perplexity over the random baseline after downloading 500 users from the queue. When less than 500 additional users are downloaded, the predictive ranking has a better perplexity than the edge

| Additional Users Downloaded | Predictive Ranking | Random Baseline | Edge Count Ranking |
| --------------------------- | ------------------ | --------------- | ------------------ |
| 0                           | 0.00               | 0.00            | 0.00               |
| 100                         | 0.50               | 0.10            | 0.08               |
| 200                         | 0.75               | 0.20            | 0.18               |
| 300                         | 1.00               | 0.30            | 0.28               |
| 400                         | 1.15               | 0.38            | 0.35               |
| 500                         | 1.25               | 0.43            | 0.42               |


Fig. 2. IV Tokens Gathered by Crawling Strategy