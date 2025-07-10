# No Alt Tab - Game Voice Assistant

**Voice-activated in-game control for Windows, no Alt-Tab required**

This project allows gamers to control their games and system using voice commands without having to Alt-Tab out of their gaming sessions. The system uses speech recognition to capture voice commands, processes them, and executes the appropriate actions.

## Features

1. Real-time speech recognition using both local (SpeechRecognition) and cloud (AWS Transcribe) options
2. Modular command system for easy extension with new voice commands
3. Containerized agent with Docker for easy deployment
4. React dashboard for monitoring command logs and system status
5. CI/CD pipeline using GitHub Actions for automated testing and deployment

## Tech Stack

- **Voice Recognition:** SpeechRecognition, AWS Transcribe
- **Backend:** Python, Flask REST API
- **Frontend:** React, Axios
- **Deployment:** Docker, AWS Amplify
- **CI/CD:** GitHub Actions

## Project Structure

```
├── agent/                  # Python voice command agent
│   ├── commands/          # Command handlers
│   │   ├── stop_music.py  # Example command handler
│   │   ├── mute_game.py   # Example command handler
│   │   └── ...           
│   └── main.py            # Main agent code with speech recognition
├── dashboard/             # React dashboard
│   ├── public/            # Public assets
│   └── src/               # React source code
│       ├── components/    # React components
│       └── ...           
├── .github/workflows/     # GitHub Actions workflows
├── Dockerfile             # Docker configuration for agent
└── requirements.txt       # Python dependencies
```

## Installation and Setup

### Prerequisites

- Python 3.10+
- Node.js LTS
- Docker (optional for containerization)
- AWS Account (optional for AWS Transcribe and Amplify)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/No_alt_tab.git
   cd No_alt_tab
   ```

2. Set up the Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up AWS credentials (optional, for AWS Transcribe):
   ```bash
   aws configure
   ```

4. Run the agent:
   ```bash
   python agent/main.py
   ```

5. Set up the dashboard:
   ```bash
   cd dashboard
   npm install
   npm start
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t game-agent .
   ```

2. Run the container:
   ```bash
   docker run --rm -p 5000:5000 game-agent
   ```

## Using the Voice Commands

Once the agent is running, you can use the following voice commands:

- "Stop music" - Stops background music in your game
- "Mute game" - Mutes game audio
- "Take screenshot" - Takes a screenshot of your game

You can add more commands by creating new modules in the `agent/commands/` directory.

## Dashboard

The dashboard provides a web interface to monitor your voice commands and system status. It displays:

- Recent voice commands and their results
- System status and health
- Command history and analytics

Access the dashboard at `http://localhost:3000` when running locally.

## Deployment

### AWS Amplify Deployment

1. Push your code to GitHub
2. Connect your repository to AWS Amplify
3. Amplify will automatically build and deploy your dashboard

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
