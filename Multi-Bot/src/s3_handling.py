import boto3

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



