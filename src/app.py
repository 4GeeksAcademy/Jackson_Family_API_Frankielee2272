import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")
# Error Handling
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}")
    return jsonify({"error": "Internal server error"}), 500
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f"Not Found Error: {error}")
    return jsonify({"error": "Resource not found"}), 404
# Sitemap Route
@app.route('/')
def sitemap():
    return generate_sitemap(app)
# Get All Members
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        app.logger.error(f"Failed to retrieve members: {e}")
        return jsonify({"error": "Failed to retrieve members", "message": str(e)}), 500
# Add Member
@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.get_json()
    if not request_body or not all(k in request_body for k in ['id', 'first_name', 'age', 'lucky_numbers']):
        return jsonify({"error": "Missing data, please provide id, first_name, age, and lucky_numbers"}), 400
    member = jackson_family.add_member(request_body)
    return jsonify(member), 201
# Get Member Info
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_info(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
# Delete Member
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)
        if result:
            return jsonify({"message": "Member deleted"}), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    DEBUG_MODE = os.environ.get('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG_MODE)  #app.py