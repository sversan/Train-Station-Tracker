from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_data(query):
    connection = sqlite3.connect('train_data.db')
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<category>')
def category_view(category):
    query_mapping = {
        "good_condition": "SELECT name FROM stations WHERE condition='Good'",
        "needs_reconditioning": "SELECT name FROM stations WHERE condition='Needs Reconditioning'",
        "needs_replacement": "SELECT name FROM train_lines WHERE status='Needs Replacement'",
        "needs_rebuilding": "SELECT name FROM train_lines WHERE status='Needs Rebuilding'",
        "tourism_guide": "SELECT station, attraction FROM tourism_guide"
    }
   
    data = get_data(query_mapping.get(category, ""))
    return render_template('category.html', category=category, data=data)

@app.route('/submit', methods=['POST'])
def submit():
    station_name = request.form['station_name']
    condition = request.form['condition']
   
    connection = sqlite3.connect('train_data.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO stations (name, condition) VALUES (?, ?)", (station_name, condition))
    connection.commit()
    connection.close()
   
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

# Database Setup
connection = sqlite3.connect('train_data.db')
cursor = connection.cursor()

# Create stations table
cursor.execute('''CREATE TABLE IF NOT EXISTS stations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    condition TEXT NOT NULL)''')

# Create train lines table
cursor.execute('''CREATE TABLE IF NOT EXISTS train_lines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL)''')

# Create tourism guide table
cursor.execute('''CREATE TABLE IF NOT EXISTS tourism_guide (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    station TEXT NOT NULL,
                    attraction TEXT NOT NULL)''')

connection.commit()
connection.close()