# Advanced Chatbot

This is an advanced chatbot application built with Python, featuring both text and voice input capabilities. It can provide weather information, weather forecasts, air quality data, and answers to environmental queries. The bot utilizes APIs for real-time data and includes a knowledge base for specific environmental topics.

## Features

- **Text Input**: Interact with the bot using text input via a GUI.
- **Voice Input**: Interact with the bot using voice commands.
- **Text-to-Speech**: The bot can read its responses aloud.
- **Weather Information**: Get current weather details for a specified location.
- **Weather Forecast**: Get a weather forecast for the next few days.
- **Air Quality Information**: Get the current air quality index for a specified location.
- **Environmental Knowledge Base**: Ask about specific environmental topics and get detailed responses.

## Installation

1. **Clone the repository**:
    ```bash
    [git clone https://github.com/yourusername/advanced-chatbot.git
    cd advanced-chatbot](https://github.com/manjeet34/Wrather_Chatbot/blob/main/weatherchatbot.py)
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Download NLTK data**:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('stopwords')
    ```

5. **Insert your OpenWeatherMap API key**:
    - Sign up at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) to get your API key.
    - Create a file named `config.py` in the root directory of the project.
    - Add the following line to `config.py`:
    ```python
    OPENWEATHERMAP_API_KEY = 'your_openweathermap_api_key_here'
    ```

## Usage

1. **Activate the virtual environment** (if not already activated):
    ```bash
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. **Run the application**:
    ```bash
    python chatbot.py
    ```

3. **Interact with the bot**:
    - Type your message in the text input field and press Enter.
    - Click the "Speak" button to provide voice input.
    - The bot will respond in the chat display area and will read its responses aloud.

## Example Queries

- **Greeting**:
    - "Hello"
    - "Hi"
- **Weather Information**:
    - "What's the weather in New York?"
    - "Tell me the weather in London"
- **Weather Forecast**:
    - "What's the weather forecast for Paris?"
    - "Give me the forecast for Tokyo"
- **Air Quality Information**:
    - "What's the air quality in Beijing?"
    - "Tell me the air quality in San Francisco"
- **Environmental Knowledge**:
    - "Tell me about global warming"
    - "What are the effects of plastic pollution?"

## Dependencies

- `nltk`
- `requests`
- `tkinter`
- `speech_recognition`
- `pyttsx3`
- `vaderSentiment`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Author

- [Manjeet Nagar](https://github.com/manjeet34)
