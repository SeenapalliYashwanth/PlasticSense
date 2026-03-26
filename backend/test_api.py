import os
import sys
from fastapi.testclient import TestClient

# Ensure package root is in Python path for importing backend package
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app import app

client = TestClient(app)


def test_analyze_pet():
    r = client.get('/analyze?plastic_type=PET')
    assert r.status_code == 200
    body = r.json()
    assert body['plastic_type'] == 'PET'
    assert 'decision' in body


def test_analyze_image_not_found_file():
    # ensure this endpoint works for method handling
    r = client.get('/analyze-image')
    assert r.status_code == 405
