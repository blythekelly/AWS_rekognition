
import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import boto3, botocore
from boto3.dynamodb.conditions import Key
import rekognitionTester

app=Flask(__name__)

#variable that will store the submitted file's name
FILE_NAME=""

#configuring credentials for the flask app to access S3
app.config['S3_BUCKET'] = "bakdrakecs178spring2023"
app.config['S3_KEY'] = "AKIAWR6RD5RKVAVMEP7A"
app.config['S3_SECRET'] = "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"
app.config['S3_LOCATION'] = 'http://bakdrakecs178spring2023.s3-website-us-east-1.amazonaws.com'

#giving the keys to boto3
s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

#displaying the home screen
@app.route('/')  
def home():
    return render_template("layout.html")

#handling form submissions
@app.route('/upload',methods=['post'])
def upload():
    
    #checking if there has been a submission
    if request.method == 'POST':
        
        #defining a variable to hold the photo that was submitted
        picture = request.files['file']
        
        #checking if this photo exists
        if picture:
                #a variable to hold the file name
                filename = secure_filename(picture.filename)
                
                #saving the photo
                picture.save(filename)
                
                #uploading the file to my S3 bucket
                s3.upload_file(
                    Bucket = 'bakdrakecs178spring2023',
                    Filename=filename,
                    Key = filename
                )
                #storing the file name in the global variable
                FILE_NAME=filename
                
    """returning the HTML that is generated through the detect_labels_html function
    This passes the actual file name and my S3 bucket's name to the function, and
    the function will return the formatted HTML to the same screen that the user is currently on.
    """
    return rekognitionTester.detect_labels_html(FILE_NAME, 'bakdrakecs178spring2023')

#defining a getter method that is used in rekognitionTester.py to access the global file name   
def getFileName():
    return FILE_NAME

#runnning flask app 
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
