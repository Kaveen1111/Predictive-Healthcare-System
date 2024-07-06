import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Function to fetch and display health data
def fetch_health_data():
    st.subheader('Health Data Input')
    # Input symptoms and medical history
    symptoms = st.text_area('Enter your symptoms (comma-separated)', '')
    medical_history = st.text_area('Enter your medical history', '')
    
    health_data = {
        'symptoms': [symptom.strip() for symptom in symptoms.split(',') if symptom.strip()],
        'medical_history': medical_history.strip(),
        # Add more fields for wearables or additional health data if needed
    }
    return health_data

# Function for AI prediction
def ai_prediction(health_data):
    if not health_data['symptoms'] and not health_data['medical_history']:
        return "Please provide your symptoms or medical history to predict health issues."
    
    # Example using OpenAI GPT-4 model for text input
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "I have symptoms of " + ', '.join(health_data['symptoms'])},
            {"role": "user", "content": "My medical history includes: " + health_data['medical_history']}
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content

# Function for mental health support chatbot
def mental_health_chatbot(user_name, user_input):
    if not user_name:
        return "Please provide your name to proceed."
    
    # Construct messages for the chatbot
    messages = [
        {"role": "system", "content": "You are a helpful and empathetic mental health support chatbot."},
        {"role": "user", "content": f"My name is {user_name}. I am feeling {user_input}."}
    ]

    # Generate response using OpenAI GPT-4 model
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150,
    )
    
    return response.choices[0].message.content

# Main Streamlit application
def main():
    st.title('Predictive Healthcare and Mental Health Support System')

    # Ask for user's name
    user_name = st.text_input('Please enter your name:')
    
    # Fetch and display health data
    health_data = fetch_health_data()

    # Perform AI prediction for health issues
    st.subheader('Health Issue Prediction')
    prediction_text = ai_prediction(health_data)
    st.write('Prediction:', prediction_text)

    # Chatbot for mental health support
    st.subheader('Mental Health Support Chatbot')
    user_input = st.text_input('How are you feeling today?')

    # Generate chatbot response
    if user_input:
        st.write('Chatbot Response:')
        chatbot_response = mental_health_chatbot(user_name, user_input)
        st.write(chatbot_response)

# Run the main function
if __name__ == '__main__':
    main()
                              
