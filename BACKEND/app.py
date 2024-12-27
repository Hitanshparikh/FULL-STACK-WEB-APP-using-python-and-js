from flask import Flask, request, jsonify
from models import db, Friend
from validate_email import validate_email

app = Flask(__name__)

REQUIRED_FIELDS = ["name", "role", "description", "email", "age", "mobile", "gender"]

@app.route("/api/friends", methods=["GET", "POST"])
def friends():
    if request.method == "GET":
        return get_friends()
    elif request.method == "POST":
        return create_friend()

def get_friends():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        friends = Friend.query.paginate(page=page, per_page=per_page, error_out=False)

        if not friends.items:
            return jsonify({"message": "No friends found."}), 404

        return jsonify([friend.to_json() for friend in friends.items]), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching friends."}), 500

def create_friend():
    try:
        data = request.json
        missing_fields = [field for field in REQUIRED_FIELDS if field not in data or not data[field]]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        if not validate_email(data["email"]):
            return jsonify({"error": "Invalid email format."}), 400

        img_url = generate_img_url(data.get("gender"), data.get("name"))
        new_friend = Friend(
            name=data["name"],
            role=data["role"],
            description=data["description"],
            email=data["email"],
            age=int(data["age"]),
            mobile=data["mobile"],
            gender=data["gender"],
            img_url=img_url,
        )

        db.session.add(new_friend)
        db.session.commit()
        return jsonify(new_friend.to_json()), 201

    except ValueError as ve:
        return jsonify({"error": "Invalid data type provided."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating a friend."}), 500

def generate_img_url(gender, name):
    if gender == "male":
        return f"https://avatar.iran.liara.run/public/boy?username={name}"
    elif gender == "female":
        return f"https://avatar.iran.liara.run/public/girl?username={name}"
    return None

if __name__ == "__main__":
    app.run(debug=True)
