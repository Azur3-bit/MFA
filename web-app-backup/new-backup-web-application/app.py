from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html template

@app.route('/buy_shoe', methods=['POST'])
def buy_shoe():
    try:
        # Run the Tkinter application to process the purchase
        subprocess.Popen(["python", "your_tkinter_app.py"])
        return jsonify({"status": "success", "message": "Shoe purchased successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
