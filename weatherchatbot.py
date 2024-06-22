import os
import requests
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tkinter as tk
from tkinter import scrolledtext
import logging
import speech_recognition as sr
import pyttsx3

# Initialize NLTK resources
nltk.download("punkt")
nltk.download("stopwords")

class AdvancedChatbot:
    def __init__(self, root):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY", '3addda958fba07cae40c853004740f67')
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.air_quality_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.stop_words = set(stopwords.words("english"))
        self.stemmer = PorterStemmer()
        self.analyzer = SentimentIntensityAnalyzer()
        self.context = {}

        self.greeting_keywords = ["hello", "hi", "greetings", "hey", "hola"]
        self.greeting_responses = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! How can I help you?",
            "Hey! What do you need assistance with?",
            "Hola! How can I support you today?"
        ]

        self.knowledge_base = {
            "climate change": (
                "Climate change refers to significant changes in global temperatures and weather patterns over time. "
                "While climate change is a natural phenomenon, scientific evidence shows that human activities have "
                "accelerated these changes, primarily due to the burning of fossil fuels, deforestation, and industrial processes. "
                "These activities increase the concentration of greenhouse gases in the atmosphere, leading to global warming, "
                "melting polar ice, rising sea levels, and more frequent extreme weather events."
            ),
            "reduce carbon footprint": (
                "You can reduce your carbon footprint by:\n"
                "- Using public transportation, carpooling, biking, or walking instead of driving alone.\n"
                "- Reducing energy consumption at home by using energy-efficient appliances and lighting, and by insulating your home.\n"
                "- Supporting and using renewable energy sources like solar, wind, and hydro power.\n"
                "- Reducing, reusing, and recycling to minimize waste.\n"
                "- Eating a plant-based diet or reducing meat consumption, as livestock farming produces significant greenhouse gases.\n"
                "- Supporting sustainable products and businesses that prioritize environmental responsibility."
            ),
            "recycling": (
                "Recycling involves converting waste into reusable material. It helps conserve natural resources, "
                "reduce pollution, and lower greenhouse gas emissions. For example:\n"
                "- Paper can be recycled into new paper products, saving trees and water.\n"
                "- Plastics can be recycled into new plastic products, reducing the need for new plastic production.\n"
                "- Metals like aluminum and steel can be recycled indefinitely without losing quality.\n"
                "- Glass can be recycled into new glass products, conserving raw materials and energy."
            ),
            "renewable energy": (
                "Renewable energy comes from natural sources that are constantly replenished, such as solar, wind, hydro, "
                "geothermal, and biomass energy. Using renewable energy reduces dependence on fossil fuels and helps combat "
                "climate change by lowering greenhouse gas emissions. Examples include:\n"
                "- Solar power: converting sunlight into electricity using solar panels.\n"
                "- Wind power: using wind turbines to generate electricity.\n"
                "- Hydropower: generating electricity from flowing or falling water.\n"
                "- Geothermal energy: using heat from the Earth's interior for heating and electricity generation.\n"
                "- Biomass energy: producing energy from organic materials like plant and animal waste."
            ),
            "sustainable practices": (
                "Sustainable practices are actions and strategies that meet current needs without compromising the ability of "
                "future generations to meet their own needs. They include:\n"
                "- Reducing waste by recycling and composting.\n"
                "- Conserving water through efficient usage and reducing wastage.\n"
                "- Supporting local and sustainable products to reduce carbon emissions from transportation.\n"
                "- Using energy-efficient appliances and lighting to reduce energy consumption.\n"
                "- Choosing sustainable transportation options like biking, walking, carpooling, or using public transit."
            ),
            "air pollution": (
                "Air pollution is the presence of harmful substances in the atmosphere, which can come from natural sources "
                "like wildfires or human activities such as vehicle emissions, industrial processes, and burning fossil fuels. "
                "Air pollution can cause health problems, harm the environment, and contribute to climate change. Key pollutants "
                "include particulate matter (PM), nitrogen oxides (NOx), sulfur dioxide (SO2), carbon monoxide (CO), and volatile "
                "organic compounds (VOCs). Reducing air pollution involves:\n"
                "- Using cleaner energy sources like renewables.\n"
                "- Improving fuel efficiency and emissions standards for vehicles.\n"
                "- Implementing regulations to control industrial emissions.\n"
                "- Encouraging public transportation and reducing reliance on single-occupancy vehicles."
            ),
            "air quality measured": (
                "Air quality is measured using various instruments that detect and quantify the presence of pollutants in the air. "
                "Some common pollutants that are measured include:\n"
                "- Particulate Matter (PM): This includes tiny particles suspended in the air, which can be harmful to human health when inhaled.\n"
                "- Nitrogen Dioxide (NO2): This gas is emitted from vehicles, power plants, and industrial processes, and it can contribute to respiratory issues and smog formation.\n"
                "- Sulfur Dioxide (SO2): Mainly emitted from industrial processes and burning fossil fuels, it can cause respiratory problems and contribute to acid rain.\n"
                "- Carbon Monoxide (CO): This colorless, odorless gas is produced by incomplete combustion of fossil fuels and can be toxic when inhaled in high concentrations.\n"
                "- Ozone (O3): While ozone in the upper atmosphere (stratosphere) is beneficial for blocking harmful UV radiation, ground-level ozone is a pollutant formed by chemical reactions between pollutants in the presence of sunlight. It can cause respiratory issues and damage vegetation.\n"
                "- Volatile Organic Compounds (VOCs): These are a diverse group of chemicals emitted from various sources, including vehicle exhaust, industrial processes, and household products. They can contribute to the formation of smog and have adverse health effects.\n"
                "Air quality monitoring stations use specialized equipment to measure the concentrations of these pollutants in the air. Data from these stations are often used to calculate the Air Quality Index (AQI), which provides a numerical value representing the overall air quality and its potential health effects."
            ),
            "water conservation": (
                "Water conservation involves strategies and activities to manage fresh water as a sustainable resource. This includes:\n"
                "- Fixing leaks and using water-efficient fixtures.\n"
                "- Reducing water usage in landscaping by using drought-resistant plants and efficient irrigation.\n"
                "- Collecting and reusing rainwater for gardening and other non-potable uses.\n"
                "- Using water-saving techniques in agriculture, such as drip irrigation.\n"
                "- Raising awareness about the importance of water conservation and encouraging responsible water use."
            ),
            "biodiversity": (
                "Biodiversity refers to the variety of life on Earth at all its levels, from genes to ecosystems, and the ecological "
                "and evolutionary processes that sustain it. Biodiversity is crucial for ecosystem resilience, providing food, clean water, "
                "medicines, and other ecosystem services. Threats to biodiversity include habitat destruction, climate change, pollution, "
                "overexploitation, and invasive species. Protecting biodiversity involves:\n"
                "- Conserving natural habitats and restoring degraded ecosystems.\n"
                "- Reducing pollution and mitigating climate change.\n"
                "- Sustainable management of natural resources.\n"
                "- Supporting conservation efforts and policies aimed at protecting endangered species."
            ),
            "global warming": (
                "Global warming refers to the long-term rise in the average temperature of the Earth's climate system. It is a major aspect "
                "of climate change and is primarily caused by increased levels of greenhouse gases from human activities, such as burning "
                "fossil fuels, deforestation, and industrial processes. Consequences of global warming include rising sea levels, more frequent "
                "and severe heatwaves, changing precipitation patterns, and disruptions to ecosystems. Mitigating global warming involves:\n"
                "- Reducing greenhouse gas emissions through cleaner energy sources and improved energy efficiency.\n"
                "- Enhancing carbon sinks like forests and oceans that absorb CO2.\n"
                "- Promoting sustainable agricultural and land-use practices.\n"
                "- Raising awareness and encouraging actions to reduce individual and collective carbon footprints."
            ),
            "ocean pollution": (
                "Ocean pollution involves harmful substances such as chemicals, plastics, and other waste materials entering the ocean. "
                "It threatens marine life, disrupts ecosystems, and poses risks to human health. To combat ocean pollution, strategies include:\n"
                "- Reducing plastic usage and improving waste management to prevent littering.\n"
                "- Promoting recycling and the use of biodegradable materials.\n"
                "- Implementing regulations to control industrial discharge and agricultural runoff.\n"
                "- Supporting ocean cleanup efforts and initiatives to protect marine habitats.\n"
                "- Raising awareness about the impacts of ocean pollution and encouraging responsible behaviors."
            )
        }

        # GUI setup
        self.root = root
        self.root.title("Advanced Chatbot")
        self.root.geometry("600x400")

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        self.user_input = tk.Entry(root)
        self.user_input.pack(padx=10, pady=10, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.process_input)

        self.voice_button = tk.Button(root, text="Speak", command=self.process_voice_input)
        self.voice_button.pack(padx=10, pady=10)

        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

    def process_input(self, event):
        user_message = self.user_input.get()
        self.user_input.delete(0, tk.END)
        self.display_message("You", user_message)
        self.respond_to_query(user_message)

    def process_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for voice input...")
            audio = recognizer.listen(source)
        
        try:
            user_message = recognizer.recognize_google(audio)
            self.display_message("You", user_message)
            self.respond_to_query(user_message)
        except sr.UnknownValueError:
            self.display_message("System", "Sorry, I could not understand what you said.")
            self.tts_engine.say("Sorry, I could not understand what you said.")
            self.tts_engine.runAndWait()
        except sr.RequestError:
            self.display_message("System", "Sorry, my speech recognition service is down.")
            self.tts_engine.say("Sorry, my speech recognition service is down.")
            self.tts_engine.runAndWait()

    def display_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def respond_to_query(self, query):
        words = word_tokenize(query.lower())
        filtered_words = [self.stemmer.stem(word) for word in words if word not in self.stop_words]

        if any(greeting in filtered_words for greeting in self.greeting_keywords):
            response = self.get_greeting_response()
        elif "weather" in filtered_words:
            response = self.get_weather_response(query)
        elif "forecast" in filtered_words:
            response = self.get_forecast_response(query)
        elif "air" in filtered_words and "quality" in filtered_words:
            response = self.get_air_quality_response(query)
        else:
            response = self.get_knowledge_response(query)

        self.display_message("Bot", response)
        self.tts_engine.say(response)
        self.tts_engine.runAndWait()

    def get_greeting_response(self):
        return random.choice(self.greeting_responses)

    def get_weather_response(self, query):
        location = self.extract_location(query)
        if location:
            weather_data = self.fetch_weather(location)
            if weather_data:
                return self.format_weather_response(weather_data)
            else:
                return "Sorry, I couldn't retrieve the weather information at the moment."
        else:
            return "Please specify a location for the weather information."

    def get_forecast_response(self, query):
        location = self.extract_location(query)
        if location:
            forecast_data = self.fetch_forecast(location)
            if forecast_data:
                return self.format_forecast_response(forecast_data)
            else:
                return "Sorry, I couldn't retrieve the forecast information at the moment."
        else:
            return "Please specify a location for the forecast information."

    def get_air_quality_response(self, query):
        location = self.extract_location(query)
        if location:
            air_quality_data = self.fetch_air_quality(location)
            if air_quality_data:
                return self.format_air_quality_response(air_quality_data)
            else:
                return "Sorry, I couldn't retrieve the air quality information at the moment."
        else:
            return "Please specify a location for the air quality information."

    def get_knowledge_response(self, query):
        for key, value in self.knowledge_base.items():
            if key in query.lower():
                return value
        return "I'm sorry, I don't have information on that topic. Can I help with something else?"

    def extract_location(self, query):
        tokens = query.split()
        for i, token in enumerate(tokens):
            if token.lower() in ["in", "at", "for", "of"]:
                if i + 1 < len(tokens):
                    return tokens[i + 1]
        return None

    def fetch_weather(self, location):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.weather_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_forecast(self, location):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.forecast_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_air_quality(self, location):
        # Assume we have a method to get latitude and longitude from location
        lat, lon = self.get_lat_lon(location)
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key
        }
        response = requests.get(self.air_quality_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_lat_lon(self, location):
        # Dummy implementation, replace with actual geocoding if necessary
        return 0, 0

    def format_weather_response(self, data):
        description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        city = data["name"]
        return
