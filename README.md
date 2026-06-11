# Personalized Diet Planner

**Personalized Diet Planner** is a full-stack diet management application that leverages Artificial Intelligence to help users create customized meal plans based on their health profiles, dietary preferences, and fitness goals. The platform combines health metrics analysis, AI-powered meal recommendations, nutritional guidance, and personalized diet plans to create a comprehensive dietary management experience.

## ✨ Key Features

- **Health Profile Analysis:** Input personal health metrics including weight, height, age, activity level, and dietary preferences to create a personalized profile.
- **BMI Calculation:** Automatically calculate Body Mass Index (BMI) and receive categorized health status (Underweight, Normal weight, Overweight, Obese).
- **AI-Powered Meal Recommendations:** Generate personalized meal recommendations based on nutritional needs, health goals, and dietary restrictions using Google Gemini.
- **Nutritional Database:** Access a comprehensive food dataset with detailed nutritional information including calories, proteins, fats, carbohydrates, and micronutrients.
- **Customized Diet Plans:** Create role-specific diet plans tailored to fitness goals (weight loss, muscle gain, maintenance) and health conditions.
- **Dietary Guidance:** Receive personalized nutrition advice, calorie tracking recommendations, and meal timing suggestions from AI.
- **Modern User Interface:** Built with HTML5, CSS3, and vanilla JavaScript to provide a fast, responsive, and user-friendly experience.

## Architecture

Personalized Diet Planner follows a **decoupled frontend-backend architecture**, ensuring scalability, maintainability, and seamless AI integration.

### Backend Responsibilities

- REST API development
- AI service integration (Google Gemini)
- Health metrics calculation
- Nutritional data processing
- Personalized recommendation generation
- Diet plan management

### Frontend Responsibilities

- Interactive user interface
- Health profile form management
- Real-time API communication
- Diet plan visualization
- Responsive user experience

### Design Principles

- Separation of Concerns
- Modular Service Architecture
- AI-Centric Personalization
- Scalable and Extensible Design

---

## 🛠️ Technology Stack

### Backend

- Python 3
- Flask
- Flask-CORS
- Pandas (Data processing)
- NumPy (Numerical computations)

### Artificial Intelligence

- Google Gemini (`google-generativeai`)

### Data Processing

- Pandas
- CSV-based nutritional database

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

### Development Tools

- python-dotenv
- pip
- VS Code

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Modern web browser (Chrome, Firefox, Edge, Safari)
- *(Optional)* Google Gemini API Key for AI-powered coaching

### Clone the Repository

```bash
git clone <repository-url>
cd "personalised diet planner"
```

### Backend Setup

```bash
cd backend

# Create virtual environment (Optional but recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

*(Optional)* Create a `.env` file in the backend directory to enable AI coaching:

```
GEMINI_API_KEY=your_api_key_here
```

**Note:** The app works without an API key. The key is only needed for personalized AI coaching.

Run the backend server:

```bash
python app.py
```

The backend will start on `http://localhost:5000` (or the port specified in the console).

### Frontend Setup

Simply open the application in your web browser:

```
http://localhost:5000
```

The Flask server automatically serves the frontend static files and templates.

---

## 📂 Project Structure

```
personalised-diet-planner/
├── backend/
│   ├── app.py              # Flask application & API routes
│   ├── food_dataset.csv    # Nutritional database
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables (create this)
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Styling
│   │   └── js/
│   │       └── app.js      # Frontend logic
│   ├── templates/
│   │   └── index.html      # Main page
│   
└── README.md
```

## ⚙️ How It Works

1. **Backend Processing:** When you submit your health profile, the Flask backend calculates BMI, daily calorie needs, and macro targets
2. **Meal Recommendations:** The app generates a 7-day personalized meal plan from the nutritional database
3. **AI Coaching (Optional):** If a Gemini API key is provided, the app generates personalized coaching tips and shopping lists
4. **Results Display:** The frontend displays your metrics, weekly meal plan, and optional AI guidance

## 🌟 Highlights

- ✨ AI-powered personalized diet planning
- 💪 Health metric analysis and BMI calculation
- 🍽️ Comprehensive nutritional database
- 🎯 Customized meal recommendations based on goals
- 📊 Automatic nutritional tracking
- 🎨 Clean and intuitive user interface
- ⚡ Fast response times with optimized AI queries
- 📱 Responsive design for desktop and tablet devices

## 🔮 Future Enhancements

- Mobile app (React Native/Flutter)
- Grocery list generation and price estimation
- Recipe integration with cooking instructions
- Exercise and fitness tracking integration
- Progress tracking and analytics dashboard
- Social features (meal plan sharing, community feedback)
- Push notifications for meal reminders
- Integration with fitness trackers (Fitbit, Apple Health)
- Multi-language support
- Offline mode for saved diet plans
- Video tutorials for meal preparation

---

## 📝 Usage Guide

1. **Create Your Profile:** Enter your health metrics (weight, height, age, activity level)
2. **Select Goals:** Choose your dietary goal (weight loss, muscle gain, maintenance)
3. **Input Preferences:** Specify dietary restrictions and food preferences
4. **Generate Plan:** Let AI create a personalized diet plan
5. **Follow Recommendations:** Get daily meal suggestions and nutritional guidance
6. **Track Progress:** Monitor your adherence and health improvements

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```
GEMINI_API_KEY=your_google_gemini_api_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### Customization

- **Food Database:** Update `food_dataset.csv` with additional foods and nutritional data
- **API Keys:** Replace the Gemini API key in `.env`
- **UI Theme:** Modify `frontend/static/css/style.css` for custom styling

---

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is available

### API key errors
- Verify your Gemini API key is correct and active
- Ensure `.env` file is in the `backend/` directory
- Check that the key has necessary permissions

### Frontend not loading
- Ensure Flask server is running on `http://localhost:5000`
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console for errors (F12)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request with improvements.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Happy healthy eating! 🥗🍎**
