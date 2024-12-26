from app import app, db
from models import Friend

# Constants
REQUIRED_FIELDS = ["name", "role", "description", "email", "age", "mobile", "gender", "imgUrl"]

from flask import request, jsonify

@app.route("/api/friends",methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    friends = [friend.to_json() for friend in friends]
    return jsonify(friends)

@app.route("/api/friends",methods=["POST"])
def create_friend():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "Invalid JSON input"}), 400
        
        #Validation
        for field in REQUIRED_FIELDS:
            if field not in data or not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        email = data.get("email")
        age = data.get("age")
        mobile = data.get("mobile")
        gender = data.get("gender")
        img_url = data.get("imgUrl")
        
        
        # Fetch avatar image based on gender if img_url is not provided
        if not img_url:
            if gender == "male":
                img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
            elif gender == "female":
                img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
            else:
                img_url = None
        new_friend = Friend(name=name,role=role,description=description,email=email,age=age,mobile=mobile ,gender=gender,img_url=img_url)
 
        db.session.add(new_friend)
        db.session.commit()
 
        return jsonify(new_friend.to_json()),201
 
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#delete a friend
@app.route("/api/friends/<int:friend_id>",methods=["DELETE"])
def delete_friend(friend_id):
    try:
        friend = Friend.query.get(friend_id)
        if friend is None:
            return jsonify({"error":"Friend not found"}),404
        db.session.delete(friend)
        db.session.commit()
        return jsonify({"msg": "Friend deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
  
# Update a friend profile
@app.route("/api/friends/<int:id>",methods=["PATCH"])
def update_friend(id):
  try:
    friend = Friend.query.get(id)
    if friend is None:
      return jsonify({"error":"Friend not found"}), 404
    
    data = request.json
    
    friend.name = data.get("name",friend.name)
    friend.role = data.get("role",friend.role)
    friend.description = data.get("description",friend.description)
    friend.email = data.get("email",friend.email)
    friend.age = data.get("age",friend.age)
    friend.mobile = data.get("mobile",friend.mobile)
    friend.gender = data.get("gender",friend.gender)
    friend.img_url = data.get("imgUrl",friend.img_url)
    
    db.session.commit()
    return jsonify(friend.to_json()), 200
  except Exception as e:
    db.session.rollback()
    return jsonify({"error":str(e)}), 500