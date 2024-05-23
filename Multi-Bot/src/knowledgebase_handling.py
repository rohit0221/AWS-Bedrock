import boto3


def update_knowledgebase(knowledgebase):
    bedrock_client = boto3.client('bedrock-agent')
    response = bedrock_client.start_ingestion_job(
    clientToken="rrtyerter67dg6ghju6rn35j35jjh5445545y4ghhh",
    dataSourceId="PTWW3VAMWH",
    description="test",
    knowledgeBaseId="ROEZ7VMG8N"
)

