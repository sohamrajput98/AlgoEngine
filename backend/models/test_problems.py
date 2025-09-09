import requests

BASE_URL = "http://127.0.0.1:8000"

# Create a problem
problem_data = {
    "title": "Two Sum",
    "description": "Find two numbers that add up to target.",
    "concept": "hashing",
    "stars": 2,
    "series_id": 1,
    "series_index": 1
}
res = requests.post(f"{BASE_URL}/problems", json=problem_data)
print("POST /problems:", res.status_code, res.json())

# Get all problems
res = requests.get(f"{BASE_URL}/problems")
print("GET /problems:", res.status_code, res.json())

# Get one problem
res = requests.get(f"{BASE_URL}/problems/1")
print("GET /problems/1:", res.status_code, res.json())
