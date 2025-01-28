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
  - [Screenshots](#screenshots)
  - [API Integration](#api-integration)
    - [Mpesa Callback URL](#mpesa-callback-url)
    - [SMS Notifications](#sms-notifications)

## Overview

The Contribution Management App is designed to manage contributions among members in a group. It facilitates case management, transaction recording, and payment processing via Mpesa, along with SMS notifications for members.

## Features

- **Member Management**: Add, update, and delete member information.
- **Case Management**: Create, update, and track contribution cases.
- **Transaction Handling**: Record all transactions, including payments and penalties.
- **Mpesa Integration**: Handle offline payments through Safaricom's C2B API.
- **SMS Notifications**: Notify members of updates and payment confirmations using Africa's Talking API.
- **Automatic Penalty Deduction**: Automatically deduct penalties from a member's account when an invoice's due date passes without payment.

## Technologies Used

- Python
- Django
- PostgreSQL
- Africa's Talking API
- Safaricom's Mpesa Daraja API
- Docker (for containerization)

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
   Visit [Africa's Talking](https://africastalking.com/) to create an account. You'll need to obtain your API credentials, including the username and API key, which are essential for configuring the application.

5. **Register an Account on Safaricom's Developer Portal**:
   Go to the [Safaricom Developer Portal](https://developer.safaricom.co.ke/) and sign up for an account. After registering, you'll receive credentials, including the API key and secret, required for integrating Mpesa services.

6. **Environment Configuration**:
   - Create a `.env` file in the root directory of the Django project.
   - Add the following credentials to your `.env` file:

     ```bash
      # Django settings
      SECRET_KEY= # Your Django secret key

      # Africa's Talking API credentials
      AFRICA_TALKING_USERNAME=your_africas_talking_username
      AFRICA_TALKING_API_KEY=your_africas_talking_api_key
      AFRICA_TALKING_API_URL=https://api.sandbox.africastalking.com/version1/messaging
      AFRICA_TALKING_AUTH_TOKEN_URL=https://api.africastalking.com/auth-token/generate

      # Mpesa settings
      MPESA_ENV=sandbox
      WHITELISTED_IPS=[196.201.214.200,196.201.214.206,196.201.213.114,196.201.214.207,196.201.214.208,196.201.213.44,196.201.212.127,196.201.212.138,196.201.212.129,196.201.212.136,196.201.212.74,196.201.212.69]
      MPESA_CONSUMER_KEY=your_mpesa_consumer_key
      MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
      MPESA_SHORTCODE=your_mpesa_shortcode
      CONFIRMATION_URL=yourdomain.com/mpesa/confirmation/
      VALIDATION_URL=yourdomain.com/mpesa/validation/

      # Penalty settings
      PENALTY_AMOUNT=your_penalty_amount

      # Email settings
      EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
      EMAIL_HOST=smtp.gmail.com
      EMAIL_PORT=587
      EMAIL_USE_TLS=True
      EMAIL_HOST_USER=your_email@example.com
      EMAIL_HOST_PASSWORD=your_email_password
      DEFAULT_FROM_EMAIL=your_email@example.com

     ```

7. **Set up the database**:
   - Create a PostgreSQL database and update the `settings.py` with database configuration.

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
    - **Sandbox Environment**: You can register and update URLs as needed.
    - **Production Environment**: URL registration is a one-time process.

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
      0 0 * * * /bin/bash -c 'source venv/bin/activate && python manage.py apply_penalties'
      ```
      Explanation:
      - `/bin/bash -c` ensures the command is run in a shell.
      - `source venv/bin/activate` activates your virtual environment.
      - `python manage.py apply_penalties` runs the Django management command to apply penalties.

12. **Run the server**:
    ```bash
    python manage.py runserver
    ```

## Screenshots

<details>
  <summary>Click to view screenshots</summary>

  ![Screenshot 2025-01-19 181803](https://github.com/user-attachments/assets/6b9ce82a-af09-4d34-bd1e-d7b1a974ea7f)
  
  ![Screenshot 2025-01-28 200935](https://github.com/user-attachments/assets/42207e03-9598-49ab-87f1-2bc1f630042b)
  
  ![Screenshot 2025-01-28 200607](https://github.com/user-attachments/assets/a2354ed8-0061-4661-aab9-55c074f3fa6c)
  
  ![Screenshot 2025-01-28 200553](https://github.com/user-attachments/assets/8327d407-2437-4914-a29b-42eb7457123e)
  
  ![Screenshot 2025-01-28 200540](https://github.com/user-attachments/assets/29e29239-ed83-4784-8cda-34bc1d4d2dfb)
  
  ![Screenshot 2025-01-28 201437](https://github.com/user-attachments/assets/1b10dde1-daf9-4c29-bfab-8706803f98c6)
  
  ![Screenshot 2025-01-19 204735](https://github.com/user-attachments/assets/1fe0c6a3-bbf2-4c3c-9e4e-e4db103aee55)
  
  ![Screenshot 2025-01-19 181731](https://github.com/user-attachments/assets/28ad7385-2363-490f-8d62-0b4780e7887d)
  
  ![Screenshot 2025-01-19 181839](https://github.com/user-attachments/assets/2387d5be-87e7-4a1f-b9b9-e107e633065e)
  
  ![Screenshot 2025-01-19 181912](https://github.com/user-attachments/assets/3dc4cba0-2cc7-412c-9b42-191df4142e22)

</details>


## API Integration

### Mpesa Callback URL

The app will handle incoming payment notifications from Mpesa through the Callback URL.

### SMS Notifications

The app has SMS sending logic handled using Africa's Talking API.
