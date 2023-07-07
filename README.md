<div align="right">
  <h3><a href='./01-intro/README.md'>Go to: MLOPS Environment Preparation</a></h3>
</div>

# mlops-zoomcamp-2023

<p align="center">  
  <a href="https://airtable.com/shrCb8y6eTbPKwSTL" target="_blank">
    <img src="https://github.com/celik-muhammed/mlops-zoomcamp/blob/main/images/banner.png?raw=true" height="200"></a>
</p>

<p align="center">
  <a href="https://airtable.com/shrCb8y6eTbPKwSTL"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>
</p>

Our MLOps Zoomcamp course

- Register in [DataTalks.Club's Slack](https://datatalks.club/slack.html)
- Join the [`#course-mlops-zoomcamp`](https://app.slack.com/client/T01ATQK62F8/C02R98X7DS9) channel
- [Tweet about the course!](https://ctt.ac/fH67W)
- Start watching course videos! [Course playlist](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK)
- [Technical FAQ](https://docs.google.com/document/d/12TlBfhIiKtyBv8RnsoJR6F72bkPDGEvPOItJIxaEzE0/edit) 
- For announcements, join our [Telegram channel](https://t.me/dtc_courses)

## Taking the course

### 2023 Cohort

* **Start**: 15 May 2023 (Monday) at 17:00 CET
* **Registration link**: https://airtable.com/shrCb8y6eTbPKwSTL
* Subscribe to our [public Google Calendar](https://calendar.google.com/calendar/?cid=M3Jzbmg0ZDA2aHVsY2M1ZjcyNDJtODNyMTRAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ) (it works from Desktop only)
* [Cohort folder](https://github.com/celik-muhammed/mlops-zoomcamp/tree/main/cohorts)


## What Does MLOps Mean?

- **`Machine learning operations (MLOps)`** is an approach to managing the entire lifecycle of a machine learning model — including its training, tuning, everyday use in a production environment and retirement.
- **`MLflow`** is an open source platform for managing the end-to-end machine learning lifecycle.


## Syllabus

### [Module 1: Introduction](01-intro)
* What is MLOps
* MLOps maturity model
* Running example: NY Taxi trips dataset
* Why do we need MLOps
* Course overview
* Environment preparation
* [Submitted Homework 1](https://github.com/celik-muhammed/mlops-zoomcamp-2023/blob/master/cohorts/2023/01-intro/Ride-Duration-Prediction-using-Regression-Analysis.ipynb)

[More details](01-intro)

### [Module 2: Experiment tracking and model management](02-experiment-tracking)

* Experiment tracking intro
* Getting started with MLflow
* Experiment tracking with MLflow
* Saving and loading models with MLflow
* Model registry
* MLflow in practice
* [Submitted Homework 2](https://github.com/celik-muhammed/mlops-zoomcamp-2023/blob/master/cohorts/2023/02-experiment-tracking/Mlflow-Ride-Duration-Prediction-Using-Regression-Analysis.ipynb)

[More details](02-experiment-tracking)

### [Module 3: Orchestration and ML Pipelines](03-orchestration)

* Workflow orchestration
* Prefect 2.0
* Turning a notebook into a pipeline
* Deployment of Prefect flow
* [Submitted Homework 3](https://github.com/celik-muhammed/mlops-zoomcamp-2023/blob/master/cohorts/2023/03-orchestration/Prefect-Ride-Duration-Prediction-Using-Regression-Analysis.ipynb)

[More details](03-orchestration)


### [Module 4: Model Deployment](04-deployment)

* Three ways of model deployment: Online (web and streaming) and offline (batch)
* Web service: model deployment with Flask
* Streaming: consuming events with AWS Kinesis and Lambda
* Batch: scoring data offline
* [Submitted Homework 4](https://github.com/celik-muhammed/mlops-zoomcamp-2023/blob/master/cohorts/2023/04-deployment/Deployment-Ride-Duration-Prediction-Using-Regression-Analysis.ipynb)

[More details](04-deployment)


### [Module 5: Model Monitoring](05-monitoring)

* Monitoring ML-based services
* Monitoring web services with Prometheus, Evidently, and Grafana
* Monitoring batch jobs with Prefect, MongoDB, and Evidently
* [Submitted Homework 5](https://github.com/celik-muhammed/mlops-zoomcamp-2023/blob/master/cohorts/2023/05-monitoring/Monitoring-Ride-Duration-Prediction-Using-Regression-Analysis.ipynb)

[More details](05-monitoring)


### [Module 6: Best Practices](06-best-practices)

* Testing: unit, integration
* Python: linting and formatting
* Pre-commit hooks and makefiles
* CI/CD (GitHub Actions)
* Infrastructure as code (Terraform)
* Homework

[More details](06-best-practices)


### [Project](07-project/)

* End-to-end project with all the things above

[More details](07-project/)



## Instructors

- Cristian Martinez
- Jeff Hale 
- Alexey Grigorev
- Emeli Dral
- Sejal Vaidya


## Other courses from DataTalks.Club:

- [Machine Learning Zoomcamp - free 4-month course about ML Engineering](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp)
- [Data Engineering Zoomcamp - free 9-week course about Data Engineering](https://github.com/DataTalksClub/data-engineering-zoomcamp/)


## FAQ

**I want to start preparing for the course. What can I do?**

If you haven't used Flask or Docker

* Check [Module 5](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/05-deployment) from ML Zoomcamp
* The [section about Docker](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/2_docker_sql) from Data Engineering Zoomcamp could also be useful

If you have no previous experience with ML

* Check [Module 1](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/01-intro) from ML Zoomcamp for an overview
* [Module 3](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/03-classification) will also be helpful if you want to learn Scikit-Learn (we'll use it in this course)
* We'll also use XGBoost. You don't have to know it well, but if you want to learn more about it, refer to [module 6](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp/06-trees) of ML Zoomcamp


**I registered but haven't received an invite link. Is it normal?**

Yes, we haven't automated it. You'll get a mail from us eventually, don't worry.

If you want to make sure you don't miss anything:

* Register in [our Slack](https://datatalks.club/slack.html) and join the `#course-mlops-zoomcamp` channel
* Subscribe to [our YouTube channel](https://youtube.com/c/datatalksclub)

**Is it going to be live?**

No and yes. There will be two parts:

* Lectures: Pre-recorded, you can watch them when it's convenient for you. 
* Office hours: Live on Mondays (17:00 CET), but recorded, so you can watch later.


**I just joined. Can I still get a certificate?**

* To get a certificate, you need to complete a project
* There will be two attempts to do a project
* First: in July, second: in August
* If you manage to finish all the materials till August, and successfully finish the project, you'll get the certificate


## Supporters and partners

Thanks to the course sponsors for making it possible to create this course

<p align="center">
  <a href="https://www.prefect.io/">
    <img height="100" src="images/prefect.png">
  </a>
</p>


<p align="center">
  <a href="https://wandb.ai/">
    <img height="100" src="https://datatalks.club/images/partners/wandb-abb.svg">
  </a>
</p>
