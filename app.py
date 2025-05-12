from flask import Flask, render_template, request
from pymongo import MongoClient
import tiktoken

app = Flask(__name__)

# Initialize MongoDB Client and Database
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI if using MongoDB Atlas
db = client['text_to_Token']
collection = db['data']

# Load encoder
encoder = tiktoken.encoding_for_model('gpt-4o')

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_text = ""

    if request.method == 'POST':
        input_text = request.form['user_input']
        try:
            # Try decoding token IDs
            token_list = [int(x.strip()) for x in input_text.split(",")]
            decoded = encoder.decode(token_list)
            result = {
                'type': 'tokens',
                'input': token_list,
                'output': decoded
            }
            
            # Store the result in MongoDB
            collection.insert_one({
                "input_text": input_text,
                "type": "tokens",
                "tokens": token_list,
                "decoded_text": decoded
            })
            
        except ValueError:
            # Treat as plain text
            tokens = encoder.encode(input_text)
            decoded = encoder.decode(tokens)
            result = {
                'type': 'text',
                'input': input_text,
                'output': tokens,
                'decoded': decoded
            }
            
            # Store the result in MongoDB
            collection.insert_one({
                "input_text": input_text,
                "type": "text",
                "tokens": tokens,
                "decoded_text": decoded
            })

    return render_template('index.html', result=result, user_input=input_text)

if __name__ == '__main__':
    app.run(debug=True)
