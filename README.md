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

#### Downloading the data

To access data. Follow steps which will setup environment and install the data files into the data folder:

    $ mkvirtualenv dmcontest
    $ git clone git@github.com:infoscout/dmcontest.git
    $ cd dmcontest
    $ pip install -r requirements.txt
    $ python download.py
    
The following 4 datasets are provided:

* `trained_brands.csv` - Trained Brands
* `trained_categories.csv` - Trained Categories
* `unknown_brands.csv` - Unknown brands
* `unknown_categories.csv` - Unknown categories

In addition the following be helpful:

* `brands.csv` - Brand keys and descriptions
* `categories.csv` - Categories key and descriptions
    

#### Browsing data

Check `read.py` to see example of reading the data:

    $ python read.py
    

For `trained_brands.csv` for example, you will likely be most interested in:

* `item_descriptor` - RSD (receipt short description) or Item Description (what's scrapped off a website)
* `major_brand` - The top level brand assigned
* `medium_brand` - The next brand level down
* `count` The number of occurences on receipts

I also recommend at browing the [datasources binder](http://ds.infoscoutinc.com/admin/datasieve/binder) to get a quick understanding of the gaps in our data.


#### Data Cleaning

Note you'll want to peform some level of cleaning on both training and unknown data before prediction. A few notes:

* Removing amounts / qtys that should not be included (i.e. QTY 3 DIET COKE)
* Ignoring or removing indeterminate / unknown


## Developing your model

Simply create a branch to develop your model on (no peaking!). 


## Ideas

* Browse the RSD binder to get a sense of the gaps in brand & categoires

* Trained items with higher counts (number of occurences on a receipt) will likely be considered more confident as we've spent more time on the head then tail. 

* Winning model will likely include a number of approaches, with yielding their own recall/precision benefit.

* Edit Distance - RSD's with an edit distance of 1 will likely yield high precision. Edit distance of 2+ will have to be careful with

* TFIDF - Term frequency is another approach. 

* Term/Character Location - Often the front part of the string may provider a better indicator than the latter part.

* Business Rulesets - While advanced models will likely be required, a list of simple rulesets may also provide significant recall.

* Third party tools (i.e. Google Predict, etc) are fair game!
