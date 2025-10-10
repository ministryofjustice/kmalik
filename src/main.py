import boto3
import os
from datetime import datetime

# === CONFIGURATION ===
BUCKET_NAME = 'alpha-everyone'
OBJECT_KEY = 'kmalik-justice-digital/test/airflow/my-file.txt' 
REGION_NAME = 'eu-west-1' 

db_name = os.environ.get("DB_NAME")
if db_name:
    print(f"DB name is: {db_name}")
else:
    print("DB name not provided.")

# === INITIATE S3 CLIENT ===
s3 = boto3.client(
    's3'
    )

# === STEP 1: READ EXISTING FILE CONTENT ===
response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
original_content = response['Body'].read().decode('utf-8')

print("Original Content:")
print(original_content)

# === STEP 2: APPEND VERIFIABLE CONTENT ===
current_time = datetime.isoformat()
verification_number = 123456789

user_name = os.getenv("SECRET_USERNAME")

new_line = f"\nAppended on {current_time} - Verification Code: {verification_number} with user name of {user_name}"
updated_content = original_content + new_line

# === STEP 3: WRITE BACK TO S3 ===
s3.put_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY, Body=updated_content.encode('utf-8'))
print("\nContent written back to S3.")

# === STEP 4: VALIDATE WRITE ===
verify_response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
verify_content = verify_response['Body'].read().decode('utf-8')

if new_line.strip() in verify_content:
    print("\n✅ Content successfully verified in file.")
else:
    print("\n❌ Verification failed.")