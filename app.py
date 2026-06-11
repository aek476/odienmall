from flask import Flask, render_template, jsonify
import psycopg2

app = Flask(__name__)

# ฟังก์ชันสำหรับเชื่อมต่อฐานข้อมูล PostgreSQL ของ odienmall
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="odienmall_db1",  # ใช้ชื่อดาต้าเบสที่คุณเอกสร้างใน pgAdmin
        user="postgres",           # ยูสเซอร์หลักของ PostgreSQL
        password="5555500000"  # ⚠️ อย่าลืมเปลี่ยนเป็นรหัสผ่านจริงของคุณเอกนะคะ
    )
    return conn

@app.route('/')
def index():
    try:
        # เปิดการเชื่อมต่อฐานข้อมูล
        conn = get_db_connection()
        cur = conn.cursor()
        
        # เขียนคำสั่ง SQL ดึงข้อมูลสินค้าออกมาทั้งหมด
        cur.execute('SELECT id, name, price, category, image_url FROM products;')
        rows = cur.fetchall()
        
        # แปลงข้อมูลให้อยู่ในรูปแบบที่หน้าเว็บเข้าใจ
        products_data = []
        for row in rows:
            products_data.append({
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "category": row[3],
                "image": row[4]
            })
            
        # ปิดการเชื่อมต่อ
        cur.close()
        conn.close()
        
        # ส่งข้อมูลไปแสดงผลที่หน้าจอเว็บ
        return render_template('index.html', products=products_data)
        
    except Exception as e:
        # หากเชื่อมต่อไม่สำเร็จ จะแสดงข้อความเตือน Error บนหน้าเว็บ
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {e}"

if __name__ == '__main__':
    app.run(debug=True)