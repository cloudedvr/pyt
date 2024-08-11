from flask import Flask, render_template_string, request
from random import seed, choice

app = Flask(__name__)

class SerialGenerator:
    def __init__(self, start=0):
        self.start = start
        self.next = start

    def generate(self):
        self.next += 1
        return self.next - 1

    def reset(self):
        self.next = self.start

class WordFinder:
    def __init__(self, path):
        file = open(path, 'r')
        self.words = self.parse(file)
        file.close()

    def parse(self, file):
        return [word.strip() for word in file]

    def random(self):
        return choice(self.words)

class SpecialWordFinder(WordFinder):
    def parse(self, file):
        return [word.strip() for word in file 
                if word.strip() and not word.startswith('#')]

# Sample data for demonstration; normally, this would be read from a file
WORDS = """cat
dog
porcupine
"""
SPECIAL_WORDS = """# Veggies
kale
parsnips

# Fruits
apple
mango
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE)

@app.route('/generate_serial', methods=['POST'])
def generate_serial():
    start = int(request.form['start'])
    serial_gen = SerialGenerator(start=start)
    generated_number = serial_gen.generate()
    return render_template_string(TEMPLATE, generated_number=generated_number, start=start)

@app.route('/reset_serial', methods=['POST'])
def reset_serial():
    start = int(request.form['start'])
    serial_gen = SerialGenerator(start=start)
    serial_gen.reset()
    return render_template_string(TEMPLATE, generated_number=serial_gen.generate(), start=start)

@app.route('/random_word', methods=['POST'])
def random_word():
    wf = WordFinder(WORDS.splitlines())
    random_word = wf.random()
    return render_template_string(TEMPLATE, random_word=random_word)

@app.route('/special_random_word', methods=['POST'])
def special_random_word():
    swf = SpecialWordFinder(SPECIAL_WORDS.splitlines())
    random_word = swf.random()
    return render_template_string(TEMPLATE, special_random_word=random_word)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python OOP Web</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        h1 {
            color: #333;
        }

        h2 {
            color: #555;
        }

        div {
            margin-bottom: 20px;
        }

        label {
            margin-right: 10px;
        }

        input[type="number"] {
            width: 100px;
        }

        button {
            padding: 5px 10px;
            margin-top: 10px;
        }

        p {
            color: #007BFF;
        }
    </style>
</head>
<body>
    <h1>Python OOP Web Demo</h1>
    
    <div>
        <h2>Serial Generator</h2>
        <form action="/generate_serial" method="POST">
            <label for="start">Start Number:</label>
            <input type="number" id="start" name="start" required>
            <button type="submit">Generate Serial</button>
        </form>
        {% if generated_number is not none %}
            <p>Generated Serial Number: {{ generated_number }}</p>
        {% endif %}
        <form action="/reset_serial" method="POST">
            <input type="hidden" name="start" value="{{ start }}">
            <button type="submit">Reset Serial</button>
        </form>
    </div>

    <div>
        <h2>Random Word Finder</h2>
        <form action="/random_word" method="POST">
            <button type="submit">Get Random Word</button>
        </form>
        {% if random_word is not none %}
            <p>Random Word: {{ random_word }}</p>
        {% endif %}
    </div>

    <div>
        <h2>Special Random Word Finder</h2>
        <form action="/special_random_word" method="POST">
            <button type="submit">Get Special Random Word</button>
        </form>
        {% if special_random_word is not none %}
            <p>Special Random Word: {{ special_random_word }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
