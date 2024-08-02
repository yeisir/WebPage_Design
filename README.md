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
   
   ```sh
   pip3 install -r requirements.txt

## Usage

Page 1: Displays data received from the UDP server.
Page 2: Provides additional options for managing the data.

## AWS Deployment Details

EC2 Instance: The application is hosted on an AWS EC2 instance.
RDS Database: Uses an AWS RDS MySQL instance for data storage.

# Note

Hope this helps :)

