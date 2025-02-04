from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import json

app = Flask(__name__)

def get_tehran_time():
    tehran_tz = pytz.timezone('Asia/Tehran')
    return datetime.now(tehran_tz).strftime("%Y-%m-%d %H:%M:%S")

# برای تست سریع، یک مسیر ساده می‌سازیم
@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Car Price API is running',
        'timestamp': get_tehran_time()
    })

@app.route('/api/cars')
def get_cars():
    try:
        url = "https://mashinbank.com/%D9%82%DB%8C%D9%85%D8%AA-%D8%AE%D9%88%D8%AF%D8%B1%D9%88"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # برای بررسی خطاهای HTTP
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # برای دیباگ
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        cars = []
        car_items = soup.find_all('div', class_='vehicle-price-item')
        
        # اگر هیچ خودرویی پیدا نشد، از داده‌های نمونه استفاده می‌کنیم
        if not car_items:
            # داده‌های نمونه برای تست
            sample_data = [
                {
                    'title': 'پژو 206 تیپ 2',
                    'model': '206',
                    'type': 'تیپ 2',
                    'year': '1402',
                    'price': '۵۸۰,۰۰۰,۰۰۰ تومان',
                    'price_change': '۰.۰۰٪'
                },
                # اضافه کردن داده‌های نمونه از متن شما
                {
                    'title': 'دنا پلاس',
                    'model': 'دنا',
                    'type': 'پلاس',
                    'year': '1402',
                    'price': '۷۵۰,۰۰۰,۰۰۰ تومان',
                    'price_change': '۰.۰۰٪'
                }
            ]
            return jsonify({
                'status': 'success',
                'data': sample_data,
                'timestamp': get_tehran_time(),
                'note': 'Using sample data'
            })
        
        for item in car_items:
            try:
                name = item.find('h2', class_='vehicle-name')
                price = item.find('div', class_='vehicle-price')
                details = item.find('div', class_='vehicle-details')
                
                cars.append({
                    'title': name.text.strip() if name else '',
                    'price': price.text.strip() if price else 'نامشخص',
                    'year': details.find('span', class_='year').text.strip() if details else '',
                    'update_time': get_tehran_time()
                })
            except Exception as e:
                print(f"Error parsing car: {e}")
                continue
        
        return jsonify({
            'status': 'success',
            'data': cars,
            'timestamp': get_tehran_time()
        })
        
    except Exception as e:
        print(f"Error in get_cars: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': get_tehran_time()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
