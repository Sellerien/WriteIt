## WriteIt

This project is a blog platform where users can create posts, leave comments, and filter posts by categories. It includes a search system for posts by keywords, a registration and authentication system via username or email, password reset functionality, and an admin panel for content management.

## Technologies:
- Python 3.13
- Django 5.1
- PostgreSQL
- HTML/CSS
- Unittest
- Git

## Installation:
In the terminal:
1. Create and activate a virtual environment::  
  python -m venv venv   
  source venv/bin/activate  # для Linux/Mac  
  venv\Scripts\activate     # для Windows

2. Clone the repository:
  git clone https://github.com/Sellerien/WriteIt.git

3. Navigate to the project directory: cd ~/writeit/

4. Install requirements: 
  cd writeit/  
  pip install -r requirements.txt

6. Apply database migrations:
  python manage.py migrate

7. Run the server:  
  python manage.py runserver

Open http://127.0.0.1:8000/ in your browser to see the project in action.

To create super-user: python manage.py createsuperuser

