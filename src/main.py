import boto3
from datetime import datetime

# === CONFIGURATION ===
BUCKET_NAME = 'alpha-everyone'
OBJECT_KEY = 'kmalik-justice-digital/test/airflow/my-file.txt' 
REGION_NAME = 'eu-west-1' 

# === INITIATE STS CLIENT ===
# client_sts = boto3.client('sts')
# response = client_sts.get_session_token(
#     DurationSeconds=3600
# )

# === INITIATE S3 CLIENT ===
s3 = boto3.client(
    's3'
    # region_name=REGION_NAME,
    # aws_access_key_id=response["Credentials"]["AccessKeyId"],
    # aws_secret_access_key=["Credentials"]["SecretAccessKey"],
    # aws_session_token=["Credentials"]["SessionToken"]
    )

# === STEP 1: READ EXISTING FILE CONTENT ===
response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
original_content = response['Body'].read().decode('utf-8')

print("Original Content:")
print(original_content)

# === STEP 2: APPEND VERIFIABLE CONTENT ===
current_time = datetime.utcnow().isoformat()
verification_number = 123456789

new_line = f"\nAppended on {current_time} - Verification Code: {verification_number}"
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