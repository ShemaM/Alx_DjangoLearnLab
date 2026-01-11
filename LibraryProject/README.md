# Introduction to Django: LibraryProject

Welcome to the **LibraryProject**. This project is designed to provide hands-on experience with Django, one of the most popular web frameworks for building robust, scalable web applications. Throughout this project, I will set up a Django development environment, learn about Django models and ORM, and explore the powerful Django admin interface.

## 🎯 Objectives

* **Set Up Django Development Environment:** Install Django, create a project, and familiarize with the default structure and development server.
* **Implementing Django Models:** Create a Django app, define models with specific attributes, and perform CRUD operations using the Django ORM.
* **Utilizing the Django Admin Interface:** Register models and customize the interface to enhance data management and visibility.

---

## 🛠 Project Progress & Tasks

### Task 0: Introduction to Django Development Environment Setup (Mandatory)

**Objective:** Gain familiarity with Django by setting up a development environment and creating a basic project.

#### Steps Taken:

1. **Environment Setup:**
    * Ensured Python is installed.
    * Created an isolated environment: `python -m venv .venv`.
    * Activated the environment: `.\.venv\Scripts\activate`.
    * Installed Django: `pip install django`.

2. **Project Creation:**
    * Created the project structure: `django-admin startproject LibraryProject .`.

3. **Running the Server:**
    * Navigated into the project directory.
    * Launched the development server: `python manage.py runserver`.
    * Verified the installation via [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 📂 Project Structure Overview

Understanding the roles of the core components:

* **`manage.py`**: A command-line utility that lets you interact with this Django project (e.g., running the server or syncing the database).

* **`LibraryProject/settings.py`**: The primary configuration file for the project, including database settings and app registrations.

* **`LibraryProject/urls.py`**: The "table of contents" for the site; it handles URL declarations and routing.

* **`LibraryProject/wsgi.py` / `asgi.py`**: Entry points for web servers to serve the project.

---
*This project provides a solid foundation in Django, preparing for the development of complex, data-driven web applications.* 
