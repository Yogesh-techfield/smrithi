# SmritiSathi (স্মৃতিসাথী)
### AI-Based Cognitive Gaming and Memory Assistance Platform for Elderly Dementia Patients in North Eastern Region (NER)

**Platform**: SmritiSathi  
**Problem Statement**: SIH26003 (Ministry of Development of North Eastern Region)  
**Theme**: MedTech / BioTech / HealthTech  

---

## 1. Project Overview
SmritiSathi is an offline-first, voice-enabled cognitive support platform tailored for elderly dementia and cognitive decline patients in the North Eastern Region of India.

### Key Capabilities
- **Cognitive & Memory Games**: Picture matching, face-name recall, word finding, and task sequencing.
- **Adaptive Difficulty Engine**: Calculates real-time session scores ($P = 0.7a + 0.3s$) and updates levels.
- **Personal Memory Graph**: Retains family members, relationships, and daily medicine routines.
- **Reminders & Alerts**: Automated triggers for missed medicines ($\ge 3$) and cognitive score decline slope ($< -0.05$).
- **Elderly-Friendly UI**: High contrast, large touch targets, and voice assistance fallback.

---

## 2. Microservices Architecture
The system consists of independent microservices:
- **Auth Service** (Port 5000): Authentication, JWT token verification, and user profiles.
- **Game & Adaptive Service** (Port 5001): Manages game catalog, session scoring, and adaptive level adjustments.
- **Memory & Sync Service** (Port 5002): Memory graph traversal, medicine reminders, offline data sync, and caregiver alerts.
- **Frontend** (Port 80): Static web interface with audio assistance.
- **Databases**: PostgreSQL (5432) and Redis (6379) for queuing and alert state.

---

## 3. How to Run Locally

### Using Docker Compose
```bash
docker-compose up -d --build
```
Access the application:
- Web Application: http://localhost
- Auth Service: http://localhost:5000/health
- Game Service: http://localhost:5001/health
- Memory Service: http://localhost:5002/health

### Running Services Directly with Python
```bash
pip install -r requirements.txt

# Terminal 1: Auth Service
python services/auth_service/app.py

# Terminal 2: Game Service
python services/game_service/app.py

# Terminal 3: Memory Service
python services/memory_service/app.py
```

### Running Unit Tests
```bash
pytest --cov=services tests/
```

---

## 4. Deploying to AWS EC2 via Terraform
The project includes Infrastructure as Code (IaC) to launch the complete stack on AWS EC2 in region `ap-south-1`.

### Step 1: Configure AWS CLI Credentials
Login with your AWS account credentials (associated with `yogyatha12345@gmail.com`):
```bash
aws configure
```
Provide:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name: `ap-south-1`
- Default output format: `json`

### Step 2: Initialize & Apply Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```
After completion, Terraform will output the public IP and web URL of your EC2 instance.

---

## 5. How to Push This Project to GitHub

Initialize the repository and push:
```bash
git init
git add .
git commit -m "Initial commit of SmritiSathi project for INT 378 and SIH26003"
git branch -M main
git remote add origin https://github.com/<your-github-username>/smrithi.git
git push -u origin main
```
