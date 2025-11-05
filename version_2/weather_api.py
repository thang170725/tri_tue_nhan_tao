import requests

def get_weather(city_name="Hà Nội"):
    API_KEY = "a3502bbb398c639df116db612b1cdf2a"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},vn&appid={API_KEY}&units=metric&lang=vi"
    
    response = requests.get(url)
    if response.status_code != 200:
        return None, "Không thể lấy dữ liệu thời tiết."
    
    data = response.json()
    
    # Lấy các trường chính
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    
    # Ghép câu trả lời
    weather_text = f"Nhiệt độ hôm nay ở {city_name} là {temp} độ C, độ ẩm {humidity} phần trăm, trời {desc}."
    return data, weather_text
