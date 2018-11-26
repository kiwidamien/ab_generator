# Sample A/B test

## Experiment

BuyMoreStuff.com are looking at the effect of changing the size and color of "Show Me" button. This appears in lists of recommended items. At the moment, the experiment is only being run on shoes.

The experiment started on 2018-10-01, and ran until 2018-11-05. You may or may not need all this data (normally a _power analysis_ would be done ahead of time to figure out how much data was needed).

Data has also been suppled from 2018-09-24 (i.e. before the experiment started). You can use this to determine a baseline probability.

## Metric

BuyMoreStuff.com's site is currently optimized for _desktop_ usage. They would like to see a 10% lift in the click-through-rate if it exists (i.e. this is the minimal detectable effect). The hope is a 10% lift in the CTR would correspond to a 10% lift in purchases, although this is probably optimistic.

You should decide on the alpha and beta parameters for the test.

## Questions

1. Use the "historical data" (i.e. 2018-09-24 to 2018-09-30) to determine what the current desktop CTR is, and the current viewing rate. How many weeks of data would you need to find a 10% lift (assuming a 10% lift exists).

2. Run an analysis on the appropriate number of weeks of data while the experiment is running. Is there a statistically signficant difference?

3. The product team is interested in the responses between men and women. You know that you would have to rerun the experiment, but you can use the weeks of data that you used in step 2 to do EDA to know what hypothesis you want to check in the next run through. The main questions the product team have are
  - Do men and women have the same CTR?
  - Do men and women both select the same "winning" variation?
  - Is the effect of switching the variation the same for men and women?

4. BuyMoreStuff.com's CTO is interested in expanding to more devices. She asks you to run your analysis in step 2 without filtering down to just the desktop device. Rerun your analysis. What is the conclusion about the variations now? How would you follow up? Is there further analysis to do?

5. The main metric was _CTR_, which is appropriate since you are changing a UI element on the page. The CTO is curious about whether or not this is appealing to certain people more. She asks if there is a statistically significant difference between the desktop click-through-probability (CTP) between the variation and the control.

## Data dictionary


### user_public.csv

Describes a subset of the user's features, and the variation that user is assigned to, (Should probably include signup_date, but was left out of simuation).

| field | description |
| --- | --- |
| username | Unique identifier for the user |
| gender | 'M' or 'F' |
| state | Two-letter abbreviation for the state user registered in |
| user_agent_string | a string representing the user's browser when creating account |
| variation | either `control` or `variation`, depending on which variation the user is assigned to |


### visits.csv

Describes visits to a page that contains the button in question. 


| field | description |
| --- | --- |
| username | Identify's the user on this page |
| experiment_id | Identifies the experiment (all entries are `button_clr`) |
| viewed_at | Timestamp, identifying when user landed on page |
| device | Type of device (`desktop`, `mobile`, `tablet`) used to view the page |
| variation | Either `control` or `variation`. Tells us which version of page was displayed. During the experiment, this will match the user's `variation` field. Before or after the experiment, this will be `control`. This field is the authoritive one on which version of the page was actually displayed | 
| success | `True` or `False`. Is `True` is a "Show Me" button is clicked |


## Issues

This isn't a perfect simulation of an A/B test. For a start, you have been given a metric and a way to approach the problem. The framework of the tables is generally good (having a table that records the result for a specific interaction) as this 
- generalizes to multiple experiments
- allows you to create an A/A test, and then use a very similar framework for an A/B test
 
However, there are some things missing:
* Sign up date is absent
* User-agent string should be included in the `visits.csv` table. This made the file much larger, with little benefit.
* Ability to set on metrics.
* No users join or leave the platform while experiment is running.
* This is also data from a fairly small userbase, with high activity (e.g. similar to deviantart). A more typical site would have more users, but each user would be less active
