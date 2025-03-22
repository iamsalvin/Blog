# Django Mini Blog

A modern blogging platform built with Django featuring a glassmorphism UI, dark/light mode toggle, PDF download functionality, and audio narration for blog posts.

## Features

- Responsive design with glassmorphism UI elements
- Dark/light mode toggle with preference saving
- User authentication (register, login, profile)
- Create, edit, and delete blog posts
- Comment system
- PDF download functionality for blog posts
- Audio narration of blog content using Google Text-to-Speech
- Category-based post organization
- Search functionality

## Tech Stack

- Django 4.2+
- PostgreSQL (production) / SQLite (development)
- Bootstrap 5
- HTML/CSS/JavaScript
- WhiteNoise for static files
- Gunicorn for production deployment

## Deployment on Render

This application is configured for easy deployment on Render.

### Setup Instructions

1. Create a new Web Service on Render
2. Connect to this GitHub repository
3. Use the following settings:
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn blog_project.wsgi:application`
4. Add the following environment variables:
   - `SECRET_KEY`: A secure random string
   - `PYTHON_VERSION`: 3.10.0 (or your preferred version)
5. Create a PostgreSQL database on Render
6. Add the database connection URL as `DATABASE_URL` environment variable

## Local Development

To set up the project for local development:

```bash
# Clone the repository
git clone https://github.com/iamsalvin/Blog.git
cd Blog

# Create and activate a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the site in action.

## License

This project is open-sourced under the MIT license.
