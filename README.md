# Delivery Service Platform

A comprehensive delivery service platform that connects businesses and users for various services including food delivery, shopping, and more.

## Features

- User and Business Registration
- Multi-category Service Listing
- Location-Based Service Filtering
- Real-time Order Tracking
- Shopping Cart and Checkout System
- Business Analytics Dashboard
- Reviews and Ratings System
- Delivery Personnel Management
- Real-time Notifications
- Recommendation System

## Tech Stack

- Backend: Django, Django REST Framework
- Database: PostgreSQL
- Real-time Features: Django Channels, Redis
- Frontend: Django Templates, Bootstrap 5
- Task Queue: Celery
- Location Services: django-location-field

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=delivery_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

- `accounts/`: User and business authentication
- `core/`: Core functionality and utilities
- `services/`: Service listings and categories
- `orders/`: Order management and tracking
- `delivery/`: Delivery personnel management
- `notifications/`: Real-time notifications
- `analytics/`: Business analytics dashboard
- `recommendations/`: Service recommendation system

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests. 