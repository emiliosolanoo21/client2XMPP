# XMPP Client with Flask and Slixmpp

## Overview

This project is a simple XMPP client developed using Flask and Slixmpp. It includes a user-friendly interface for user registration and login, with session management and error handling. The primary purpose of this client is to allow users to communicate using the XMPP protocol after logging in with their credentials.

## Features

- *User Registration*: Users can create an account with a username and password. A successful registration redirects the user back to the login page.
- *User Login*: Registered users can log in with their credentials. The login form expects the username in the format yourname@alumchat.lol.
- *Session Management*: After logging in, users can start using the XMPP client for messaging.
- *Error Handling*: Flash messages are used to inform the user about registration and login errors.
- *Responsive Design*: The interface is built using Bootstrap, ensuring a responsive and intuitive user experience.

## Installation

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Steps

1. Clone the repository:

``` 
git clone https://github.com/emiliosolanoo21/xmpp-client.git
cd xmpp-client
```

2. Create and activate a virtual environment:

```
python -m venv env
source env/bin/activate   
# On Windows use `env\Scripts\activate`
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Run the Flask application:

```
flask run
```

5. Open your web browser and navigate to http://127.0.0.1:5000 to access the application.

## Folder Structure

```
|-- app/
|   |-- __init__.py
|   |-- routes.py
|   |-- xmpp_client.py
|-- templates/
|   |-- base.html
|   |-- login.html
|   |-- register.html
|-- static/
|   |-- css/
|       |-- style.css
|-- requirements.txt
|-- README.md
|-- run.py
```

## Dependencies

The application relies on the following Python packages, which are listed in requirements.txt:

- Flask
- Slixmpp
- Jinja2
- Bootstrap (included via CDN)

## Future Improvements

- Add functionality for sending and receiving XMPP messages.
- Implement chat history storage and retrieval.
- Improve error handling with more specific feedback for users.