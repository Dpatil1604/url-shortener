import random
import string
from flask import Flask, request, redirect, render_template
from models import db, URLMap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Function to generate random short code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()
        new_url = URLMap(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        return f"Your short URL: http://localhost:5000/{short_code}"
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_original(short_code):
    url_map = URLMap.query.filter_by(short_code=short_code).first()
    if url_map:
        return redirect(url_map.original_url)
    else:
        return "URL not found", 404
if __name__ == '__main__':
    app.run(debug=True)
