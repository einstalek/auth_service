Flask Authorization Microservice

Provides simple register and login forms with validation. Stores 
user data in sqlite database. 

To create database, type in python shell:
1. from flask_auth import db
2. db.create_all()

This will create auth.db file inside project directory