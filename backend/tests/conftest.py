# conftest.py - pytest configuration for Planvesto backend tests
# No database fixtures - all tests are pure unit tests.
import os

os.environ.setdefault("SUPABASE_URL", "https://mock.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "mock-service-role-key-for-testing")
