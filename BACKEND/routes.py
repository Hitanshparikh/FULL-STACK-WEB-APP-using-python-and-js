from app import app, db
from models import Friend
from flask import request, jsonify
from validate_email import validate_email

# Constants
REQUIRED_FIELDS = ["name", "role", "description", "email", "age", "mobile", "gender"]

def generate_img_url(gender, name):
    if gender == 'male':
        return f"https://avatar.iran.liara.run/public/boy?username={name}"
    elif gender == 'female':
        return f"https://avatar.iran.liara.run/public/girl?username={name}"
    return None

@app.route("/api/friends", methods=["GET", "POST"])
@app.route("/api/friends", methods=["GET", "POST"])
def friends():
    if request.method == "GET":
        return get_friends()
    elif request.method == "POST":
        return create_friend()

def get_friends():
    print("Fetching all friends...")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    friends = Friend.query.paginate(page=page, per_page=per_page, error_out=False)

    friends_data = [friend.to_json() for friend in friends.items]

    # Check if any friends were found
    if not friends_data:
        return jsonify({"message": "No friends found."}), 404

    print(f"Found {len(friends_data)} friends.")
    return jsonify(friends_data), 200

def create_friend():
    try:
        data = request.json
        print(f"Received data for new friend: {data}")

        # Validation
        for field in REQUIRED_FIELDS:
            if field not in data or not data.get(field):
                error_message = f"Missing required field: {field}"
                print(error_message)
                return jsonify({"error": error_message}), 400

        # Validate email format
        if not validate_email(data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate age
        
        img_url = generate_img_url(data["gender"], data["name"])

        # Create new friend
        new_friend = Friend(
            name=data["name"],
            role=data["role"],
            description=data["description"],
            email=data["email"],
            age=data["age"],
            mobile=data["mobile"],
            gender=data["gender"],
            img_url=img_url,
        )

        db.session.add(new_friend)
        db.session.commit()
        print(f"New friend created: {new_friend.to_json()}")
        return jsonify(new_friend.to_json()), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating friend: {e}")
        return jsonify({"error": str(e)}), 500
