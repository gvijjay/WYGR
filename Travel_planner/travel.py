import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from wygr.agents.travel_planner import ( generate_itinerary_tool,
    get_location_info_tool, parse_user_input
)

load_dotenv()

# Load API keys
weather_api_key = os.getenv("WEATHER_API_KEY")
geolocation_api_key = os.getenv("GEOLOCATION_API_KEY")
openai_api_key = os.getenv("OPEN_API_KEY")

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5, openai_api_key=openai_api_key)

st.title("Travel Planner")

user_prompt = st.text_input("Enter your travel request (e.g., 'Travel plan to Paris for 5 days.')")

if st.button("Generate Plan"):
    if user_prompt:
        destination, days = parse_user_input(user_prompt)
        if destination:
            location_info = get_location_info_tool(destination, geolocation_api_key, weather_api_key)
            if isinstance(location_info, str):
                st.error(location_info)
            else:
                context = {
                    "lat": location_info["lat"],
                    "lon": location_info["lon"],
                    "weather": location_info["weather"]
                }
                itinerary = generate_itinerary_tool(destination, days, context, llm)
                st.subheader("Your Travel Itinerary")
                st.write(itinerary)
        else:
            st.error("Error: Invalid input format.")
    else:
        st.warning("Please enter a travel request.")
