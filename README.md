# MA705 Final Project

This repository contains files used in the MA705 dashboard project.

The final dashboard is deployed on Heroku [here](https://ma705bostonuniversities.herokuapp.com).

### Dashboard Description
The dashboard is designed to help users have a better understanding of the time and location changes in NYC vehicle collisions from 2015 to 2017.
There are mainly two parts of the analysis:

* *Time Analysis* includes yearly, monthly, weekly and hourly changes in the number of vehicle collisions in NYC.
* *Location Analysis* includes vehicle collision distribution of different boroughs and street in NYC.

Users can click the options on left-side bar to choose the type of analysis you'd like to explore. Also, to better visualize and compare the changes, they can select the year or boroughs they would like to put in each analysis.
            
### Data Sources
The original dataset is obained from Kaggle [here](https://www.kaggle.com/nypd/vehicle-collisions).
And this vehicle collision data was collected by the NYPD and published by NYC OpenData.

### Data Process
First, I dropped the collisions that don't have any location information, such as latitude or longtitude.
Then, I found there are some collisions whose longitude and latitude are not in the borough where it was recorded to occur. So I make the polygon for each borough, and check whether the latitude/longitude is consistent with the borough in the "BOROUGH" column. By doing this, I removed the collisions that have inconsistent location information.
Finally, considering that the "TIME" in original data is a combination of hour, month, year, in order to make the subsequent analysis clearer, I transfer this combination into seperate hour, month, year and day of week, and store them into a column respectively.

### Other Comments
The dashboard is designed to be multi page dashboard.