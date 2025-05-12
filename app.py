from flask import Flask, render_template, request
import tiktoken

app = Flask(__name__)

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
        except ValueError:
            # Treat as plain text
            tokens = encoder.encode(input_text)
            result = {
                'type': 'text',
                'input': input_text,
                'output': tokens,
                'decoded': encoder.decode(tokens)
            }

    return render_template('index.html', result=result, user_input=input_text)

if __name__ == '__main__':
    app.run(debug=True)
