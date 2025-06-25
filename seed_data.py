from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")  # या Atlas URI
db = client["ecommerce"]
products_collection = db["products"]
users_collection = db["users"]

products = [
    {'id': 1, 'name': 'Mobile Phone', 'price': 12000, 'description': 'Smartphone with 4GB RAM', 'image': 'mobile.jpg'},
    {'id': 2, 'name': 'Laptop', 'price': 45000, 'description': '15 inch laptop with SSD', 'image': 'laptop.jpg'},
    {'id': 3, 'name': 'Headp hones', 'price': 1500, 'description': 'Noise cancelling headphones', 'image': 'headphones.jpg'},
    {'id': 4, 'name': 'Smart watch', 'price': 3500, 'description': 'Fitness tracking smartwatch', 'image': 'smartwatch.jpg'},
    {'id': 5, 'name': 'Bluetooth Speaker', 'price': 2000, 'description': 'Portable Bluetooth speaker', 'image': 'speaker.jpg'},
    {'id': 6, 'name': 'Wireless Mouse', 'price': 800, 'description': 'Ergonomic wireless mouse', 'image': 'mouse.jpg'},
    {'id': 7, 'name': 'Tablet', 'price': 15000, 'description': '10-inch tablet', 'image': 'tablet.jpg'},
    {'id': 8, 'name': 'Gaming Keyboard', 'price': 2500, 'description': 'RGB mechanical keyboard', 'image': 'keyboard.jpg'},
    {'id': 9, 'name': 'Power Bank', 'price': 1200, 'description': '10000mAh power bank', 'image': 'powerbank.jpg'},
    {'id': 10, 'name': 'Smart TV', 'price': 32000, 'description': '40 inch Android TV', 'image': 'tv.jpg'},
    {'id': 11, 'name': 'Gaming Console', 'price': 28000, 'description': '4K gaming console', 'image': 'console.jpg'},
    {'id': 12, 'name': 'Camera', 'price': 25000, 'description': 'DSLR camera', 'image': 'camera.jpg'},
    {'id': 13, 'name': 'Drone', 'price': 18000, 'description': '4K drone with GPS', 'image': 'drone.jpg'},
    {'id': 14, 'name': 'Printer', 'price': 6500, 'description': 'Wireless printer', 'image': 'printer.jpg'},
    {'id': 15, 'name': 'Router', 'price': 1600, 'description': 'High-speed router', 'image': 'router.jpg'},
    {'id': 16, 'name': 'External Hard Drive', 'price': 5000, 'description': '1TB HDD', 'image': 'harddrive.jpg'},
    {'id': 17, 'name': 'Refrigerator', 'price': 28000, 'description': 'Double Door 300L Fridge', 'image': 'fridge.jpg'},
    {'id': 18, 'name': 'Washing Machine', 'price': 19000, 'description': 'Front Load 6kg Washer', 'image': 'washing.jpg'},
    {'id': 19, 'name': 'Air Conditioner', 'price': 32000, 'description': '1.5 Ton Inverter AC', 'image': 'ac.jpg'},
    {'id': 20, 'name': 'Microwave Oven', 'price': 7500, 'description': 'Convection Microwave 25L', 'image': 'microwave.jpg'},
    {'id': 21, 'name': 'Ceiling Fan', 'price': 1800, 'description': 'Energy Saving 1200mm Fan', 'image': 'fan.jpg'},
    {'id': 22, 'name': 'Smart Light Bulb', 'price': 1200, 'description': 'Wi-Fi RGB LED Bulb', 'image': 'smartbulb.jpg'},
    {'id': 23, 'name': 'Portable AC', 'price': 27000, 'description': '1 Ton Portable Air Conditioner', 'image': 'portableac.jpg'},
    {'id': 24, 'name': 'Hair Dryer', 'price': 900, 'description': '1200W Compact Dryer', 'image': 'hairdryer.jpg'},
    {'id': 25, 'name': 'Electric Kettle', 'price': 1100, 'description': '1.5L Stainless Steel Kettle', 'image': 'kettle.jpg'},
    {'id': 26, 'name': 'Air Purifier', 'price': 10500, 'description': 'HEPA Filter Air Purifier', 'image': 'purifier.jpg'},
    {'id': 27, 'name': 'Fitness Band', 'price': 2500, 'description': 'Waterproof Smart Band', 'image': 'fitnessband.jpg'},
    {'id': 28, 'name': 'VR Headset', 'price': 4500, 'description': 'Virtual Reality Headset', 'image': 'vr.jpg'},
    {'id': 29, 'name': 'Smart Door Lock', 'price': 8500, 'description': 'Biometric + Keypad Lock', 'image': 'doorlock.jpg'},
    {'id': 30, 'name': 'LED Desk Lamp', 'price': 1300, 'description': 'USB Rechargeable Study Lamp', 'image': 'desklamp.jpg'},
    {'id': 31, 'name': 'Gaming Chair', 'price': 9500, 'description': 'Ergonomic Adjustable Chair', 'image': 'chair.jpg'},
    {'id': 32, 'name': 'Typewriter', 'price': 3700, 'description': 'RGB Blue Switch Keyboard', 'image': 'mechkeyboard.jpg'},
    {'id': 33, 'name': 'Monitor 24-inch', 'price': 11500, 'description': 'Full HD LED Monitor', 'image': 'monitor.jpg'},
    {'id': 34, 'name': 'Wireless Charger', 'price': 2000, 'description': 'Fast Charging Pad', 'image': 'wirelesscharger.jpg'},
    {'id': 35, 'name': 'Electric Toothbrush', 'price': 2200, 'description': 'Rechargeable with Timer', 'image': 'toothbrush.jpg'},
    {'id': 36, 'name': 'Steam Iron', 'price': 1700, 'description': 'Non-stick Soleplate Steam Iron', 'image': 'iron.jpg'}
]

users = [{'username': 'admin', 'email': 'admin@example.com', 'password': 'admin123'}]

products_collection.delete_many({})
products_collection.insert_many(products)

users_collection.delete_many({})
users_collection.insert_many(users)

print("Products and Users inserted successfully!")



