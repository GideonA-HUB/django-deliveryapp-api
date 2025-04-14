import requests
import json
from datetime import datetime

BASE_URL = 'http://127.0.0.1:8000/api'

def get_token(username, password):
    response = requests.post(
        f'{BASE_URL}/token/',
        data={'username': username, 'password': password}
    )
    return response.json()['access']

def test_orders_api(token):
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test creating an order
    order_data = {
        'business': 1,  # Replace with actual business ID
        'delivery_address': '123 Test Street',
        'delivery_instructions': 'Ring bell',
        'items': [
            {
                'service': 1,  # Replace with actual service ID
                'quantity': 2,
                'price': 20.00
            }
        ]
    }
    
    print("\nTesting Order Creation:")
    response = requests.post(
        f'{BASE_URL}/orders/orders/',
        headers=headers,
        json=order_data
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    order_id = response.json().get('id')
    
    if order_id:
        # Test getting order details
        print("\nTesting Order Details:")
        response = requests.get(
            f'{BASE_URL}/orders/orders/{order_id}/',
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test updating order status
        print("\nTesting Order Status Update:")
        status_data = {
            'status': 'confirmed',
            'notes': 'Order confirmed by test'
        }
        response = requests.post(
            f'{BASE_URL}/orders/orders/{order_id}/update_status/',
            headers=headers,
            json=status_data
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test getting order items
        print("\nTesting Order Items:")
        response = requests.get(
            f'{BASE_URL}/orders/orders/{order_id}/items/',
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test getting order status history
        print("\nTesting Order Status History:")
        response = requests.get(
            f'{BASE_URL}/orders/orders/{order_id}/statuses/',
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

def main():
    # Replace with actual credentials
    username = 'test_user'
    password = 'test_password'
    
    try:
        token = get_token(username, password)
        print("Authentication successful!")
        test_orders_api(token)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main() 