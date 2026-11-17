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

###  Initialize & Apply Terraform
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```
After completion, Terraform will output the public IP and web URL of your EC2 instance.

---

