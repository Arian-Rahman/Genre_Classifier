from flask import Flask, render_template, request
import requests
from gradio_client import Client


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['text']

        output = predict_genre(input_text)
        confidence_list = output.get('confidences', [])
        labels = [elem['label'] for elem in confidence_list if elem['confidence'] > 0.5]

        label_text = ", ".join(labels) if labels else "No genres detected."

        print(label_text)
        return render_template('index.html', result=label_text)
    else:
        return render_template('index.html')
    
    

def predict_genre(text):
    client = Client("soothsayer1221/Music-Genre-Classifier")
    result = client.predict(
		lyrics="Hello!!",
		api_name="/predict"
    )
    return result
    

if __name__ == '__main__':
    app.run(debug=True)

