import random

import requests
from flask import Flask, render_template, request, session

from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'secret_key'

load_dotenv()
api_key = os.getenv("API_KEY")
print(api_key)

base_url = "http://api.weatherapi.com/v1"

world_cities = [
    "Delhi", "Shanghai", "Sao Paulo", "Mumbai", "Beijing", "Cairo", "Dhaka",
    "Mexico City", "Osaka", "Karachi", "Chongqing", "Istanbul", "Lahore",
    "Buenos Aires", "Kinshasa", "Cairo", "Lima", "London", "Bangkok",
    "New York", "Chengdu", "Nanjing", "Ho Chi Minh City", "Baghdad",
    "Hong Kong", "Lahore", "Bangalore", "Kolkata", "Tehran", "Rio de Janeiro",
    "Shenzhen", "Wuhan", "Los Angeles", "Lima", "Kinshasa", "Bangkok",
    "Santiago", "Hyderabad", "Dallas", "Bogota", "Riyadh", "Belo Horizonte",
    "Madrid", "Houston", "Ahmedabad", "Barcelona", "Toronto",
    "Washington, D.C.", "Boston", "Miami"
]

japan_cities = [
    "Sapporo", "Aomori", "Morioka", "Sendai", "Akita", "Yamagata", "Fukushima",
    "Mito", "Utsunomiya", "Maebashi", "Saitama", "Chiba", "Tokyo", "Yokohama",
    "Niigata", "Toyama", "Kanazawa", "Fukui", "Nagano", "Gifu", "Shizuoka",
    "Nagoya", "Kyoto", "Osaka", "Kobe", "Nara", "Wakayama", "Tottori",
    "Shimane", "Okayama", "Hiroshima", "Yamaguchi", "Tokushima", "Takamatsu",
    "Matsuyama", "Kochi", "Fukuoka", "Saga", "Nagasaki", "Kumamoto", "Oita",
    "Miyazaki", "Kagoshima", "Naha"
]

random_world_cities = random.choice(world_cities)


@app.route('/')
def index():
  return render_template("index.html")


@app.route("/get_japan_cities", methods=['POST'])
def get_japan_cities():
  selected_city = request.form.get("japan_cities")
  endpoint = f"{base_url}/current.json?key={api_key}&q={selected_city}&aqi=no"
  response = requests.get(endpoint)

  if response.status_code == 200:
    weather_data = response.json()
    session['selected_city_temp_c'] = f"{weather_data['current']['temp_c']} ℃"
    session['selected_city'] = selected_city

  return render_template(
      "index.html",
      selected_city=session.get('selected_city'),
      selected_city_temp_c=session.get('selected_city_temp_c'),
      random_city=session.get('random_city'),
      random_city_temp_c=session.get('random_city_temp_c'))


@app.route("/get_random_cities", methods=['POST'])
def get_random_cities():
  random_city = random.choice(world_cities)
  endpoint = f"{base_url}/current.json?key={api_key}&q={random_city}&aqi=no"
  response = requests.get(endpoint)

  if response.status_code == 200:
    weather_data = response.json()
    session['random_city_temp_c'] = f"{weather_data['current']['temp_c']} ℃"
    session['random_city'] = random_city

  return render_template(
      "index.html",
      selected_city=session.get('selected_city'),
      selected_city_temp_c=session.get('selected_city_temp_c'),
      random_city=session.get('random_city'),
      random_city_temp_c=session.get('random_city_temp_c'))


@app.route("/guess_high", methods=['POST'])
def guess_high():
  if session.get('selected_city_temp_c') and session.get('random_city_temp_c'):
    if  session['selected_city_temp_c'] > session['random_city_temp_c']:
      result = "正解!"
    else:
      result = "不正解..."
    return render_template("index.html", result=result)
  else:
    return "エラー: 必要なデータがありません"


@app.route("/guess_low", methods=['POST'])
def guess_low():
  if session.get('selected_city_temp_c') and session.get('random_city_temp_c'):
    if  session['selected_city_temp_c'] > session['random_city_temp_c']:
      result = "正解!"
    else:
      result = "不正解..."
    return render_template("index.html", result=result, show=True)
  else:
    return "エラー: 必要なデータがありません"

if __name__ == "__main__":
  app.run(host='localhost', port=(5000))
