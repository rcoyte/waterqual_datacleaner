# waterqual_datacleaner
Used to stitch together data downloaded from https://www.waterqualitydata.us/ so that it connects places to data and unmelts the dataframe

A few known issues: 
1) Does not standardize units before unmelting data.
2) Does not deal with detection limits/ censor data that is below detection limit
