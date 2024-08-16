import json

def calculate_lung_health(age, gender, pulse, breathHoldTime):
    pulse = float(pulse)
    breathHoldTime = float(breathHoldTime)
    score = (breathHoldTime / pulse) * 100
    return score

def main(event, context):
    try:
        body = json.loads(event['body'])
        age = body.get('age')
        gender = body.get('gender')
        pulse = body.get('pulse')
        breathHoldTime = body.get('breathHoldTime')

        if None in (age, gender, pulse, breathHoldTime):
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": json.dumps({"error": "Invalid input"})
            }

        score = calculate_lung_health(age, gender, pulse, breathHoldTime)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"score": score})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({"error": "Internal server error"})
        }
