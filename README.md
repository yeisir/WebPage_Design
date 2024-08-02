# WebPage_Design

This repository contains a set of applications and scripts designed to interact with each other and provide a web interface for data visualization.

## Project Structure

The project is divided into several main components:

1. **UDP Server**: A UDP server that receives data from an external source and processes it.
2. **Sniffer**: A component that sends data to the UDP server and forwards it to a Flask server.
3. **Flask Server**: A web server that receives data from the sniffer and provides an interface to interact with the data.
4. **Page Templates**:
   - `pag1.html`: A template for the first page of the web interface.
   - `pag2.html`: A template for the second page of the web interface.

## Deployment

This project was deployed on an AWS EC2 instance and uses an AWS RDS MySQL database for data storage.

## Requirements

Make sure you have the following installed:

- Python 3.x
- MySQL server (for local development) or access to AWS RDS MySQL

## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:yeisir/WebPage_Design.git
2. Navigate to the project directory:
   ```sh
    cd WebPage_Design
4. Install the required Python:
   ```sh
   pip3 install -r requirements.txt
5. Configure the 'flask_app.py' file with your AWS RDS MySQL database credentials.
6. Run the UDP server and data processing scripts:
   ```sh
    python3 udp_server.py
    python3 sn_data.py
8. Start the Flask application:
   ```sh
    python3 flask_app.py
10. Access the web interface by navigating to http://<YOUR_EC2_PUBLIC_IP>:<PORT> in your web browser.

## Usage

Page 1: Displays data received from the UDP server.
Page 2: Provides additional options for managing the data.

## AWS Deployment Details

EC2 Instance: The application is hosted on an AWS EC2 instance.
RDS Database: Uses an AWS RDS MySQL instance for data storage.

# Note

Feel free to adjust any details as needed. I hope this helps, and if you have any questions, don't hesitate to contact me :)

