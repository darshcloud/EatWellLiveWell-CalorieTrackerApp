# Introduction

* Cloud Project- 2 : EatWellLiveWell-Calorietracker Application [https://calorietracker.net]

* University Name : http://www.sjsu.edu/

* Course : Cloud Technologies- CMPE281

* Professor : [Sanjay Garje](https://www.linkedin.com/in/sanjaygarje/)

* Students : 

<hr>

# Problem statement

## User Features:
* 
* 
* 
* 
* 
* 
* 
* 

## Admin Features:
* Admin can add/view new users and add new food categories.
* Admin can add new foods or modify food items and its details.
* Admin can also revoke access to users or remove food items and its details.


## Tools and Technologies used:
  * Frontend: HTML,Javascript,Bootstrap,ChartJs
  * Backend:Python Django framework
  * Other tools: GitHub actions for CI/CD,Visual studio code/any editor,Docker.
  
  
## Architecture Diagram

## AWS components
* RDS: PostgreSQL is used as the database for the application to store all the user and food details.
* ElastiCache: Memcache is used to render models  to the application quickly by caching responses from RDS.
* Redshift ML: A redshift cluster has been created to import data from the database and then the model is created by running a K-means clustering algorithm.The clusters that are created can be used to provide targeted experiences for the various clusters of users.
* SageMaker: Redshift ML uses sagemaker internally to create training models and run the in-built machine learning algorithms.

## Instructions to run project locally

## Sample Demo screenshots
