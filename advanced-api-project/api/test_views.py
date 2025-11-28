from rest_framework.test import APITestCase
from rest_framework import status", "response.data"

class TestSample(APITestCase):
    def test_basic(self):
        self.assertEqual(1, 1)


### ▶️ How to Run Tests
1. Activate virtual environment
2. Navigate to project directory
3. Run:

```bash
python manage.py test api
