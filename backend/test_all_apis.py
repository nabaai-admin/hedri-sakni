#!/usr/bin/env python3
"""Comprehensive API testing script"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class APITester:
    def __init__(self):
        self.token = None
        self.headers = {}
        self.results = []
        
    def log(self, endpoint, method, status, success, message=""):
        result = {
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "success": success,
            "message": message
        }
        self.results.append(result)
        status_icon = "✓" if success else "✗"
        print(f"{status_icon} {method:6} {endpoint:40} [{status}] {message}")
    
    def test_login(self):
        print("\n=== AUTHENTICATION ===")
        url = f"{BASE_URL}/auth/login"
        payload = {"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.token = response.json().get('token')
                self.headers = {
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
                self.log("/auth/login", "POST", 200, True, "Login successful")
            else:
                self.log("/auth/login", "POST", response.status_code, False, "Login failed")
                return False
        except Exception as e:
            self.log("/auth/login", "POST", 0, False, str(e))
            return False
        return True
    
    def test_areas(self):
        print("\n=== AREAS ===")
        base = f"{BASE_URL}/areas"
        
        # GET all areas
        try:
            r = requests.get(base, headers=self.headers)
            self.log("/areas", "GET", r.status_code, r.status_code == 200)
        except Exception as e:
            self.log("/areas", "GET", 0, False, str(e))
        
        # POST create area
        area_data = {
            "name": f"Test Area {datetime.now().timestamp()}",
            "description": "Automated test area",
            "link": "https://example.com",
            "is_active": True
        }
        try:
            r = requests.post(base, json=area_data, headers=self.headers)
            if r.status_code == 201:
                area_id = r.json().get('data', {}).get('id')
                self.log("/areas", "POST", 201, True, f"Created area ID: {area_id}")
                
                # GET specific area
                try:
                    r = requests.get(f"{base}/{area_id}", headers=self.headers)
                    self.log(f"/areas/{area_id}", "GET", r.status_code, r.status_code == 200)
                except Exception as e:
                    self.log(f"/areas/{area_id}", "GET", 0, False, str(e))
                
                # PUT update area
                try:
                    r = requests.put(f"{base}/{area_id}", json={"description": "Updated"}, headers=self.headers)
                    self.log(f"/areas/{area_id}", "PUT", r.status_code, r.status_code == 200)
                except Exception as e:
                    self.log(f"/areas/{area_id}", "PUT", 0, False, str(e))
                
                # DELETE area
                try:
                    r = requests.delete(f"{base}/{area_id}", headers=self.headers)
                    self.log(f"/areas/{area_id}", "DELETE", r.status_code, r.status_code == 200)
                except Exception as e:
                    self.log(f"/areas/{area_id}", "DELETE", 0, False, str(e))
            else:
                self.log("/areas", "POST", r.status_code, False, r.text)
        except Exception as e:
            self.log("/areas", "POST", 0, False, str(e))
    
    def test_customers(self):
        print("\n=== CUSTOMERS ===")
        base = f"{BASE_URL}/customers"
        
        # GET all customers
        try:
            r = requests.get(base, headers=self.headers)
            self.log("/customers", "GET", r.status_code, r.status_code == 200)
        except Exception as e:
            self.log("/customers", "GET", 0, False, str(e))
        
        # Create test area first
        area_data = {"name": f"Customer Test Area {datetime.now().timestamp()}", "is_active": True}
        try:
            r = requests.post(f"{BASE_URL}/areas", json=area_data, headers=self.headers)
            if r.status_code == 201:
                area_id = r.json().get('data', {}).get('id')
                
                # POST create customer
                customer_data = {
                    "name": "Test Customer",
                    "phone_number": "1234567890",
                    "national_id": f"NID{datetime.now().timestamp()}",
                    "area_id": area_id,
                    "reservation_status": "OPEN"
                }
                try:
                    r = requests.post(base, json=customer_data, headers=self.headers)
                    if r.status_code == 201:
                        customer_id = r.json().get('data', {}).get('id')
                        self.log("/customers", "POST", 201, True, f"Created customer ID: {customer_id}")
                        
                        # GET specific customer
                        try:
                            r = requests.get(f"{base}/{customer_id}", headers=self.headers)
                            self.log(f"/customers/{customer_id}", "GET", r.status_code, r.status_code == 200)
                        except Exception as e:
                            self.log(f"/customers/{customer_id}", "GET", 0, False, str(e))
                        
                        # PUT update customer
                        try:
                            r = requests.put(f"{base}/{customer_id}", json={"name": "Updated Customer"}, headers=self.headers)
                            self.log(f"/customers/{customer_id}", "PUT", r.status_code, r.status_code == 200)
                        except Exception as e:
                            self.log(f"/customers/{customer_id}", "PUT", 0, False, str(e))
                        
                        # DELETE customer
                        try:
                            r = requests.delete(f"{base}/{customer_id}", headers=self.headers)
                            self.log(f"/customers/{customer_id}", "DELETE", r.status_code, r.status_code == 200)
                        except Exception as e:
                            self.log(f"/customers/{customer_id}", "DELETE", 0, False, str(e))
                    else:
                        self.log("/customers", "POST", r.status_code, False, r.text)
                except Exception as e:
                    self.log("/customers", "POST", 0, False, str(e))
                
                # Cleanup test area
                requests.delete(f"{BASE_URL}/areas/{area_id}", headers=self.headers)
        except Exception as e:
            self.log("/customers", "POST", 0, False, f"Failed to create test area: {str(e)}")
    
    def test_reservations(self):
        print("\n=== RESERVATION SLOTS ===")
        base = f"{BASE_URL}/reservations"
        
        # GET all reservation slots
        try:
            r = requests.get(base, headers=self.headers)
            self.log("/reservations", "GET", r.status_code, r.status_code == 200)
        except Exception as e:
            self.log("/reservations", "GET", 0, False, str(e))
        
        # Create test area
        area_data = {"name": f"Reservation Test Area {datetime.now().timestamp()}", "is_active": True}
        try:
            r = requests.post(f"{BASE_URL}/areas", json=area_data, headers=self.headers)
            if r.status_code == 201:
                area_id = r.json().get('data', {}).get('id')
                
                # POST create reservation slot
                slot_data = {
                    "area_id": area_id,
                    "scheduled_datetime": (datetime.utcnow() + timedelta(hours=1)).isoformat()
                }
                try:
                    r = requests.post(base, json=slot_data, headers=self.headers)
                    if r.status_code == 201:
                        slot_id = r.json().get('data', {}).get('id')
                        self.log("/reservations", "POST", 201, True, f"Created slot ID: {slot_id}")
                        
                        # GET specific slot
                        try:
                            r = requests.get(f"{base}/{slot_id}", headers=self.headers)
                            self.log(f"/reservations/{slot_id}", "GET", r.status_code, r.status_code == 200)
                        except Exception as e:
                            self.log(f"/reservations/{slot_id}", "GET", 0, False, str(e))
                        
                        # PUT update slot
                        try:
                            update_data = {"scheduled_datetime": (datetime.utcnow() + timedelta(hours=2)).isoformat()}
                            r = requests.put(f"{base}/{slot_id}", json=update_data, headers=self.headers)
                            self.log(f"/reservations/{slot_id}", "PUT", r.status_code, r.status_code == 200)
                        except Exception as e:
                            self.log(f"/reservations/{slot_id}", "PUT", 0, False, str(e))
                        
                        # DELETE slot
                        try:
                            r = requests.delete(f"{base}/{slot_id}", headers=self.headers)
                            self.log(f"/reservations/{slot_id}", "DELETE", r.status_code, r.status_code == 200)
                        except Exception as e:
                            self.log(f"/reservations/{slot_id}", "DELETE", 0, False, str(e))
                    else:
                        self.log("/reservations", "POST", r.status_code, False, r.text)
                except Exception as e:
                    self.log("/reservations", "POST", 0, False, str(e))
                
                # Cleanup test area
                requests.delete(f"{BASE_URL}/areas/{area_id}", headers=self.headers)
        except Exception as e:
            self.log("/reservations", "POST", 0, False, f"Failed to create test area: {str(e)}")
    
    def test_analytics(self):
        print("\n=== ANALYTICS ===")
        
        # GET summary
        try:
            r = requests.get(f"{BASE_URL}/analytics/summary", headers=self.headers)
            self.log("/analytics/summary", "GET", r.status_code, r.status_code == 200)
        except Exception as e:
            self.log("/analytics/summary", "GET", 0, False, str(e))
        
        # GET attempts
        try:
            r = requests.get(f"{BASE_URL}/analytics/attempts", headers=self.headers)
            self.log("/analytics/attempts", "GET", r.status_code, r.status_code == 200)
        except Exception as e:
            self.log("/analytics/attempts", "GET", 0, False, str(e))
    
    def test_external(self):
        print("\n=== EXTERNAL INTEGRATION ===")
        
        # GET health check (no auth required)
        try:
            r = requests.get(f"{BASE_URL}/external/health")
            self.log("/external/health", "GET", r.status_code, r.status_code == 200)
        except Exception as e:
            self.log("/external/health", "GET", 0, False, str(e))
    
    def print_summary(self):
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r['success'])
        failed = total - passed
        
        print(f"Total tests: {total}")
        print(f"Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"Failed: {failed} ({failed/total*100:.1f}%)")
        
        if failed > 0:
            print("\nFailed tests:")
            for r in self.results:
                if not r['success']:
                    print(f"  - {r['method']} {r['endpoint']} [{r['status']}] {r['message']}")

def main():
    tester = APITester()
    
    if not tester.test_login():
        print("Authentication failed. Cannot proceed with tests.")
        return
    
    tester.test_areas()
    tester.test_customers()
    tester.test_reservations()
    tester.test_analytics()
    tester.test_external()
    
    tester.print_summary()

if __name__ == "__main__":
    main()
