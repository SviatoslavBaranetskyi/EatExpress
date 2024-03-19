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
POST /api/v1/auth/user/register<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"username": "username",<br>
&nbsp;&nbsp;&nbsp;"password": "password",<br>
&nbsp;&nbsp;&nbsp;"confirm_password": "password",<br>
&nbsp;&nbsp;&nbsp;"email": "username@gmail.com",<br>
&nbsp;&nbsp;&nbsp;"first_name": "Name",<br>
&nbsp;&nbsp;&nbsp;"last_name": "Surname",<br>
&nbsp;&nbsp;&nbsp;"phone_number": "+123456789",<br>
&nbsp;&nbsp;&nbsp;"address": "Street, City, Code"<br>
}
- User authorization<br>
POST /api/v1/auth/user/login<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"username": "username",<br>
&nbsp;&nbsp;&nbsp;"password": "password"<br>
}
- User logout<br>
POST /api/v1/auth/user/logout<br>
Authorization: Bearer your-access-token
## Requests that require a token (Authorization: Bearer your-access-token):
- Retrieve a user profile<br>
GET /api/v1/auth/user/profile/{username}
- Update profile<br>
PUT /api/v1/auth/user/profile/{username}<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"first_name": "Name",<br>
&nbsp;&nbsp;&nbsp;"last_name": "Surname",<br>
&nbsp;&nbsp;&nbsp;"phone_number": "+123456789",<br>
&nbsp;&nbsp;&nbsp;"address": "Street, City, Code",<br>
&nbsp;&nbsp;&nbsp;"email": "username@gmail.com"<br>
}
- Delete profile<br>
DELETE /api/v1/auth/user/profile/{username}
- Retrieve Restaurant Menu<br>
GET api/v1/restaurant/menu
- Retrieve a list of user orders<br>
GET api/v1/delivery/orders
- Create a new order<br>
POST api/v1/delivery/orders
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"dishes": [<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"dish_id": 4,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"quantity": 2<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"dish_id": 3,<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"quantity": 1<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>
&nbsp;&nbsp;&nbsp;],<br>
&nbsp;&nbsp;&nbsp;"delivery_address": "new address"<br>
&nbsp;&nbsp;&nbsp;"payment_method": "credit_card"<br>
}<br>
- Retrieve detailed information for order<br>
GET api/v1/delivery/orders/{id}
## Developer
Baranetskyi Sviatoslav

Email: svyatoslav.baranetskiy738@gmail.com
