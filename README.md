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
- User authorization<br>
POST /api/v1/auth/user/login
- User logout<br>
POST /api/v1/auth/user/logout<br>
Authorization: Bearer your-access-token
## Requests that require a token (Authorization: Bearer your-access-token):
- Retrieve Profile<br>
GET /api/v1/auth/user/profile/{username}
- Update Profile<br>
PUT /api/v1/auth/user/profile/{username}
- Delete Profile<br>
DELETE /api/v1/auth/user/profile/{username}
- Retrieve Restaurant Menu<br>
GET api/v1/restaurant/menu
- Retrieve a list of user orders<br>
GET api/v1/delivery/orders
- Create a new order<br>
POST api/v1/delivery/orders
- Retrieve detailed information for order<br>
GET api/v1/delivery/orders/{id}
## Developer
Baranetskyi Sviatoslav

Email: svyatoslav.baranetskiy738@gmail.com
