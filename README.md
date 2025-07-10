# GameVoiceControl

**Voice-activated in-game control for Windows, no Alt-Tab required**

## 🚀 Features
1. Real-time speech-to-text using AWS Transcribe  
2. Local Python agent mapping commands (e.g., “stop music”, “close window”) to OS actions  
3. Dockerized microservices with CI/CD pipeline for rapid releases  
4. React dashboard for logs, metrics, and custom macro setup

## 🛠️ Tech Stack
- **Frontend:** React, AWS Amplify  
- **Backend:** Python (`speech_recognition`, `pywin32`), AWS Lambda  
- **Containerization:** Docker, GitHub Actions  
- **Cloud:** AWS Transcribe, ECS/Fargate

## 📐 Architecture
1. **Microphone input** → streamed to **AWS Transcribe**  
2. **Lambda function** parses text → pushes to **local agent**  
3. **Local agent** executes OS commands  
4. **Dashboard** displays command history and analytics

## ⚙️ Installation
1. Clone: `git clone https://github.com/yourname/GameVoiceControl.git`  
2. Build services: `docker-compose up --build`  
3. Configure AWS credentials & Transcribe in `config.yml`  
4. Start listener: `python agent/main.py`  
5. Launch dashboard: `npm start` in `/dashboard`

## 🙌 Contributing
1. Fork repo & create branch  
2. Write tests & update docs  
3. Submit PR for review
