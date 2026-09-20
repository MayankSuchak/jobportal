from app import create_app, db
from app.models import User, Job, Application, SavedJob, JobCategory

def test_routes():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        # 1. Test Homepage
        res = client.get('/')
        assert res.status_code == 200
        assert b'NextHire' in res.data
        assert b'Discover Your Next Career Move' in res.data
        print("[PASS] Homepage loaded successfully (200 OK)")

        # 2. Test Jobs Search & Filtering
        res = client.get('/jobs?q=Python')
        assert res.status_code == 200
        assert b'Senior Full-Stack Python Engineer' in res.data
        print("[PASS] Job search with keyword returned matching jobs (200 OK)")

        # 3. Test Job Detail Page
        res = client.get('/jobs/1')
        assert res.status_code == 200
        assert b'Job Overview' in res.data
        print("[PASS] Job detail view (200 OK)")

        # 4. Test Categories Page
        res = client.get('/categories')
        assert res.status_code == 200
        assert b'Software Engineering' in res.data
        print("[PASS] Categories directory view (200 OK)")

        # 5. Test Candidate Login
        res = client.post('/auth/login', data={
            'email': 'candidate@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b'Candidate Dashboard' in res.data or b'Hello, Alex' in res.data
        print("[PASS] Candidate login authentication succeeded (200 OK)")

        # 6. Test Candidate Dashboard & Applications
        res = client.get('/seeker/dashboard')
        assert res.status_code == 200
        assert b'Total Applied' in res.data
        print("[PASS] Candidate dashboard view (200 OK)")

        res = client.get('/seeker/applications')
        assert res.status_code == 200
        assert b'My Applications' in res.data
        print("[PASS] Candidate applications history view (200 OK)")

        # 7. Test Logout
        res = client.get('/auth/logout', follow_redirects=True)
        assert res.status_code == 200
        assert b'logged out' in res.data
        print("[PASS] Logout succeeded (200 OK)")

        # 8. Test Employer Login
        res = client.post('/auth/login', data={
            'email': 'recruiter@techcorp.com',
            'password': 'password123'
        }, follow_redirects=True)
        assert res.status_code == 200
        assert b'TechCorp Global' in res.data or b'Employer' in res.data
        print("[PASS] Employer login authentication succeeded (200 OK)")

        # 9. Test Employer Dashboard & Applicants Board
        res = client.get('/employer/dashboard')
        assert res.status_code == 200
        assert b'Active Listings' in res.data
        print("[PASS] Employer dashboard view (200 OK)")

        res = client.get('/employer/manage-jobs')
        assert res.status_code == 200
        assert b'Manage Job Listings' in res.data
        print("[PASS] Employer job management view (200 OK)")

        res = client.get('/employer/applicants')
        assert res.status_code == 200
        assert b'Applicant Tracking' in res.data
        print("[PASS] Employer applicant tracking board (200 OK)")

        print("\nAll automated integration tests passed with 100% success!")

if __name__ == '__main__':
    test_routes()
