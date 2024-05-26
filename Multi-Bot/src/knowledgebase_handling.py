import boto3


def update_knowledgebase(knowledgebaseid,datasourceid):
    bedrock_client = boto3.client('bedrock-agent')
    response = bedrock_client.start_ingestion_job(
    clientToken="rrtyerter67dg6ghju6rgkkkn35j35jjh5445545y4ghhh",
    dataSourceId=datasourceid,
    description="test",
    knowledgeBaseId=knowledgebaseid
)

