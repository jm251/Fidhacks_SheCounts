# SheCounts Financial Literacy Chatbot Frontend

This project provides a web-based frontend for the SheCounts financial literacy chatbot, built with HTML/JavaScript frontend and Python Flask backend.

## Project Structure

```
chatbots code/
├── chatbot_code_template.py    # Original Streamlit chatbot
├── chatbot_backend.py          # Flask API backend
├── requirements.txt            # Python dependencies
├── setup_chatbot.py           # Setup script
└── README.md                  # This file

Root directory/
└── chatbot_frontend.html      # HTML frontend
```

## Features

- **Interactive Chat Interface**: Clean, responsive web interface
- **AI-Powered Questions**: Generate random financial literacy questions using Google Gemini
- **Answer Evaluation**: Automatic evaluation of user responses
- **Resource Recommendations**: Relevant financial resources from Pinecone database
- **Real-time Chat**: Seamless conversation flow with the AI assistant

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key
- Pinecone API key (optional, for resource recommendations)

### Quick Setup

1. **Navigate to the chatbots code directory**:
   ```bash
   cd "chatbots code"
   ```

2. **Run the setup script**:
   ```bash
   python setup_chatbot.py
   ```

3. **Configure API keys** in `chatbot_backend.py`:
   - Replace `YOUR_API_KEY_HERE` with your Google Gemini API key
   - Replace `YOUR_PINECONE_API_KEY_HERE` with your Pinecone API key

### Manual Setup

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create templates folder**:
   ```bash
   mkdir templates
   cp ../chatbot_frontend.html templates/
   ```

3. **Configure API keys** in `chatbot_backend.py`

## Running the Application

### Web Frontend (Recommended)

1. **Start the Flask backend**:
   ```bash
   python chatbot_backend.py
   ```

2. **Open your browser** to: http://localhost:5000

### Streamlit Version (Alternative)

For development or testing, you can also run the original Streamlit version:
```bash
streamlit run chatbot_code_template.py
```

## API Endpoints

The Flask backend provides the following REST API endpoints:

- `POST /api/generate_question` - Generate a new question
- `POST /api/submit_answer` - Submit and evaluate an answer
- `POST /api/ask_question` - Ask a general question
- `POST /api/reset_chat` - Reset the chat session

## Getting API Keys

### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to `chatbot_backend.py`

### Pinecone API Key (Optional)
1. Visit [Pinecone](https://app.pinecone.io/)
2. Create an account
3. Get your API key from the dashboard
4. Copy the key to `chatbot_backend.py`

## Customization

### Adding New Topics
Modify the `generate_question()` function in `chatbot_backend.py` to include new topics:
```python
def generate_question(self, topic="your_new_topic"):
    question_instruction = f"Generate a question about {topic}..."
```

### Styling
Edit the CSS in `chatbot_frontend.html` to customize the appearance:
- Colors, fonts, and layout in the `<style>` section
- Responsive design breakpoints
- Chat bubble styling

### Adding Resources
Update your Pinecone database with new financial literacy resources, or modify the `get_relevant_resource()` function to use different data sources.

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure API keys are correctly set in `chatbot_backend.py`
   - Check that your API keys have the necessary permissions

2. **Pinecone Connection Issues**
   - Verify your Pinecone API key and index name
   - The app will still work without Pinecone (resources won't be shown)

3. **Port Already in Use**
   - Change the port in `chatbot_backend.py`: `app.run(port=5001)`
   - Update the API_BASE_URL in the frontend accordingly

4. **CORS Issues**
   - Ensure Flask-CORS is installed: `pip install flask-cors`
   - Check that CORS is properly configured in the backend

### Development Tips

- Use browser developer tools to monitor API calls
- Check Flask console for backend error messages
- Test API endpoints individually using tools like Postman

## Integration with SheCounts Website

The frontend is designed to integrate seamlessly with the existing SheCounts website:
- Uses the same styling and navigation structure
- Matches the existing color scheme and fonts
- Includes the site header and navigation menu

To integrate:
1. Update navigation links in other pages to point to the chatbot
2. Ensure consistent styling across all pages
3. Test the mobile responsiveness

## Future Enhancements

- User authentication and progress tracking
- Multiple chatbot topics/specializations
- Voice input/output capabilities
- Integration with learning management systems
- Analytics and reporting features

## Support

For issues or questions:
1. Check this README for common solutions
2. Review the Flask and browser console logs
3. Verify your API keys and network connectivity
4. Test with the Streamlit version to isolate issues
