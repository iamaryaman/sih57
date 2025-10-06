from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="WY76zpcdPLMzBWcvWzoP"
)

# Absolute path to the image file
result = client.run_workflow(
    workspace_name="lol-iaho2",
    workflow_id="optical-character-model",
    images={"image": r"C:\Users\Aryaman\Desktop\hackathon\SIH57\images\Screenshot 2025-05-25 234110.png"},
    use_cache=True
)

print(result)
print(type(result[0]))
