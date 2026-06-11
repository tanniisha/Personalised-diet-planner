# Personalised Diet Planner

*Personalised Diet Planner* is a full-stack diet management application that uses health metrics and AI-powered recommendations to create customized weekly meal plans. It combines BMI calculation, nutritional analysis, and Google Gemini AI coaching into a clean Flask + vanilla JavaScript experience.

## ✨ Key Features

- *Health Profile Analysis:* Input age, gender, height, weight, activity level, fitness goal, and dietary preference.
- *BMI Calculation:* Computes Body Mass Index and returns a categorized health status.
- *AI-Powered Recommendations:* Google Gemini integration provides recipe guidance.
- *Personalized Diet Plans:* Builds a 7-day meal plan with calorie targets and dietary preference filtering.
- *Dietary Guidance:* Provides smart meal suggestions and health-focused insights.
- *Modern User Interface:* Built with HTML5, CSS3, and vanilla JavaScript.

## Architecture

The app uses a *decoupled frontend-backend architecture*.

### Backend Responsibilities

- REST API endpoint (/api/plan)
- Health metrics calculation
- Built-in nutrition data lookup and meal plan generation
- Google Gemini AI coaching integration

### Frontend Responsibilities

- User profile form handling
- API communication with the backend
- Weekly meal plan display
- Clickable recipe detail presentation
- Responsive and interactive UI

### Design Principles

- Separation of concerns
- Simple and maintainable structure
- AI-enabled personalization
- Easy extension and customization

## Technology Stack

### Backend

- Python 3
- Flask
- google-generativeai
- python-dotenv

### Artificial Intelligence

- Google Gemini (google-generativeai)

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

## Getting Started

### Prerequisites

- Python 3.8+ installed
- A modern browser (Chrome, Firefox, Edge, Safari)

### Clone the Repository

bash
git clone <repository-url>
cd "personalised diet planner"


### Backend Setup

bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt


Create a .env file in the backend/ folder to configure Google Gemini AI coaching:

env
GEMINI_API_KEY=your_api_key_here


Run the backend server:

bash
python app.py


Open the app in your browser:

text
http://localhost:5000


## Project Structure


personalised diet planner/
├── backend/
│   ├── app.py              
│   ├── requirements.txt    
│   └── .env               
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   
│   │   └── js/
│   │       └── app.js      
│   └── templates/
│       └── index.html      
└── README.md


##  How It Works

1. The user submits health profile details through the frontend form.
2. The Flask backend calculates BMI, daily calories, and macros.
3. The backend generates a weekly meal plan from a built-in nutrition dataset.
4. If GEMINI_API_KEY is provided, the backend requests AI coaching from Google Gemini.
5. The frontend displays the weekly plan and allows users to click meals for quick recipe details.

##  Highlights

- AI-enabled meal guidance with Gemini integration
- Personalized calorie and macro calculations
- Built-in nutrition dataset for meal recommendations
- Lightweight, dependency-minimal frontend

##  Future Enhancements

- Progress tracking and history
- Fitness and activity logging

##  Usage Guide

1. Enter your personal health details.
2. Choose your fitness goal.
3. Select your dietary preference.
4. Generate the weekly plan.
5. Click a meal card to view recipe-style preparation guidance.

## Configuration

### Environment Variables

Create backend/.env and add:

env
GEMINI_API_KEY=your_google_gemini_api_key


### Customization

- *Food data:* edit backend/app.py to adjust built-in meal items
- *Styles:* edit frontend/static/css/style.css
- *Logic:* edit backend/app.py and frontend/static/js/app.js

##  Troubleshooting

### Backend won't start

- Confirm Python 3.8+ is installed
- Activate the virtual environment
- Install dependencies: pip install -r requirements.txt
- Ensure port 5000 is free

### AI key errors

- Check the API key in backend/.env
- Verify your Gemini key is valid and active

### Frontend errors

- Make sure Flask is running
- Open browser developer console for errors

*Happy healthy eating! 🥗🍎*
