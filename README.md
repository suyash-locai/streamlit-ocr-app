
## Description
This microservice aims to provide character recognition and text extraction from the images.
Currently, it supports the image parsing from .png and .jpg files.


## Getting Started
The service can be access through REST APIs for text extractions through single document or asynchronous batch processing.
In order to experience batch processing, you can use 1.png, 2.png and 3.png as input to trigger a batch job.
There are corresponding S3 object keys pre-created for demo purposes.

### Deployment
The Service is created using fastapi and python which can be deployed on any vpc, or on-prem.

### Dependencies
For the demo purposes, the infrastructure dependencies are set to AWS but can be setup to any infrastructure as per the requirement.



