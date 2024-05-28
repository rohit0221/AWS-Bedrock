AWS boto configs:

C:\Users\<user>\.aws\credentials
[default]
aws_access_key_id=
aws_secret_access_key=

# Development Setup

## Create Buckets

Create 3 buckets and store them in envs:
BUCKET_RAG="bedrock-bucket-docubot"
BUCKET_HEALTH="bedrock-bucket-health"
BUCKET_FINANCE="bedrock-bucket-finance"


## Create knowledge sources

knowledge-base-docubot
knowledge-base-health
knowledge-base-finance
knowledge-base-youtube

## Create datasource in each

datasource-docubot
datasource-health
datasource-finance
datasource-youtube

## Link S3 buckets to these datasources

## Configure Vector Database

Embed English by Cohere
Choose pinecone
Provide Endpoint URL e.g.
https://vectordb-finance-sohrk74.svc.aped-4627-b74a.pinecone.io

Provide Credentials secret ARN: get from secrets manager

Text field name: text
Bedrock-managed metadata field name: metadata


Create knowledge base button
## Choose a vector store (done in parallel)

vectordb-docubot
vectordb-health
vectordb-finance
vectordb-youtube



## Create a vector store (done in parallel)
Go to Pinecone
Create new Index
1) Put Name
2) Choose Dimension 1024 and Metric cosine

Create new API key:
Name: default
Key : Store this key value -> to be used in secrets manager later



## Create a new secret in AWS secrets manager (done in parallel)
Secret name: pinecone


Secret key: apiKey
Secret value: ad7f0f17-ccc3-4d8c-bd9d-c20471cb95d4