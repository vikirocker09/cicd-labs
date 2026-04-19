# Flask Jenkins CI/CD Pipeline

A complete Jenkins CI/CD pipeline for a Python Flask web application — covering Build, Test, Lint, Security Scan, Package, and Staging Deployment stages.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Jenkins Setup](#jenkins-setup)
- [Pipeline Stages](#pipeline-stages)
- [Configuration](#configuration)
- [Notifications](#notifications)
- [Running Locally](#running-locally)

---
### screenshots
  
<img width="940" height="427" alt="image" src="https://github.com/user-attachments/assets/94ebe9b4-0549-4f97-bc54-795882b5fe6d" />
<img width="940" height="427" alt="image" src="https://github.com/user-attachments/assets/e2aa5b0c-f6c9-47a6-a433-fa00a40c200d" />
<img width="940" height="427" alt="image" src="https://github.com/user-attachments/assets/775164c9-2c84-41b1-bd48-906b148f8146" />
<img width="940" height="164" alt="image" src="https://github.com/user-attachments/assets/f8549250-5391-4ced-88e7-764115a701b2" />

## Project Structure

```
flask-jenkins-cicd/
├── app/
│   └── app.py              # Flask application
├── tests/
│   └── test_app.py         # pytest unit tests
├── reports/                # Auto-generated test & coverage reports
├── dist/                   # Auto-generated deployment packages
├── requirements.txt        # Python dependencies
├── Jenkinsfile             # Jenkins pipeline definition
└── README.md
```

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Jenkins | ≥ 2.414 | CI/CD server |
| Python | ≥ 3.9 | Runtime |
| pip | latest | Package manager |
| Git | any | SCM |
| Java | ≥ 17 | Jenkins runtime |

### Required Jenkins Plugins

Install these from **Manage Jenkins → Plugins**:

- **Pipeline** (workflow-aggregator)
- **GitHub Integration** (github)
- **Email Extension** (email-ext)
- **HTML Publisher** (htmlpublisher)
- **JUnit** (junit)
- **Git** (git)

---

## Jenkins Setup

### 1. Install Jenkins

```bash
# Ubuntu / Debian
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | \
  sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian binary/" | \
  sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt-get update && sudo apt-get install -y jenkins python3 python3-pip python3-venv
sudo systemctl enable --now jenkins
```

### 2. Fork & Clone the Repository

1. Fork this repo on GitHub.
2. Clone it onto the Jenkins server:

```bash
git clone https://github.com/<your-username>/flask-jenkins-cicd.git
```

### 3. Create the Jenkins Pipeline Job

1. Click **New Item** → enter a name → choose **Pipeline** → OK.
2. Under **Build Triggers**, check **GitHub hook trigger for GITScm polling**.
3. Under **Pipeline**, select **Pipeline script from SCM**.
4. Set SCM to **Git**, paste your forked repo URL, set branch to `*/main`.
5. Set **Script Path** to `Jenkinsfile`.
6. Click **Save**.

### 4. Configure GitHub Webhook

In your GitHub repo go to **Settings → Webhooks → Add webhook**:

- **Payload URL**: `http://<jenkins-host>:8080/github-webhook/`
- **Content type**: `application/json`
- **Events**: _Just the push event_

### 5. Configure Email Notifications

Go to **Manage Jenkins → System**:

- Fill in **SMTP server**, port, credentials under **Extended E-mail Notification**.
- Update `EMAIL_RECIPIENT` in the `Jenkinsfile` environment block.

---

## Pipeline Stages

```
Checkout → Build → Lint → Test → Security Scan → Package → Deploy to Staging → Smoke Test
```

| Stage | Description |
|-------|-------------|
| **Checkout** | Pulls latest source from GitHub |
| **Build** | Creates Python virtualenv, installs all `requirements.txt` deps |
| **Lint** | Runs `flake8` for code style (non-blocking) |
| **Test** | Executes `pytest` with JUnit XML + HTML coverage report |
| **Security Scan** | Checks dependencies for known CVEs with `safety` |
| **Package** | Tars application into a versioned archive, archives artifact |
| **Deploy to Staging** | Copies package to staging host & restarts the service (`main` only) |
| **Smoke Test** | Hits `/health` endpoint to confirm deployment succeeded |

---

## Configuration

Edit the `environment` block at the top of `Jenkinsfile`:

```groovy
environment {
    STAGING_HOST    = 'staging-server'       // Your staging server hostname/IP
    DEPLOY_USER     = 'deploy'               // SSH user for deployment
    EMAIL_RECIPIENT = 'team@yourdomain.com'  // Alert email address
    APP_PORT        = '5000'                 // Flask port
}
```

---

## Notifications

Emails are sent automatically via the **Email Extension Plugin** after every build:

| Event | Email Subject |
|-------|--------------|
| Success | ✅ [Jenkins] `<job>` #`<n>` – SUCCESS |
| Failure | ❌ [Jenkins] `<job>` #`<n>` – FAILED |

Each email includes job name, build number, branch, commit SHA, duration, and a direct link to the build or console log.

---

## Running Locally

```bash
# Clone
git clone https://github.com/<your-username>/flask-jenkins-cicd.git
cd flask-jenkins-cicd

# Install deps
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v --cov=app

# Start the app
python app/app.py
# → http://localhost:5000
```

### API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home — version & status |
| GET | `/health` | Health check |
| GET | `/api/greet/<name>` | Personalised greeting |




 
 
 


