# Airport Service API

## Overview
**Airport Service** is an application that allows you to conveniently order tickets for travel,
view the history of your orders and receive up-to-date information about flights and routes. 
For administrative staff, it is possible not only to create orders, but also to manage data: 
create, edit and eliminate irrelevant data , thus ensuring the accuracy and relevance of information
in the system.

## Features
- JWT authenticated
- Admin panel `/admin/`
- Documentation is located at `api/schema/swagger-ui/` or `api/schema/redoc/`
- Managing orders and tickets
- Filtering *airplanes, airplane types, airports, routes, flights, crews, tickets, orders*
- Registration and login using an **email** instead of a **username**
- All endpoints are covered by **tests**
- A simple user can only view data and create ticket orders
- The admin can manipulate, delete, edit and create data from the endpoint
- Additional fields that show which seats are occupied and how many free seats are available in *flight endpoint*
- It is forbidden to delete in endpoints: *route, order, flight, ticket*

# DB Structure
![DB Structure](media/photo_for_readme_md/DB_structure.png)

# Installing
- Install PostgresSQL and create db 
- Create .env and put your variable like in the env_example

# Run with Docker
Docker should be installed
- `docker-compose build`
- `docker-compose up`


# Getting access
- **Create user:** `api/user/register/`
- **Get access token:** `api/user/token/`