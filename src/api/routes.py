"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Photo, Order, OrderItems
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

ENDPOINT = "https://westeurope.api.cognitive.microsoft.com/"
project_id = "4a0d1a7e-a87e-43e2-838c-3eec869f5aeb"
prediction_key = "225ae10ed4e14b4ea2a4e56ac1a9474f"
publish_iteration_name ="Iteration4"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)


with open("C:/Users/USUARIO/Pictures/BeBanana/HollybikeSonia.png", node="rb") as test_data:
    results = predictor.detect_image(project_id, publish_iteration_name, test_data)

for prediction in results.predictions:
    print("\t" + prediction.tag_name + """": {0:2f}% bbox.left = {1:2f}%, bbox.top = {2:2f}%, 
    bbox.width = {3:2f}%, bbox.height {4:2f}%""".format(prediction.probability * 100, prediction.bounding_box.left, 
    prediction.bounding_box.top, prediction.bounding_box.width,prediction.bounding_box.height,))
 
@api.route('/users', methods = ['GET'])
def get_users(): 
    users = User.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))
    response_body = {
        "message" : "Nice!",
        "data": users_serialized
    }
    if (users == []):
        return jsonify({"msg": "Not users yet"}), 404
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>', methods = ['GET'])
def get_user(user_id): 
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
        
    user_info = User.query.filter_by(id=user_id).first().serialize()
    print ("AAAAAAAAAAAAAA", user)
    response_body = {
        "message" : "Nice!",
        "data": user_info
    }

    return jsonify(response_body), 200

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    users_query = User.query.filter_by(email=email).first()
    if not users_query:
        return jsonify({"msg": "Doesn't exist"}), 402
    if password != users_query.password:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@api.route('/register', methods=['POST'])
def register():
    request_body = request.get_json()

    if User.query.filter_by(email=request_body["email"]).first():
        return jsonify({"msg": "Email already exists"}), 409
   
    user = User()
    user.new_user(
        email=request_body["email"],    
        password=request_body["password"],
        username=request_body["username"],
        name = request_body["name"],
        firstname = request_body["firstname"],
        role = request_body["role"]
    )

    access_token = create_access_token(identity=request_body["email"])
    return jsonify(access_token=access_token), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        User.query.filter_by(id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "User deleted"}), 200
    else:
        return jsonify({"msg": "User doesn't exist"}), 401
    
@api.route('/photos', methods=['POST'])
def post_photo():
    request_body = request.get_json()

    if Photo.query.filter_by(id=request_body["id"]).first():
        return jsonify({"msg": "Duplicated image"}), 409
   
    photo = Photo()
    photo.new_photo(
        id=request_body["id"],    
        url=request_body["url"],
        bicycle=request_body["bicycle"],
        helmet = request_body["helmet"],
        price = request_body["price"],
        user_id = request_body["user_id"]
    )

