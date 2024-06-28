# SnapScene
SnapScene is a vibrant social media platform where you can share your moments, discover stunning photos from around the world, and connect with fellow photography enthusiasts. Capture, share, and explore with SnapScene, your new favorite photo-sharing community.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [License](#license)

## Features

- User authentication and profile management
- Create, update, and delete posts
- Comment on posts
- Like and unlike posts
- Responsive design for mobile and desktop

## Requirements

- Docker
- Docker Compose

## Installation
1. Clone the repository:
````
git clone https://github.com/Kali2114/SnapScene
cd snapscene
````
2. Create a .env file in the root directory of the project based on the .env.example file and add the necessary environment variables:
````
cp .env.example .env
````
Then, edit the .env file to set the appropriate values:
````
DB_HOST=db
DB_NAME=snapscene
DB_USER=your_db_user
DB_PASS=your_db_password
````
3. Build and start the Docker containers:
````
docker-compose up --build
````

## Running the Application
After running the docker-compose up --build command, the application will be accessible at 
````
http://localhost:8000
````
The application consists of two main services defined in the docker-compose.yml file:
````
app: The Django application service
db: The PostgreSQL database service
````
## Docker Compose Services

* app: The Django application service - This service handles the Django application, including building the Docker image, exposing the necessary ports, mounting volumes, and defining the startup commands.
* db: The PostgreSQL database service - This service handles the PostgreSQL database, including the Docker image configuration, volume mounting, and setting environment variables for the database.

## Environment Variables
The application uses the following environment variables, which should be defined in the .env file:
* DB_HOST: The database host (default: db)
* DB_NAME: The name of the database (default: snapscene)
* DB_USER: The database user (default: your_db_user)
* DB_PASS: The database password (default: your_db_password)

## License
This project is licensed under the GNU General Public License. See the LICENSE file for more information.


