from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
        return render_template('11-3mqtt.html')

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080)

