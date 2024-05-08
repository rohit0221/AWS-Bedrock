import boto3
import json

llamaModelId = 'meta.llama2-13b-chat-v1' 
prompt = "tell me about Elon musk"

llamaPayload = json.dumps({ 
	'prompt': prompt,
    'max_gen_len': 512,
	'top_p': 0.9,
	'temperature': 0.2
})

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime', 
    region_name='us-east-1'
)
response = bedrock_runtime.invoke_model(
    body=llamaPayload, 
    modelId=llamaModelId, 
    accept='application/json', 
    contentType='application/json'
)
body = response.get('body').read().decode('utf-8')
response_body = json.loads(body)
print(response_body['generation'].strip())