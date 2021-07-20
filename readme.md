# PizzeriaAPP
Project for self learning purposes, featuring API (FastAPI), containers (Docker), ORM (SQLAlchemy) and database (PostgreSQL) usage. 

Simulates a working pizza place.

__*Work in progress - see development branch*__

## Requirements

- Filled Menu with many positions, names, prices and categories
- Should allow to pick any combination of menu positions
- Should let users pick each position many times
- Total price of a single order should be updated live
- Should store a history of orders

## Entity-Relationship Diagram
![PizzeriaAPP-ERD.png.png](docs/PizzeriaAPP-ERD.png "Simple ERD diagram for a pizza place")

## Skills used
- dockerized a PostgreSQL database
- created a functioning API with FastAPI
- implement basic CRUD functionality
- apply ORM with SQLAlchemy

### Possible improvements
- Prepare a better database that add a relation between main dishes and addons (now theoretically you can pick just an addon from the menu)