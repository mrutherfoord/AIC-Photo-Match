# AIC API Front End App

This directory contains the web-based front end tool so that developers can have
real-time feedback on image upload, processing, and any errors within this
chain.

## Live Site

The deployment build of this project can be found
[here](https://bradleyhop.github.io/scratch-aic).

## Tools

Vue.js and Vue CLI is the front end framework in building this project. Eslint,
stylelint, and other Vue-specific linters help me maintain and write consistent
code. Most of the code I've written, if you're unaccustomed to Vue, is
/src/App.vue and /src/components/* .

## User Stories, Method, Pitfalls, and TODO

### User Stories

1. The user can select a jpeg, jpg, or png image from from their computer to upload.
    * The uploaded file is sent to an AWS Simple Storage Service (S3) bucket.
2. The user can see a progress bar tracking the upload progress.
    * If upload is successful, show message saying so.
    * If upload is unsuccessful, show error message in browser.
3. Upon successful upload, user can see the image chosen in the 'Uploaded Image'
   card.
4. Once the data is returned, the user can see:
    * The computed dominant color of their uploaded image in the 'Uploaded
        Image' card.
    * A work of art displayed in the 'AIC Match' card from the Art Institute of
        Chicago's Api that most closely matches that color.
    * The color the algorithm from the art work that was matched in the 'AIC
        Match' card.

### Methods

The AWS chain is defined by Step Functions. The front end utilizes the AWS
javascript API to interface with it's services.

1. Read file info and upload to configured AWS S3 bucket.
2. Lamda function is triggered on upload. Once triggered, the Lamda function
   with process the image according to its algorithm to determine dominant color
   and Art Institue of Chicago art work match.
3. Lamda function sends json result to AWS Simple Notification Service (SNS). The
   SNS service then sends the json data to AWS Simple Queue Service (SQS).
4. The json data sits in the SQS queue until the browser makes a request for the
   data.
5. Data is sent to browser and is processed by the app to display data
   information.

### What I Would Chnage if I Had More Time

1. The design structure my collaborator and I chose gets the job done: upload
   and image, process it, and return some data in json form. However, the chain
   of S3 -> Lamda function -> Lamda function -> SNS -> SQS does not seem very
   efficient. However, since I've no back end web develop training yet, this
   seemed to be the best choice to prototype the app. I was able to make the
   appropriate method calls for each service after digging around the
   (well-documented) AWS services APIs.
2. It's not secure in that anyone can upload anything to the S3 bucket,  and I'm
   not sure if the messages in the SQS are always going to go to the correct
   user instance.
3. If the processing time for the image is too long, the results will not be
   pushed  in time to SNS and SQS within the 20 second max timeout allowed in
   the AWS sqs.receiveMessage() method: the call to this method is fired as soon
   as the image is successfully uploaded.

### TODO

1. Learn and implement AWS Restful API to trigger Lamda functions and serve
   computed json data.
2. Add more error checking for download of images from the Art Institute's API.
   (Note: As of 9/2/2020, more error checking immplemented and shown to user at
   every step of chain.)
3. Enforce file type and size upload limit.
4. Add more data to json like links to the Art Institute's page on the work, or
   maybe a wikipedia article. These extra bits of information will bring the app
   closer to something usable to the general public.
