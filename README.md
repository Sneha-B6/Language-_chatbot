# Language Learning Tutor 

An intelligent AI-powered language learning companion that provides personalized tutoring in multiple languages.

## Features 

- Interactive language learning sessions in Spanish, French, German, Italian, and Japanese
- Three proficiency levels: Beginner, Intermediate, and Advanced
- Real-time corrections and feedback
- Conversation history tracking
- Personalized learning experience
- Color-coded interface for better user experience

## System Architecture 

The system consists of the following components:

1. **Language Tutor Core**
   - Powered by Llama 70B model for natural language processing
   - LangChain integration for conversation management
   - SQLite database for persistent conversation history
   - Custom API handler for model interactions

2. **Error Tracking System**
   - Real-time mistake monitoring
   - Contextual feedback and corrections
   - Progress analysis and reporting
   - Historical performance tracking

3. **User Interface**
   - Intuitive command-line interface
   - Color-coded interactions for better readability
   - Simple navigation commands
   - User-friendly menu system

## Getting Started 

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for API access

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/language-learning-tutor.git
   cd language-learning-tutor
   pip install -r requirements.txt
