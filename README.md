# Contribution Management App

## Table of Contents
- [Contribution Management App](#contribution-management-app)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Running Tests](#running-tests)
  - [Screenshots](#screenshots)
  - [Continuous Integration](#continuous-integration)
  - [API Integration](#api-integration)
    - [Mpesa Callback URL](#mpesa-callback-url)
    - [SMS Notifications](#sms-notifications)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Overview

The Contribution Management App is designed to manage contributions among members in a group. It facilitates case management, transaction recording, and payment processing via Mpesa, along with SMS notifications for members.

## Features

- **Member Management**: Add, update, and delete member information.
- **Case Management**: Create, update, and track contribution cases.
- **Transaction Handling**: Record all transactions, including payments and penalties.
- **Mpesa Integration**: Handle offline payments through Safaricom's C2B API.
- **SMS Notifications**: Notify members of updates and payment confirmations using Africa's Talking API.
- **Unit Testing**: Comprehensive tests for edge cases and functionality.
- **Automatic Penalty Deduction**: Automatically deduct penalties from a member's account when an invoice's due date passes without payment.

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

### Setup

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

4. **Register an Account on Africa's Talking**:
   Visit [Africa's Talking](https://africastalking.com/) to create an account. You'll need to obtain your API credentials, including the username and API key, which are essential for configuring your application.

5. **Register an Account on Safaricom's Developer Portal**:
   Go to the [Safaricom Developer Portal](https://developer.safaricom.co.ke/) and sign up for an account. After registering, you'll receive credentials, including the API key and secret, required for integrating Mpesa services.

6. **Environment Configuration**:
   - Create a `.env` file in the root directory of your Django project.
   - Add the following credentials to your `.env` file:

     ```bash
      # Django settings
      SECRET_KEY= # Your Django secret key (used for cryptographic operations like signing cookies)

      # Africa's Talking API credentials
      AFRICA_TALKING_USERNAME= # Your Africa's Talking username (provided during account creation)
      AFRICA_TALKING_API_KEY= # Your Africa's Talking API key (used for authenticating API requests)
      AFRICA_TALKING_API_URL=https://api.sandbox.africastalking.com/version1/messaging # Base URL for the Africa's Talking messaging API (sandbox URL for testing)

      # Mpesa settings
      MPESA_ENV=sandbox # Environment mode: 'sandbox' for testing, 'production' for live transactions
      MPESA_CONSUMER_KEY= # Your Mpesa consumer key (provided by Safaricom for accessing the API)
      MPESA_CONSUMER_SECRET= # Your Mpesa consumer secret (provided by Safaricom for accessing the API)
      MPESA_SHORTCODE= # Your Mpesa shortcode (assigned by Safaricom to handle payments)
      CONFIRMATION_URL=yourdomain.com/mpesa/confirmation/ # URL for receiving payment confirmation (to be handled by your server)
      VALIDATION_URL=yourdomain.com/mpesa/validation/ # URL for receiving payment validation (to be handled by your server)

     ```

7. **Set up the database**:
   - Create a PostgreSQL database and update the `settings.py` with your database configuration.

8. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

9. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

10. **Register URLs**:
    To register the Validation and Confirmation URLs with M-Pesa, run the following command:

    ```bash
    python manage.py register_urls
    ```

    **Note**:
    - **Sandbox Environment**: You can register and update your URLs as needed. Feel free to overwrite existing URLs if necessary.
    - **Production Environment**: URL registration is a one-time process. If you need to change your URLs, you must delete the existing ones from the URL Management tab under Self-Service and then re-register using the `register_urls` command. For further assistance, you can also contact support at [apisupport@safaricom.co.ke](mailto:apisupport@safaricom.co.ke).

    After running the command, if the URLs are successfully registered, you will see a byte string similar to this in your terminal:

    ```bash
    b'{"OriginatorCoversationID": "7619-37765134-1", "ResponseCode": "0", "ResponseDescription": "success"}'
    ```

    This indicates that the URLs have been registered successfully.

11. **Configure the Cron Job for Automatic Penalty Deduction**:
    - Open the crontab editor on your server:
      ```bash
      crontab -e
      ```
    - Add the following line to run the command daily at midnight:
      ```bash
      0 0 * * * /bin/bash -c 'source /path/to/your/virtualenv/bin/activate && cd /path/to/your/project && python manage.py apply_penalties'
      ```
      Explanation:
      - `/bin/bash -c` ensures the command is run in a shell.
      - `source /path/to/your/virtualenv/bin/activate` activates your virtual environment.
      - `cd /path/to/your/project` navigates to your project directory.
      - `python manage.py apply_penalties` runs the Django management command to apply penalties.

12. **Run the server**:
    ```bash
    python manage.py runserver
    ```

## Running Tests

To run tests, use the following command:
```bash
python manage.py test
```

## Screenshots

<details>
  <summary>Click to view screenshots</summary>

  ![Screenshot 2025-01-19 181803](https://github.com/user-attachments/assets/6b9ce82a-af09-4d34-bd1e-d7b1a974ea7f)
  ![Screenshot 2025-01-19 181132](https://github.com/user-attachments/assets/d4471948-3e7a-4664-9548-da9e04b7927d)
  ![Screenshot 2025-01-19 181218](https://github.com/user-attachments/assets/417dcdd3-9353-4589-ba0e-7cecbc7de97d)
  ![Screenshot 2025-01-19 181635](https://github.com/user-attachments/assets/8c06fa9e-fee3-4183-8f26-60184b6f1bed)
  ![Screenshot 2025-01-19 181652](https://github.com/user-attachments/assets/3949164d-41f5-43fd-86d1-92c8cc58888f)
  ![Screenshot 2025-01-19 181711](https://github.com/user-attachments/assets/395ce5c1-bd67-4c98-bcb9-fc3c18673fcd)
  ![Screenshot 2025-01-19 181731](https://github.com/user-attachments/assets/28ad7385-2363-490f-8d62-0b4780e7887d)
  ![Screenshot 2025-01-19 181839](https://github.com/user-attachments/assets/2387d5be-87e7-4a1f-b9b9-e107e633065e)
  ![Screenshot 2025-01-19 181912](https://github.com/user-attachments/assets/3dc4cba0-2cc7-412c-9b42-191df4142e22)

</details>

## Continuous Integration

This project uses GitHub Actions for continuous integration. The tests will automatically run on every push or pull request to the `main` branch.

## API Integration

### Mpesa Callback URL

The app will handle incoming payment notifications from Mpesa through the Callback URL.

### SMS Notifications

The app has SMS sending logic handled using Africa's Talking API.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any improvements or suggestions.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Africa's Talking](https://africastalking.com/)
- [Safaricom Mpesa](https://developer.safaricom.co.ke/docs)
