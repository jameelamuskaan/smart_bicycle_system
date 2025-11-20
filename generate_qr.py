# ...existing code...
import qrcode
import os

os.makedirs("static/qr", exist_ok=True)

# DB uses bike_ids 101..145 mapped to QR strings BIKE-QR-001..BIKE-QR-045
start_db_id = 101
count = 45

for i in range(1, count + 1):
    db_id = start_db_id + (i - 1)          # 101..145
    qr_code_str = f"BIKE-QR-{i:03d}"       # BIKE-QR-001 .. BIKE-QR-045
    img = qrcode.make(qr_code_str)
    img_path = os.path.join("static", "qr", f"{qr_code_str}.png")
    img.save(img_path)
    print(f"✅ Generated: {img_path} for bike_id={db_id} qr='{qr_code_str}'")

print("\n🎉 All QR codes generated!")
# ...existing code...
