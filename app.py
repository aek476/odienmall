from flask import Flask, render_template, jsonify, request
import psycopg2

app = Flask(__name__)

# ฟังก์ชันเชื่อมต่อฐานข้อมูล
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="odienmall_db1",  # ดาต้าเบสที่คุณเอกสร้าง
        user="postgres",
        password="5555500000"  # ⚠️ อย่าลืมเปลี่ยนเป็นรหัสเข้า pgAdmin ของคุณเอกนะคะ
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, price, category, image_url FROM products;')
        rows = cur.fetchall()
        products_data = [{"id": r[0], "name": r[1], "price": float(r[2]), "category": r[3], "image": r[4]} for r in rows]
        cur.close()
        conn.close()
        return render_template('index.html', products=products_data)
    except Exception as e:
        return f"เกิดข้อผิดพลาดในการดึงข้อมูลสินค้า: {e}"

# 🔥 API สำหรับรับออเดอร์จากหน้าบ้านมาบันทึกลง PostgreSQL จริง
@app.route('/api/checkout', methods=['POST'])
def checkout():
    try:
        data = request.get_json()
        cart_items = data.get('items', [])
        total_price = data.get('total_price', 0)
        
        if not cart_items:
            return jsonify({"status": "error", "message": "ไม่มีสินค้าในตะกร้า"}), 400
            
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 1. บันทึกลงตาราง orders เพื่อเอาเลขบิล (order_id)
        cur.execute('INSERT INTO orders (total_price) VALUES (%s) RETURNING order_id;', (total_price,))
        order_id = cur.fetchone()[0]
        
        # 2. วนลูปบันทึกสินค้าแต่ละชิ้นที่อยู่ในตะกร้าลงตาราง order_items
        for item in cart_items:
            cur.execute('''
                INSERT INTO order_items (order_id, product_id, product_name, price, quantity)
                VALUES (%s, %s, %s, %s, %s);
            ''', (order_id, item['id'], item['name'], item['price'], item['quantity']))
            
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "message": f"🎉 บันทึกคำสั่งซื้อเลขที่ {order_id} เข้าฐานข้อมูลสำเร็จแล้วค่ะ!"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)