
# UAV Rental App

UAV Rental App is a Django web application for renting unmanned aerial vehicles (UAVs). It allows users to browse available UAVs, make rental requests, and manage their rentals. This README provides instructions for installing, running, and using the application.

This project is made as a case study for Baykar Interview.
## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [API Guide](#api-guide)
- [Admin Panel Guide](#admin-panel-guide)

## Features

Following functionality was requested:
functionality
- Membership and Login Screen 
  - Login screen and signup screens are implemented

- For the UAV to be rented; Add, Delete, Update, List, Rent
  - New UAVs can be added by admin user on the admin panel. They will show on the list in home page.
- UAV Features: Brand, Model, Weight, Category etc.
  - Brand, Model, Weight, Category fields are added to UAV Model
- Members' UAV rental records
  -  After logging in, user can see active rentals in their profile tab.
  - Unactive rentals can be seen in admin panel.

- For the leased UAV; Deleting, Updating, a Rental
  - User can change the dates and return a Rental through their profile

- Rental Features: UAV, Date and Time Ranges, Renting Member etc.
    - Rental model includes UAV and the User models, and the start and end dates of the rental

- Filtering and searching features in the table for all Listing pages
  - Listing pages have search and ordering features added

Following extras are also implemented:

- Restarting the project with docker
- Well-crafted documentation and comment lines
- Unit testing
- Using datatable for listing pages
- Keeping relational tables separately
- Front-End Bootstrap, Jquery features

## Installation

### With Docker

1. Make sure Docker is installed.
2. Navigate to the project directory:

   ```bash
   cd uav-rental-app
   ```
3. Build container
    ```bash
   docker-compose build
   ```
4. Run the container
    ```bash
   docker-compose up -d
   ```
5. Make the migrations and create a superuser
    ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate 
   docker-compose exec web python manage.py createsuperuser 
    ```


### Without Docker
1. Clone the repository:

   ```bash
   git clone https://github.com/dgkngk/uav-rental-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd uav-rental-app
   ```

3. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:
   
   - Ensure you have PostgreSQL installed and running on your system.
   - Create a PostgreSQL database for the application.
   - Update the database settings in `settings.py` to point to your PostgreSQL database.

5. Apply migrations to create database schema:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Running the Application

1. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

2. Open your web browser and navigate to [http://localhost:8000](http://localhost:8000) to access the application.

## Endpoints

- **Login:** `/login/`
  - Use a saved username and password to login

- **Logout:** `/logout/`
  - Logs the user out and redirects to login page
- **Signup:** `/signup/`
  - Username and password registration
- **Home:** `/home/` or `/`
  - Homepage includes the rental list of UAVs
- **Profile:** `/profile/`
  - Profile includes the list of rental records and update options
- **Admin:** `/admin/`
  - Admin panel can be used to add and edit UAVs, Users or Rental records.

## API Guide

- **Login API:** `/api/login/`
  - Returns a auth token when correct username and password is provided as form-data.
- **Logout API:** `/api/logout/`
  - Deletes the auth token
- **Signup API:** `/api/signup/`
  - 
- **UAV List API:** `/api/uavs-json/` or `api/uavs-json\`
  - Returns the not rented uavs as a json list.

## Admin Panel Guide

1. Navigate to the admin panel:

   - Open your web browser and go to [http://localhost:8000/admin/](http://localhost:8000/admin/)
   - Log in using your admin credentials.

2. Use the admin panel to:

   - Add, edit, or delete UAVs and Rentals.
   - Manage user accounts.
   - Monitor application data and activities.

