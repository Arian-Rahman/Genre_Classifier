from gradio_client import Client

client = Client("soothsayer1221/Music-Genre-Classifier")
result = client.predict(
		lyrics="Hello!!",
		api_name="/predict"
)
print(result)