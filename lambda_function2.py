from datetime import datetime
import json
import boto3

def lambda_handler(event, context):
    try:
        print("Event-Try Block", event)
        
        messages = event
 
        # Initialize S3 client
        s3_client = boto3.client('s3')
        
        # Filter messages where the booking duration is more than 1 day
        filtered_messages = filter_messages(messages)
        
        print("Filtered_messages:", filtered_messages)
        
        # Write the filtered records to the S3 bucket
        write_to_s3(filtered_messages, s3_client)

        # Return a success response
        return {
            'statusCode': 200,
            'body': json.dumps('Filtered records written to S3 bucket successfully!')
        }

    except Exception as e:
        # If any exception occurs, handle it and return an appropriate response
        print("Event-Exception Block", event)
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }


def filter_messages(messages):
    # Filter messages where the booking duration is more than 1 day
    filtered_messages = []
    for message in messages:
        try:
            # Extract relevant fields for filtering and also Convert date strings to datetime objects
            start_date = datetime.strptime(message['startDate'], '%Y-%m-%d')
            end_date   = datetime.strptime(message['endDate'], '%Y-%m-%d')
            
            # Calculate booking duration
            duration = end_date - start_date
            
            # Check if booking duration is more than 1 day
            if duration.days > 1:
                filtered_messages.append(message)
        except Exception as e:
            # If any exception occurs during message filtering, log it and continue to the next message
            print(f"Error filtering message: {str(e)}")
    return filtered_messages


def write_to_s3(records, s3_client):
    try:
        # Write the filtered records to the S3 bucket
        bucket_name = 'airbnb-booking-records-assign4'
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_key = f'filtered_bookings_{current_date}.json'
        
        # If there are no filtered records, do not write anything
        if records:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=json.dumps(records)
            )
            print("Success! filtered records write to S3.")
        else:
            print("No filtered records to write to S3.")
    except Exception as e:
        # If any exception occurs during writing to S3, handle it and log the error
        print(f"Error writing to S3: {str(e)}")
