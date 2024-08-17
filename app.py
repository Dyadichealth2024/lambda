from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from botocore.exceptions import ClientError
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure AWS credentials
boto3.setup_default_session(
    aws_access_key_id='fakeAccessKeyId',
    aws_secret_access_key='fakeSecretAccessKey',
    region_name='us-west-2'
)

# Configure DynamoDB
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = dynamodb.Table('Users')

@app.route('/register', methods=['POST'])
def register():
    logging.debug("Received request: %s", request.data)
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    company_name = data.get('companyName')
    email = data.get('email')
    password = data.get('password')  # Ideally, hash the password before storing it

    try:
        table.put_item(
            Item={
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'companyName': company_name,
                'password': password,
            }
        )
        logging.debug("User registered successfully: %s", data)
        return jsonify({"message": "User registered successfully"}), 200
    except ClientError as e:
        logging.error("Error registering user: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
