from flask import Flask, request
import gensim

app = Flask(__name__)

model = gensim.models.Word2Vec.load("./model")
reference_pair = ("full", "empty")

html_form_with_message = '''
<!DOCTYPE html>
<html>
<head>
<title>Text Echo App</title>
</head>
<body>
    <h2>Enter a word to find its opposite</h2>
    <h3>(Try: long, cold, night)
    <form method="post" action="/">
        <label for="text">Word:</label><br>
        <input type="text" name="my_input_value"><br><br>
        <input type="submit" value="Find Opposite Pairing">
    </form>
     <style>
        body {
            background-color: turquoise;
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }
    </style>
    <p>DATA</p>
</body>
</html>
'''

def calculation(target_word):
    result_vector = model.wv[target_word] - model.wv[reference_pair[0]] + model.wv[reference_pair[1]]
    opposite_words = model.wv.similar_by_vector(result_vector, topn=2)
    return opposite_words[1][0]

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = ''
    calculated_value = ''
    if request.method == 'POST':
        user_input = request.form['my_input_value'].lower()
        calculated_value = calculation(user_input)

    display_text = calculated_value
    return html_form_with_message.replace("DATA", display_text)

app.run()
