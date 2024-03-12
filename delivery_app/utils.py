import requests


def get_dish_details(dish_id):
    response = requests.get(f"http://127.0.0.1:8000/api/v1/menu/{dish_id}/")
    dish_data = response.json()
    return dish_data.get('name', ''), dish_data.get('price', 0)
