# Help Desk Ticketing System

The Help Desk Ticketing System is a lightweight, full-featured web application built with Flask, SQLAlchemy, SCSS, and HTML. It enables users to create, view, update, and manage  tickets in an organised and efficient way. Designed with responsiveness and usability in mind, the system is suitable for both internal teams and client-facing environments. 

## Features

- Create, view, edit, and delete help desk tickets
- Secure administration registration and login with password hashing
- Responsive and accessible user interface styled with SCSS and HTML
- Flash alerts for real-time feedback on user actions (success/error)
- Paginated ticket listings with configurable items per page
- Dynamic ticket forms with input validation
- Modular and maintainable codebase using Flask blueprints
- Built-in SQLite database managed via SQLAlchemy ORM
- Clean separation of concerns between routes (`views/`), templates, and stylesheets

## Technologies Used

- **Python 3** with **Flask**
- **SQLAlchemy** ORM with **SQLite**
- **SCSS** for modular and maintainable styling
- **Jinja2** templating engine
- **HTML5**

## Database
The system uses SQLAlchemy for ORM and SQLite as the default local database. 

## Architecture

This project follows the Model-View-Controller (MVC) design pattern:

- **Model**: Managed by SQLAlchemy in the `models/` directory, handling database schema and interactions.
- **View**: HTML templates rendered using Jinja2, located in the `templates/` directory.
- **Controller**: Flask route logic located in the `views/` directory, managing requests, input validation, and responses.

This separation of concerns ensures modularity, scalability, and ease of maintenance.

## Getting Started

## Prerequisites

Ensure Python 3 is installed. It is also recommended to use a virtual environment:

1) To create the virtual environment run the following in the terminal: py -m venv venv
2) To activate the virtual environment run the following in the terminal: venv\Scripts\activate

## Repository

Clone the repository which is located at: https://github.com/rcsgrv/HelpDeskTicketingSystem.git

## Install Dependencies

Install required packages:

pip install -r requirements.txt

## Running the Application

To start the Flask development server, run:

py main.py

This will launch the app at http://127.0.0.1:5000/.

Alternatively, the application is currently hosted on Render and can be accessed via the following URL: https://help-desk-ticketing-system-eucm.onrender.com

## Administrator Access

To improve security, a 2-step process has been implemented for users wanting to register as Administrators. Upon selecting the Administrator account type on the Registration page, users will be prompted to input an administrator verification code. 

This code has been hardcoded but serves as a proof of concept for this assignment. The code is currently: 53c17e4d8efdafeddd375e53e4689cc757f1f322ef4595caedc3e85e2fb79c4e

## Project Structure

┣ 📂HelpDeskTicketingSystem
┃ ┣ 📂models
┃ ┃ ┣ 📜TicketModel.py
┃ ┃ ┗ 📜UserModel.py
┃ ┣ 📂static
┃ ┃ ┣ 📜_variables.scss
┃ ┃ ┣ 📜main.css
┃ ┃ ┣ 📜main.css.map
┃ ┃ ┗ 📜main.scss
┃ ┣ 📂templates
┃ ┃ ┣ 📜admin_code.html
┃ ┃ ┣ 📜base.html
┃ ┃ ┣ 📜create_ticket.html
┃ ┃ ┣ 📜edit_ticket.html
┃ ┃ ┣ 📜home.html
┃ ┃ ┣ 📜login.html
┃ ┃ ┣ 📜profile.html
┃ ┃ ┣ 📜register.html
┃ ┃ ┗ 📜ticket_details.html
┃ ┣ 📂utils
┃ ┃ ┗ 📜ticket_helper.py
┃ ┣ 📂views
┃ ┃ ┣ 📜auth.py
┃ ┃ ┣ 📜home.py
┃ ┃ ┣ 📜tickets.py
┃ ┃ ┗ 📜users.py
┃ ┣ 📜__init__.py
┃ ┣ 📜extensions.py
┃ ┗ 📜seed_data.py
┣ 📂instance
┃ ┗ 📜helpdeskticketingsystem.db
┣ 📜config.py
┣ 📜main.py
┣ 📜README.md
┗ 📜requirements.txt