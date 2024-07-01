import random
import string

from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(3, 5)

    @task
    def register_user(self):
        first_digit = random.choice(['7', '8'])
        rest_digits = ''.join(random.choices('0123456789', k=10))
        number = f"{first_digit}{rest_digits}"
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])
        email = f"{username}@{domain}"
        credo_schema = {
            "first_name": "Ivanov",
            "last_name": "Ivanov",
            "email": email,
            "number_phone": number,
            "password": "ghjv!231G",
            "middle_name": "Iofaf",
            "time_call": "in 8h"
        }
        response = self.client.post("http://127.0.0.1:8000/api/v1/auth/sign-up", json=credo_schema)
