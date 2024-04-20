from flask import Flask, render_template

app = Flask(__name__)

# Define the routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
