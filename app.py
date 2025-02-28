from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicines WHERE name LIKE %s", ('%' + query + '%',))
    medicines = cursor.fetchall()
    conn.close()
    
    return jsonify(medicines)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    data = request.json  # Get JSON data from request
    medicine_list = data.get("medicines", [])

    if not medicine_list:
        return jsonify({"error": "No medicines provided"}), 400

    total = sum(med["price"] * med["quantity"] for med in medicine_list)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert total bill first, then get the generated bill_id
    cursor.execute("INSERT INTO bills (total_amount) VALUES (%s)", (total,))
    bill_id = cursor.lastrowid

    # Insert each medicine into bill_items
    for med in medicine_list:
        cursor.execute("""
            INSERT INTO bill_items (bill_id, medicine_name, quantity, price) 
            VALUES (%s, %s, %s, %s)
        """, (bill_id, med["name"], med["quantity"], med["price"] * med["quantity"]))

    conn.commit()
    conn.close()

    return jsonify({"redirect_url": url_for('bill_page', bill_id=bill_id)})

@app.route('/bill/<int:bill_id>')
def bill_page(bill_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get bill details
    cursor.execute("SELECT * FROM bills WHERE id = %s", (bill_id,))
    bill = cursor.fetchone()

    # Get bill items
    cursor.execute("SELECT * FROM bill_items WHERE bill_id = %s", (bill_id,))
    items = cursor.fetchall()

    conn.close()
    
    return render_template('bill.html', bill=bill, items=items)

if __name__ == '__main__':
    app.run(debug=True)
