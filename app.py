from flask import Flask, render_template, jsonify

app = Flask(__name__)

# ดาต้าจำลองของเครื่องใช้ไฟฟ้าภายในร้าน odienmall
products_data = [
    {"id": 1, "name": "ตู้เย็น 2 ประตู Inverter", "price": 12900, "category": "ตู้เย็น", "image": "https://images.unsplash.com/photo-1571175432247-5238fd759a55?w=500"},
    {"id": 2, "name": "เครื่องซักผ้าฝาหน้า 10 KG", "price": 18500, "category": "เครื่องซักผ้า", "image": "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=500"},
    {"id": 3, "name": "สมาร์ททีวี 4K Oled 55 นิ้ว", "price": 24900, "category": "ทีวี", "image": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=500"}
]

# 1. หน้าแรกของเว็บ (ดึงข้อมูลสินค้าไปแสดงผล)
@app.route('/')
def index():
    return render_template('index.html', products=products_data)

# 2. API สำหรับให้ TypeScript เรียกดูข้อมูลสินค้า
@app.route('/api/products')
def get_products():
    return jsonify(products_data)

if __name__ == '__main__':
    app.run(debug=True)