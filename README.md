## Datamaster Prediction Contest

One of our biggest challenges to wider and scalable adoption of our dataset is our ability to match receipt lines items to categories and brands. To date we've primarily relied on human training in conjunction with a few ML approach's.

A company wide challenge is issued for the engineer who can develop the best model to predict unknown RSD's / item descriptions to brand AND categories.


## Criteria

#### Scoring
* Every percent point recall increase for brand or category will yield 1 pt
* Prediction model must yield 97%+ precision on current data 
* Category predictions must be at minimum at the major-cat level (3 levels deep)
* Recall based on basket-item impact, not unique RSDs or Item Descriptions. 

#### Deadline
* Model results due Sept 30th

#### Reward
* 5k stock options awarded to engineer who's model yields the most points.
* Minimum of 20 pts required (roughly ~10% increase in both brand/category)


## Data

To access data....


## Ideas

* Winning model will likely include a number an array of approaches, with each having their own recall/precision benefit.

* Edit Distance - RSD's with an edit distance of 1 will likely yield high precision. Edit distance of 2+ will have to be careful with

* TFIDF - Term frequency is another approach 

* Term/Character Location - Often the front part of the string may provider a better indicator than the latter part

* Business Rulesets - While advanced models will likely be required, be aware a list of simple rulesets may also provide significant recall.


