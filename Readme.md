# Self-Healing CI/CD Pipeline

## Overview
An intelligent CI/CD pipeline that automatically detects, retries, and recovers from failures without manual intervention.

## Self-Healing Capabilities
| Failure Type | Self-Healing Action |
|--------------|---------------------|
| Network timeout | Auto-retry 3 times |
| Flaky test | Auto-retry with backoff |
| Build failure | Auto-retry with clean cache |
| Container unhealthy | Auto-restart |
| Deployment failure | Auto-rollback |

## Tech Stack
- Jenkins (CI/CD)
- Docker (Containerization)
- GitHub (Version Control)
- Docker Hub (Registry)
- Python Flask (Sample App)

## Setup Instructions

### Prerequisites
- Docker Desktop installed
- Jenkins installed
- GitHub account
- Docker Hub account

### Steps to Run

1. Clone the repository
2. Push to GitHub
3. Configure Jenkins with Docker Hub credentials
4. Create new Pipeline job in Jenkins
5. Point to GitHub repo and Jenkinsfile
6. Build Now

## Testing Self-Healing

Test the self-healing capabilities:

1. **Test retry**: Push code with syntax error, watch auto-retry
2. **Test rollback**: Force deployment failure
3. **Test health check**: Kill container manually

## Demo URLs
- Application: http://localhost:5000
- Health Check: http://localhost:5000/health
- Force Failure: http://localhost:5000/fail

#I have added the webhook for automatic testing and building 
## Author
Shreya Tripathi