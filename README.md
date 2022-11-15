# Introduction

Cloud Project- 2 : EatWellLiveWell-Calorietracker Application [https://calorietracker.net]

University Name : http://www.sjsu.edu/

Course : Cloud Technologies- CMPE281

Professor's Name : [Sanjay Garje](https://www.linkedin.com/in/sanjaygarje/)
 
Team Name: Cloud Bloom<br/> <br/>
Team Members:
[Sirisha Polisetty](https://www.linkedin.com/in/sirishapolisetty/) <br/>
[Bhavya Hegde](https://www.linkedin.com/in/bhavya-hegde/) <br/>
[Darshini Venkatesha Murthy Nag](https://www.linkedin.com/in/darshini-venkatesha-murthy-nag-90052756/) <br/>
[Blessy Dickson Daniel Moses](https://www.linkedin.com/in/blessy-dickson/) <br/>

## Problem Statement

## Application Features
* Users can register and login using application custom login or through Amazon Cognito
* On successful Login, users can view list of food items
* Users can add new food items
* Users can view macronutrient breakdown for a particular food item
* Users can add the food they have consumed in a day in the food log to know about the total calories consumed and the macronutrients breakdown. 
* Users can log their weight and can see their weight history plotted in the form of a graph

## Admin Features:
* Admin can add/view new users and add new food categories.
* Admin can add new foods or modify food items and its details.
* Admin can also revoke access to users or remove food items and its details.


## Tools and Technologies used:
  * Frontend: HTML, Javascript, Bootstrap, ChartJs
  * Backend: Python Django framework
  * Other tools: GitHub actions for CI/CD, Visual studio code/any editor, Docker.
  
  
## Architecture Diagram

## AWS components
* Amazon RDS <br/>
  PostgreSQL is used as the database for the application to store all the user and food details.<br/>
* Amazon ElastiCache <br/>
  Memcache is used to render models  to the application quickly by caching responses from RDS.<br/>
* Amazon Redshift ML <br/>
  A redshift cluster has been created to import data from the database and then the model is created by running a K-means clustering algorithm.The clusters that are    created can be used to provide targeted experiences for the various clusters of users.<br/>
* Amazon SageMaker <br/>
  Redshift ML uses sagemaker internally to create training models and run the in-built machine learning algorithms.<br/>
* Amazon Cognito <br/>
  Aws Cognito is used to manage user authentications for calorie tracker.<br/>
* Amazon Route53 <br/>
  Route53 Setup done by adding a A Record to the domain for the alias of cloud front distribution created by Custom Domain Name setup of aws Cognito.<br/>
* AWS Certificate Manager <br/>
  AWS Certificate Manager has been created and validated to allow https traffic to auth flow.<br/>
* Amazon S3 <br/>
  Amazon S3 buckets are used to store application Images, Sagemaker data dump and CI/CD pipeline application data.<br/>
* S3 Transfer Acceleration <br/>
  S3 transfer acceleration is enabled to promote faster file upload to S3 bucket.<br/>
* Amazon CloudFront <br/>
  Amazon Cloudfront is used to render application Images.<br/>
* AWS Lambda<br/>
  Lambda function created for application S3 bucket is used to trigger email to admin when images are uploaded to S3 bucket.<br/> 
  Lambda function is created for Amazon Lex chatbot, which is used to fetch the calories of the food items from the dynamoDB.<br/>
* Amazon Simple Notification Service (SNS)<br/>
  SNS topic is created for sending email to admin once images are uploaded to S3 bucket.<br/>
* Amazon EC2 <br/><br/>
* Elastic Load Balancer (ALB)<br/><br/>
* Auto Scaling Groups <br/><br/>
* Amazon CloudWatch <br/><br/>
* Amazon Lex <br/><br/>
* Amazon DynamoDB <br/><br/>
* Amazon Rekognition <br/><br/>

  
  

## CI/CD Pipeline
* GitHub workflows, Amazon S3, Ubuntu  crontab, and Docker for CI/CD of this project.

## Instructions to run project locally

#### Create a virtual environment
```
python -m venv venv
  ```
#### Activate the virtual environment

* macOS:
```
source venv/bin/activate
```

* Windows:
```

venv\scripts\activate
```

#### Install required dependencies
```
pip install -r requirements.txt
```

#### Set up environment variables
```
touch .env
```
* We need to add below details in env
```
SECRET_KEY=''
DEBUG=True
DATABASE_NAME=''
DATABASE_USER=''
DATABASE_PASS=''
DATABASE_HOST=''
COGNITO_REGION_NAME=''
USER_POOL_ID=''
CLIENT_ID=''
CLIENT_SECRET=''
TOKEN_ENDPOINT=''
REDIRECT_URI=''
ELASTICACHE_HOST=''
AWSAccessKeyId=''
AWSSecretKey=''
REGION_NAME=''
```

#### Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

#### Create an admin user to access the Django Admin interface
```
python manage.py createsuperuser
```

#### Run the application
```

python manage.py runserver
```

## Sample Demo screenshots
![login](https://user-images.githubusercontent.com/111547793/201795997-9bb6482b-de73-4ae7-bc9f-18fea7e1c9d7.png)
![food_list](https://user-images.githubusercontent.com/111547793/201796014-61a10b0c-3a79-4bd8-bc5a-98227f8ae451.png)
![Food_Log](https://user-images.githubusercontent.com/111547793/201796036-41f8c50b-af5b-4192-9ef0-adab6235400c.png)
 

