import requests

base_url = "http://127.0.0.1"
final_url = base_url+":8080/api/client"
print("Url is", final_url)


payload = {
    'email': "sachin@mail.com",
    'password': "paradox",
    'role': "Student",
}

response = requests.post(final_url, data=payload)

print(response.text)  # TEXT/HTML
print(response.status_code, response.reason)  # HTTP
