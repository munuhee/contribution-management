# Contribution Management App

## Overview

The Contribution Management App is designed to manage contributions among members in a group. It facilitates case management, transaction recording, and payment processing via Mpesa, along with SMS notifications for members.

## Features

- **Member Management**: Add, update, and delete member information.
- **Case Management**: Create, update, and track contribution cases.
- **Transaction Handling**: Record all transactions, including payments and penalties.
- **Mpesa Integration**: Handle offline payments through Safaricom's C2B API.
- **SMS Notifications**: Notify members of updates and payment confirmations using Africa's Talking API.
- **Unit Testing**: Comprehensive tests for edge cases and functionality.

## Technologies Used

- Python
- Django
- PostgreSQL (or any preferred database)
- Africa's Talking API
- Safaricom's Mpesa Daraja API
- Docker (optional for containerization)

## Installation

### Prerequisites

- Python 3.12
- pip
- PostgreSQL

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/munuhee/contribution-management-app.git
   cd contribution-management-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   - Create a PostgreSQL database and update the `settings.py` with your database configuration.

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## Running Tests

To run tests, use the following command:
```bash
python manage.py test
```

You can also use `pytest` for additional testing features:
```bash
pytest
```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The tests will automatically run on every push or pull request to the `main` branch.

## API Integration

### Mpesa Callback URL

Ensure to set up the callback URL in the Safaricom API settings. The app will handle incoming payment notifications from Mpesa through this URL.

### SMS Notifications

Configure Africa's Talking API credentials in your settings to enable SMS notifications.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or suggestions.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Africa's Talking](https://africastalking.com/)
- [Safaricom Mpesa](https://developer.safaricom.co.ke/docs)
