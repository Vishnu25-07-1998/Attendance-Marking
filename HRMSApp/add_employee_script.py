import requests
import json

# Define the URL of your API endpoint
api_url = "http://localhost:8000/api/add_employee/"  # Update with your actual API endpoint

# Define the employee data in a Python dictionary
employee_data = {
    "name": "John Doe",
    "designation": "Developer",
    "department": "IT",
    "date_of_joining": "2024-01-16"
}

# Convert the dictionary to a JSON string
json_data = json.dumps(employee_data)

# Set the headers with the correct Content-Type
headers = {"Content-Type": "application/json"}

# Make the POST request
response = requests.post(api_url, data=json_data, headers=headers)

# Print the response
print(response.status_code)
print(response.json())
