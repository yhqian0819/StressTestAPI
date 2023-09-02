from locust import HttpUser, between, task

class MyWebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_main(self):
        self.client.get("/test")