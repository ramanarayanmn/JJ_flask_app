from flask import Flask,render_template,request
import json
import random
import base64
#from detect import ImageProcessor
import detect
import os

app = Flask(__name__)

imageList = {}

@app.route("/health")
def healthCheck():
    return "Hello, World!"

@app.route("/getImages")
def getImages():
    return imageList

@app.route("/uploadImages", methods = ["POST"])
def uploadImages():
    objectId = str(random.randint(0,10000000))
    print(request.json)
    imageList[objectId] = request.json

    imageEncodedVersion = request.json["image"].split(",")
    extension = "png"
    if "jpeg" in imageEncodedVersion[0]:
        extension = "jpeg"
    # Decode the image data and Write Image data to a file
    with open("./images/imageToSave"+objectId+"."+extension,"wb") as file:
        file.write(base64.decodebytes(bytes(imageEncodedVersion[1],"utf-8")))
    return getImages()



@app.route("/deleteImages", methods = ["POST"])
def deleteImages():
    for objectId in request.json.keys():
        imageEncodedVersion = imageList[objectId]["image"].split(",")
        extension = "png"
        if "jpeg" in imageEncodedVersion[0]:
            extension = "jpeg"
        filename = "./images/imageToSave"+objectId+"."+extension
        os.remove(filename)
        del imageList[objectId]
    return getImages()


@app.route("/callScript", methods = ["POST"])
def callScript():
    result = detect.customMain()
    print("Logging result variable", result)
    print("hello")
    return "3 JJ powders"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()