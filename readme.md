# PizzeriaAPP
Project for self learning purposes - featuring: API (FastAPI), containers (Docker), ORM (SQLAlchemy), raw SQL and database (PostgreSQL) usage. 

Simulates a working pizza place.

## Requirements

- Filled Menu with many positions, names, prices and categories
- Should allow to pick any combination of menu positions
- Should let users pick each position many times
- Total price of a single order should be updated live
- Should store a history of orders

## Entity-Relationship Diagram
![PizzeriaAPP-ERD.png.png](docs/PizzeriaAPP-ERD.png "Simple ERD diagram for a pizza place")

## Skills used
- dockerized PostgreSQL database and APP
- created a functioning API with FastAPI
- implemented CRUD functionality
- applied ORM with SQLAlchemy and raw SQL (and an option to select which one to use)
- prepared end2end RestAPI tests collection in Postman (and an additional simpler version to use with pytest)

### Possible improvements
- Prepare a better database that add a relation between main dishes and addons (now theoretically you can pick just an addon from the menu)
- provide a way to store history of orders and ordereditems (even for items that are deleted such as menu positions)
