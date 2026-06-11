public checkout(): void {
        if (this.items.length === 0) {
            alert('ตะกร้าของคุณยังว่างเปล่าอยู่ค่ะ!');
            return;
        }

        let totalPrice = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        // ยิง Fetch API ส่งข้อมูลสินค้าในตะกร้าข้ามไปหาหน้าบ้าน Flask
        fetch('/api/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                items: this.items,
                total_price: totalPrice
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message); // จะเด้งกล่องข้อความบอกเลขบิลสั่งซื้อที่ดึงมาจากฐานข้อมูลจริงค่ะ
                this.items = [];
                this.render();
                
                // สั่งปิดหน้าต่างตะกร้าสินค้าอัตโนมัติ
                const modalEl = document.getElementById('cartModal');
                if (modalEl) {
                    const modal = (window as any).bootstrap.Modal.getInstance(modalEl);
                    if (modal) modal.hide();
                }
            } else {
                alert('เกิดข้อผิดพลาด: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }