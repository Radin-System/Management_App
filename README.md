# Company Management Application

## Overview

This project is a Flask web application designed to manage various aspects of our company. It includes functionality for controlling services like Asterisk and managing some Zabbix operations.

## Goals

- Provide a user-friendly web interface for managing company resources.
- Integrate with Asterisk to control telephony services.
- Interface with Zabbix for monitoring and management tasks.
- Ensure secure and efficient operations within the application.

## Features

- **User Management**: Add, edit, and remove users with various roles and permissions.
- **Asterisk Control**: Manage telephony services, including call routing and monitoring.
- **Zabbix Integration**: View and manage monitoring alerts, system statuses, and performance metrics.
- **Dashboard**: Overview of system status, recent activities, and alerts.

## Dependencies

1. **Install system dependencies for Python and C extensions**
    ```sh
    sudo apt install python3-dev build-essential libssl-dev libjpeg-dev libpng-dev zlib1g-dev libldap2-dev libsasl2-dev libmysqlclient-dev libpq-dev libxml2-dev libxslt1-dev tesseract-ocr tesseract-ocr-eng libtesseract-dev odbcinst unixodbc-dev pkg-config
    ```

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/company-management-app.git
    cd company-management-app
    ```

2. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Change Configs

 Make sure to change the configurations on the config.ini in .configfiles folder after running the app once.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
