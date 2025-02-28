from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_mysql_connection

app = Flask(__name__)

# Home Route - Display medicines
@app.route('/')
def home():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch all medicines from database
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', medicines=medicines)

# Route to add a new medicine
@app.route('/add_med', methods=['POST'])
def add_med():
    name = request.form.get('name')
    price = request.form.get('price')

    if not name or not price:
        return jsonify({"error": "Please provide medicine name and price"}), 400

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO medicines (name, price) VALUES (%s, %s)"
        cursor.execute(query, (name, price))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to edit a medicine
@app.route('/edit_med/<int:id>', methods=['POST'])
def edit_med(id):
    name = request.form.get('name')
    price = request.form.get('price')

    if not name or not price:
        return jsonify({"error": "Please provide medicines name and price"}), 400

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        query = "UPDATE medicines SET name=%s, price=%s WHERE id=%s"
        cursor.execute(query, (name, price, id))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete a medicine
@app.route('/delete_med/<int:id>', methods=['POST'])
def delete_med(id):
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        query = "DELETE FROM medicines WHERE id=%s"
        cursor.execute(query, (id,))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
