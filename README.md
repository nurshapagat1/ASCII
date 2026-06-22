ASCII

A web application that converts uploaded images into ASCII art.

---


About

ASCII is a web application that allows users to transform images into ASCII art.

Users can create an account, upload images, generate ASCII versions of their pictures, and save their creations locally or online.

The application provides user authentication, image uploading, project management, and an image processing system that converts visual content into text-based artwork.

This project was created as a practice project to explore authentication systems, file handling, image processing, and full-stack web development.

---

Features

User Authentication

- User registration
- Login and logout
- User account management
- Secure authentication system

Image to ASCII Conversion

- Upload images
- Convert images into ASCII art
- Generate text-based artwork from images
- Preview generated ASCII output

Project Management

- Create personal projects
- Save generated ASCII artworks
- Store projects locally
- Manage previously created projects

User Experience

- Simple and clean interface
- Responsive design
- Easy image conversion workflow

---

Tech Stack

Backend

- Python
- Django

Database

- SQLite / PostgreSQL

Frontend

- HTML5
- CSS3
- JavaScript

Tools

- Git
- GitHub

Deployment

- Coming soon

---

Installation

Follow these steps to run the project locally.

---

1. Clone the repository

git clone https://github.com/nurshapagat1/ASCII.git

Go to the project folder:

cd ASCII

---

2. Create a virtual environment

Create a virtual environment:

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

---

3. Install dependencies

Install all required packages:

pip install -r requirements.txt

---

4. Configure environment variables

Create a ".env" file in the project root:

SECRET_KEY=your_secret_key
DEBUG=True

Add database configuration if needed:

DATABASE_NAME=ascii_db
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

---

5. Apply migrations

Run database migrations:

python manage.py makemigrations

python manage.py migrate

---

6. Create an admin user

Create a superuser:

python manage.py createsuperuser

Enter:

- Username
- Email
- Password

---

7. Run the application

Start the development server:

python manage.py runserver

Open your browser:

http://127.0.0.1:8000/

---

Usage

1. Register a new account
2. Login to your profile
3. Upload an image
4. Convert the image into ASCII art
5. Save your generated artwork
6. Access your previous projects anytime

---

Future Improvements

- Download ASCII art as an image or text file
- Add different ASCII styles
- Improve image conversion quality
- Add real-time preview
- Add cloud storage
- Add project sharing
- Create API for ASCII conversion
- Docker deployment
---
License

This project was created for educational purposes only.

