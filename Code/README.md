# Data Science Workflow Manager

## Prerequisites:
- The Dependencies for this application are specified in requirements.txt
- Use pip install -r requirements.txt to install all of them at the same time 
- Before you can run the app, you must unzip the data file so that the models can be trained with the appropriate data and the scritps can proccess it if they need to. 

## To Run the app Use:
'make' or 'make run' to run the redis server used for caching and the python application

The server should start on port 5000. To access the web application go to localhost:50000


#Contents

This repository contains the source files for the web application wrokflow management system. 
In the wfmg folder we have a the mian files that deal with routing for the flask part of the app 
and callback for the dashboard 

# wfmg folder: 

This folder contains files for the web application and for the plug-in architechture. 

The plug-in architechture is an important part of the application since it allows developers to create new model and deal with the raw data. 
the folder that contains the files for the plug-in architechture is workFlowManager. this module contains classes for procedures such as the frequncy and the probability distributions as well as the classes for implementing machine learning models. 

The callback folder contains the sourcode required to create an interactive dashboard. Here we use Dash to create a user interface without the need to user react or any other user interface library to accomplish it. 

The templates folder contains html files that are used in the flask application. 

In the static and assets folder we have css code and javascript that are used in the interactive dashboard and in the rest of the flask application. 

app.py contains the dash application that is triggered when the user click on the link for the dashboard. 

we also have routes.py wich is pretty common in flask application. This file containes all the routes or pages for the flask app. 


# script folder: 

This folder contains all the scripts that are used in the processing steps of the data science workflow. 

The make file in the main directory is used to trigger the scripst and start processing the data. 

# Data folder: 

This folder contains the files that are going to be processed by the scripts so that the visualization part of the app (Dash) can get that data and plot it in the dashboard. 

Here we have files from DB1B and from T100

For more information about the project, please go to the videos. We esplained everything in a lot more detail there. https://www.youtube.com/playlist?list=PLG3lylzOg8Fj4oIe69NSAlziteyjSEc7z


## Authors

* **Tomas Ortega**
* **Serge Metellus**

## License

This project is licensed under the MIT License