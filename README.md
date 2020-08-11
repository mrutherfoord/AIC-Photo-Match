# AIC-Photo-Match

Web app project using paintings from the Art Institute of Chicago

## Live Site

The live build of this project can be found
[here](https://bradleyhop.github.io/scratch-aic/).

## Goals

The first goal of this project is to build a web application that allows users
to upload a photo and returns a painting from the art institute that most
closely matches the dominant color of the uploaded image. Ultimately, the user
will be able to choose a color palette (analagous, complimentary, or tertiary),
and have the application return paintings that most closely match the palette.

## Contributors

[Melissa Rutherfoord](https://github.com/mrutherfoord) is writing the machine
learning code for the color matching algorithms and their implementation via AWS
Lambda functions.

[Bradley Smith](https://github.com/bradleyhop) is writing a front end user
interface so developers can see the results of various image uploads and test
the functionality of the machine learning and AWS Lambda functions.

## Structure of Project

The root direct contains the Python Jupyter file that contains the machine
learning and AWS Lambda code. The directory frontend/ contains the front end web
user interface.
