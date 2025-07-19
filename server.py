from flask import Flask, render_template, send_from_directory
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stocks.json')
def stocks():
    return send_from_directory('static', 'stocks.json')

if __name__ == '__main__':
    app.run(debug=True)
