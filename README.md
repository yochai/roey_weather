Weather Forecast Web Application

This is a simple Python web application that provides weather forecasts by retrieving data from an external API and displaying it on a webpage. 
The application was built for deploy on AWS EC2 as a Docker container using Nginx as a reverse proxy and Gunicorn as the application server.


Project Overview
---------------------
Weather Forecast is a web application that allows users to get up-to-date weather forecasts for their desired locations. The application fetches weather data from an external API and presents it in an easy-to-read format on a webpage. 
It's a convenient tool for users who want to plan their activities based on weather conditions.

Features
---------------------
Location-Based Weather Forecast: Users can enter the name of a city or country to get a weather forecast for that location.
7-Day Weather Forecast: The application provides a 7-day weather forecast, including temperature, humidity, and wind speed.
Dockerized Deployment: The project is containerized using Docker, making it easy to deploy on AWS EC2 or other cloud platforms.
Nginx Reverse Proxy: Nginx serves as a reverse proxy, ensuring efficient handling of incoming HTTP requests and static file serving.
Gunicorn Application Server: Gunicorn serves as the WSGI HTTP server, handling Python application requests.
