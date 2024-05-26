import boto3
import tempfile
import os
import streamlit as st

def delete_all_objects(bucket_name):
    # Initialize a session using Amazon S3
    s3 = boto3.client('s3')
    bucket_name = bucket_name
    response = s3.list_objects_v2(Bucket=bucket_name)
    print(response)    

    # List all objects in the bucket
    objects_to_delete = s3.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket is empty
    if 'Contents' in objects_to_delete:
        # Create a list of objects to delete
        delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]

        # Delete all objects
        response = s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': delete_keys,
                'Quiet': True  # Set to False if you want detailed information
            },
            #ExpectedBucketOwner='175573404892'
        )

        print(f"Deleted objects: {response}")
    else:
        print("The bucket is already empty.")

def upload_new_documents(docs,bucketname):             
    for doc in docs:
        # Save the file locally
        temp_dir = tempfile.TemporaryDirectory()
        local_path = os.path.join(temp_dir.name, doc.name)
        with open(local_path, 'wb') as f:
            f.write(doc.read())
        client = boto3.client('s3')
        bucket_name = bucketname
        object_name = doc.name
        response = client.upload_file(local_path, bucket_name, object_name)
        st.success("File(s) uploaded successfully!")

def upload_youtube_transcript():
    client = boto3.client('s3')
    bucket_name = 'knowledgebase-test-rohit'
    file_name='../youtube_transcripts/video-transcript.txt'
    object_name = os.path.basename('../youtube_transcripts/video-transcript.txt')
    response = client.upload_file(file_name, bucket_name, object_name)    

