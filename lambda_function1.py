#Create Producer Lambda Function - Python Code
import json
import random
import uuid
import boto3

def lambda_handler(event, context):
    # Initialize SQS client
    sqs_client = boto3.client('sqs')
    
    # Define the SQS queue URL
    queue_url = 'https://sqs.ap-south-1.amazonaws.com/767397926411/AirbnbBookingQueue'  
    
    # Generate mock Airbnb booking data
    mock_data = generate_mock_data()
    
    print(mock_data)
    
    """body = json.dumps(mock_data)
    print("body : ",mock_data)
    """
    
    # Publish each mock booking data to the SQS queue
    for booking in mock_data:
        # Send message to SQS queue
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(booking)
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Mock Airbnb booking data published successfully to the queue!')
    }

def generate_mock_data():
    # Generate mock Airbnb booking data
    mock_data = []
    cities = ['New York', 'Los Angeles', 'London', 'Paris', 'Tokyo']
    countries = ['USA', 'UK', 'France', 'Japan']
    
    for _ in range(10):  # Generate 10 mock booking records
        booking = {
            "bookingId"    : random.randint(1000,9999),
            "userId"       : random.randint(1000,9999),
            "propertyId"   : random.randint(1000,9999),
            "Location"     : f"{random.choice(cities)}, {random.choice(countries)}",
            "startDate"    : "2023-12-01",
            "endDate"      : "2023-12-05",
            "Price"        : round(random.uniform(50, 500), 2)
        }
        mock_data.append(booking)
    
    return mock_data
