# EatExpress
Food delivery service
## Idea
The main idea is to create an API for a food delivery service, similar to UberEats.
# Technological stack
- Django
- Django Rest Framework
- PostgreSQL
- JWT
# Description:
## Requests that do not require a token:
- Register a user<br>
POST /api/v1/auth/user/register
Content-Type: application/json
{
    "username": "username",
    "password": "password",
    "confirm_password": "password",
    "email": "username@gmail.com",
    "first_name": "Name",
    "last_name": "Surname",
    "phone_number": "+123456789",
    "address": "Street, City, Code"
}
- User authorization<br>
POST /api/v1/auth/user/login
Content-Type: application/json
{
    "username": "username",
    "password": "password"
}
- User logout<br>
POST /api/v1/auth/user/logout<br>
Authorization: Bearer your-access-token
## Requests that require a token (Authorization: Bearer your-access-token):
- Retrieve a user profile<br>
GET /api/v1/auth/user/profile/{username}
- Update profile<br>
PUT /api/v1/auth/user/profile/{username}
Content-Type: application/json
{
    "first_name": "Name",
    "last_name": "Surname",
    "phone_number": "+123456789",
    "address": "Street, City, Code",
    "email": "username@gmail.com"
}
- Delete profile<br>
DELETE /api/v1/auth/user/profile/{username}
- Retrieve Restaurant Menu<br>
GET api/v1/restaurant/menu
- Retrieve a list of user orders<br>
GET api/v1/delivery/orders
- Create a new order<br>
POST api/v1/delivery/orders
- Retrieve detailed information for order<br>
Content-Type: application/json
{
    "dishes": [
        {
            "dish_id": 4,
            "quantity": 2
        },
        {
            "dish_id": 3,
            "quantity": 1
        }
    ],
    "delivery_address": "new address"
    "payment_method": "credit_card"
}
GET api/v1/delivery/orders/{id}
## Developer
Baranetskyi Sviatoslav

Email: svyatoslav.baranetskiy738@gmail.com
