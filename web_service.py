import json
import os
import shutil
import flask
import werkzeug
from flask import Flask, request
from flask_restplus import Api, Resource , fields
from werkzeug.datastructures import FileStorage
import face_rec
from decoupagevedio import decoupage

app = Flask(__name__)
api = Api(app=app, version='0.1', title='ApiV', description='', validate=True)

""" UPLOAD_DIRECTORY = "/unkownPic" """


@api.route("/video/<string:title>")
class decoupeV(Resource):
    def post(self, title):
        print(title)
        data = request
        print(title)
        print(data)
        decoupage(title)


parser = api.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True)


@api.route('/with-parser/parser/')
@api.expect(parser)
class WithParserResource(Resource):
    @api.doc(parser=parser)
    def post(self):
        data = flask.request.files['file']
        print(data)
        filename = werkzeug.utils.secure_filename(data.filename)
        print("\nReceived image File name : " + data.filename)
        saved_path = os.path.join("test", filename)
        data.save(saved_path)
        message=identifier.get(self)
        return "Image Uploaded Successfully"+ json.dumps(message)



class identifier(Resource):
    def get(self):
        for image_file in os.listdir("test"):
            full_file_path = os.path.join("test", image_file)

        print("Looking for faces in {}".format(image_file))

        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        predictions = face_rec.predict(full_file_path, model_path="trained_knn_model.clf")

        # Print results on the console
        list=[]
        for name, (top, right, bottom, left) in predictions:
            list.append(name)
            print("- Found {} at ({}, {})".format(name, left, top))

        # Display results overlaid on an image
        #face_rec.show_prediction_labels_on_image(os.path.join("test", image_file), predictions)

        """ if name.find("unknown") != "unknown": """
        
        print(list)
        if "unknown"  not in list and len(list)>0 :
            shutil.copy(os.path.join("test", image_file), 'picture/' + name)
            os.remove(os.path.join("test", image_file))
            return {"statu": True, "message": "found face ", "response": list}
        else:
            shutil.copy(os.path.join("test", image_file), 'unkownPic' )
            os.remove(os.path.join("test", image_file))
            return {"statu": False, "message": "found face ", "response": list}


if __name__ == "__main__":
    app.run(port=8885, host='localhost')
