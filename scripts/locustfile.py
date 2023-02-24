import random

from locust import HttpUser, task, between

from sklearn.datasets import load_iris

FREQUENT = 100
RARE = 1


class User(HttpUser):

    wait_time = between(1, 5)
    X, _ = load_iris(return_X_y=True)

    @task(FREQUENT)
    def send_correct_data(self):
        vals = random.choice(self.X)
        self.client.post(f"/predict?sepal_length={vals[0]}&sepal_width={vals[1]}"
                         f"&petal_length={vals[0]}&petal_width={vals[3]}")

    @task(RARE)
    def send_wrong_data(self):
        vals = random.choice(self.X)
        idx = random.choice(range(len(vals)))
        vals[idx] = 100
        self.client.post(f"/predict?sepal_length={vals[0]}&sepal_width={vals[1]}"
                         f"&petal_length={vals[0]}&petal_width={vals[3]}")
