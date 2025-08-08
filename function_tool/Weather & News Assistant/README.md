# 🌤️ Weather & News Assistant

A professional AI-powered Streamlit application that provides real-time weather and news updates using advanced language models and multiple APIs.

## ✨ Features

- **🌍 Location Detection**: Automatically detect user's location using IP geolocation
- **🌤️ Real-time Weather**: Get detailed weather information including temperature, humidity, wind speed, and conditions
- **📰 Latest News**: Fetch the latest news headlines from your region
- **🤖 AI Assistant**: Powered by Gemini AI for intelligent responses
- **💬 Chat Interface**: Interactive chat-based interface for natural conversations
- **📱 Responsive Design**: Beautiful, modern UI that works on all devices
- **⚙️ API Status Monitoring**: Real-time status of all connected APIs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys for the following services:
  - **Gemini AI** (Google)
  - **OpenWeather** (Weather data)
  - **Mediastack** (News data)
  - **IP Geolocation** (Location detection)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd function_tool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using uv
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   NEW_API_KEY=your_mediastack_api_key_here
   LOCATION_API_KEY=your_ipgeolocation_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 Usage

### Getting Started

1. **Initialize the Agent**: Click "🔄 Initialize Agent" in the sidebar
2. **Detect Location**: Click "📍 Detect My Location" to get your current location
3. **Start Chatting**: Use the chat interface to ask questions like:
   - "What's the weather like today?"
   - "Show me the latest news"
   - "What's the weather in London?"
   - "Get news about technology"

### Quick Actions

The sidebar provides quick access to:
- **📍 Detect My Location**: Automatically detect your current location
- **🌤️ Get Weather**: Fetch current weather for your location
- **📰 Get Latest News**: Get the latest news headlines
- **🗑️ Clear Chat**: Clear the chat history

## 🔧 API Configuration

### Required API Keys

1. **Gemini AI** (Google)
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Used for AI-powered responses

2. **OpenWeather**
   - Sign up at [OpenWeather](https://openweathermap.org/api)
   - Used for weather data

3. **GNews**
   - Sign up at [GNews](https://gnews.io/)
   - **Important**: After signing up, you must activate your account by clicking the activation link in the email
   - Used for news data

4. **IP Geolocation**
   - Sign up at [IP Geolocation](https://ipgeolocation.io/)
   - Used for location detection

### Environment Variables

Create a `.env` file with the following variables:
```env
GEMINI_API_KEY=your_gemini_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
NEW_API_KEY=your_mediastack_api_key
LOCATION_API_KEY=your_ipgeolocation_api_key
```

## 🏗️ Architecture

### Components

- **`app.py`**: Main Streamlit application
- **`main.py`**: Command-line version of the agent
- **`location_tool.py`**: Location detection functionality
- **`weather_tool.py`**: Weather data fetching
- **`new_tool.py`**: News data fetching

### Technologies Used

- **Streamlit**: Web application framework
- **Agents SDK**: AI agent framework
- **Gemini AI**: Language model for responses
- **OpenWeather API**: Weather data
- **GNews API**: News data
- **IP Geolocation API**: Location detection

## 🎨 Features

### Professional UI
- Modern gradient design
- Responsive layout
- Interactive chat interface
- Real-time status indicators

### Smart Agent
- Automatic location detection
- Context-aware responses
- Error handling and recovery
- Professional formatting

### Real-time Data
- Live weather updates
- Latest news headlines
- Location-based content
- API status monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Agent not initializing**
   - Check your Gemini API key
   - Ensure all environment variables are set

2. **Location detection fails**
   - Verify your IP Geolocation API key
   - Check internet connection

3. **Weather data not loading**
   - Confirm OpenWeather API key
   - Check if the location exists in OpenWeather database

4. **News not loading**
   - Verify Mediastack API key
   - Check if news are available for your region

### Error Messages

- **"API key not found"**: Add the missing API key to your `.env` file
- **"Agent not initialized"**: Click "Initialize Agent" in the sidebar
- **"Location not detected"**: Click "Detect My Location" in the sidebar

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and AI Agents**
