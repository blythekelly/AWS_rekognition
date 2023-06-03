import boto3
import flaskApp

#tester function to work with rekognition
def detect_labels(photo, bucket):
    
    #using my default profile to start a boto3 session
    session = boto3.Session(profile_name="default")
    
    #using rekognition as the client     
    client = session.client('rekognition')
    
    #specifying that the image comes from my S3 bucket 
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
    MaxLabels=10,
    )

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        
        #printing each label and confidence percentage
        print("Label: " + label['Name'])
        print("Confidence: " + str(label['Confidence']))

        #printing other names for the labels
        print("Aliases:")
        for alias in label['Aliases']:
            print(" " + alias['Name'])

            #printing each category for the image
            print("Categories:")
        for category in label['Categories']:
            print(" " + category['Name'])
            print("----------")
            print()

    if "ImageProperties" in str(response):
        print("Background:")
        print(response["ImageProperties"]["Background"])
        print()
        print("Foreground:")
        print(response["ImageProperties"]["Foreground"])
        print()
        print("Quality:")
        print(response["ImageProperties"]["Quality"])
        print()

    return len(response['Labels'])
  
  
#function to create HTML to display the labels detected for the image on the Flask app  
def detect_labels_html(photo, bucket):
    
    #using my default profile to start a boto3 session
    session = boto3.Session(profile_name="default")
      
    #using rekognition as the client  
    client = session.client('rekognition')

    #specifying that the image comes from my S3 bucket
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
    MaxLabels=10,)
    
    #obtaining file name from the flaskApp form
    image=flaskApp.getFileName()
    html=""
    html+='<center><p>Detected labels for ' + photo+"</p></center>"
    
    #in this HTML version of displaying the Rekognition labels, I reduced the amount of information that is returned.
    for label in response['Labels']:
        html+=("<center><br><br><p> Label: " + label['Name']+"</p>")
        html+=("<p> Confidence: " + str(label['Confidence'])+"</p>")

        html+=("<p> Aliases: </p>")
        for alias in label['Aliases']:
            html+=(" " + alias['Name'])

            html+=("<p> Categories:</p>")
        for category in label['Categories']:
            html+=(" " + category['Name']+"</center>")
  

    return html


def main():
    #testing an image to see if the function displays the correct labels
    #the image is of a butterfly and purple flowers, so the labels printed to the console were expected.
    photo = '15CCB514-76C5-4C9F-A560-E802BAC58CB5_4_5005_c.jpeg'
    bucket = 'bakdrakecs178spring2023'
    label_count = detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))

if __name__ == "__main__":
    main()
