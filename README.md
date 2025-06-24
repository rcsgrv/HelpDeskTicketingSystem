# Help Desk Ticketing System

The Help Desk Ticketing System is a lightweight web application built with Flask, SQLAlchemy, SCSS, and HTML. The application enables users to create, view, update, and manage tickets in an organised and efficient way. Designed with responsiveness and usability in mind, the system is suitable for both internal teams and client-facing environments. 

## Features

- Create, view, edit, and delete  tickets
- Secure administration registration and login with password hashing
- Responsive and accessible user interface styled with SCSS and HTML
- Flash alerts for real-time feedback on user actions (success/error)
- Paginated ticket listings with configurable items per page
- Dynamic ticket forms with input validation
- Modular and maintainable codebase using Flask blueprints
- Built-in SQLite database managed via SQLAlchemy ORM (Object Relational Mapper)
- Clean separation of concerns between routes, templates, and stylesheets

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

### Prerequisites

Ensure Python 3 is installed. It is also recommended to use a virtual environment.

To create the virtual environment run the following in the terminal: 

py -m venv venv

To activate the virtual environment run the following in the terminal: 

venv\Scripts\activate

### Repository

Clone the repository which is located at: 

https://github.com/rcsgrv/HelpDeskTicketingSystem.git

### Install Dependencies

To install required packages run the following in the terminal: 

pip install -r requirements.txt

### Running the Application

To start the Flask development server run the following in the terminal: 

py main.py

This will launch the app at http://127.0.0.1:5000/.

Alternatively, the application is currently hosted on Render and can be accessed via the following URL: https://help-desk-ticketing-system-eucm.onrender.com

### Seed Data

When the application is ran for the first time, seed data will be generated. This seed data consists of 10 users and 10 tickets. 

- The first user is an Administrator with the following credentials:
- - Email Address: user1@test.com
- - Password: password1

- The remaining 9 users are Regular Users, following the same pattern:
- - Email: user{n}@test.com
- - Password: password{n}

Where {n} ranges from 2 to 10 (e.g. user2@test.com / password2, user3@test.com / password3, etc.).

### Administrator Registration

To improve security, a 2-step process has been implemented for users wanting to register as Administrators. Upon selecting the Administrator account type on the Registration page, users will be prompted to input an administrator verification code. 

This code has been hardcoded but serves as a proof of concept for this assignment. The code is currently: 

53c17e4d8efdafeddd375e53e4689cc757f1f322ef4595caedc3e85e2fb79c4e

## Testing

The Help Desk Ticketing System includes comprehensive unit tests covering key functionality such as user authentication, ticket creation, viewing, editing, and deletion. These tests use the Pytest framework along with mocking techniques to isolate components and validate behaviour without requiring a live database or full application context.

### Unit Tests
To run the unit tests locally, ensure your virtual environment is activated and dependencies are installed, then run the following in the terminal: 

pytest

This command will discover and run all tests in the `tests/` directory and provide a detailed report of the results.

### Manual Testing
In addition to the unit tests, the application has been thoroughly manually tested to ensure that all user interactions, including registration, login, ticket management, and permissions, function as expected across typical use cases.