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
- PostgreSQL
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

## Setup

1. **Register an Account on Africa's Talking:**

   Visit [Africa's Talking](https://africastalking.com/) to create an account. You'll need to obtain your API credentials, including the username and API key, which are essential for configuring your application.

2. **Register an Account on Safaricom's Developer Portal:**

   Go to the [Safaricom Developer Portal](https://developer.safaricom.co.ke/) and sign up for an account. After registering, you'll receive credentials, including the API key and secret, required for integrating Mpesa services.

These credentials will be used for configuring your application.

1. **Environment Configuration:**
   - Create a `.env` file in the root directory of your Flask project.
   - Add the following credentials to your `.env` file:

     ```bash
     # Django settings
     SECRET_KEY= #Your django secret_key

     # Africa's Talking API credentials
     AFRICA_TALKING_USERNAME= #your_username
     AFRICA_TALKING_API_KEY= #your_api_key

     # Mpesa settings
     MPESA_ENV= # sandbox or live
     MPESA_CONSUMER_KEY= # your mpesa consumer key
     MPESA_CONSUMER_SECRET= # your mpesa consumer secret
     MPESA_SHORTCODE= # your short code (Business Number)
     CONFIRMATION_URL= # yourdomain.com/mpesa/confirmation/
     VALIDATION_URL= # yourdomain.com/mpesa/validation/

     ```

## Register URLs

To register the Validation and Confirmation URLs with M-Pesa, run the following command:

```bash
python manage.py register_urls
```

**Note:**

- **Sandbox Environment:** You can register and update your URLs as needed. Feel free to overwrite existing URLs if necessary.

- **Production Environment:** URL registration is a one-time process. If you need to change your URLs, you must delete the existing ones from the URL Management tab under Self-Service and then re-register using the `register_urls` command. For further assistance, you can also contact support at [apisupport@safaricom.co.ke](mailto:apisupport@safaricom.co.ke).

After running the command, if the URLs are successfully registered, you will see a byte string similar to this in your terminal:

```bash
b'{"OriginatorCoversationID": "7619-37765134-1", "ResponseCode": "0", "ResponseDescription": "success"}'
```

This indicates that the URLs have been registered successfully.


## Running Tests

To run tests, use the following command:
```bash
python run_tests.py
```


## Continuous Integration

This project uses GitHub Actions for continuous integration. The tests will automatically run on every push or pull request to the `main` branch.

## API Integration

### Mpesa Callback URL

The app will handle incoming payment notifications from Mpesa through the Callback URL.

### SMS Notifications

The app has sms sending logic handled using Africa's Talking API.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or suggestions.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Africa's Talking](https://africastalking.com/)
- [Safaricom Mpesa](https://developer.safaricom.co.ke/docs)
