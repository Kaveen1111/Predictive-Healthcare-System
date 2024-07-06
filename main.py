import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Function to fetch and display health data
def fetch_health_data():
    st.subheader('Health Data Input')
    # Input symptoms and medical history
    symptoms = st.text_area('Enter your symptoms or describe how you feel', '')
    medical_history = st.text_area('Enter your medical history', '')
    
    health_data = {
        'symptoms': symptoms.strip(),
        'medical_history': medical_history.strip(),
        # Add more fields for wearables or additional health data if needed
    }
    return health_data

# Function for AI prediction with more advanced medical knowledge
def ai_prediction(health_data):
    if not health_data['symptoms']:
        return "Please provide your symptoms to predict health issues."
    
    # Example using OpenAI GPT-4 model for text input
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"My symptoms are: {health_data['symptoms']}. My medical history is: {health_data['medical_history']}"},
            {"role": "system", "content": "Provide a detailed medical analysis and suggest potential diagnoses and treatments."}
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content

# Function for mental health support chatbot with continuous conversation
def mental_health_chatbot(conversation_history):
    # Construct messages for the chatbot
    messages = [{"role": role, "content": content} for role, content in conversation_history]

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

    # Initialize conversation history in session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Chatbot for mental health support
    st.subheader('Mental Health Support Chatbot')
    
    # Display previous conversation
    for i, (role, content) in enumerate(st.session_state.conversation_history):
        st.write(f"{role.capitalize()}: {content}")

    # User input
    user_input = st.text_input('You:', key=f'user_input_{len(st.session_state.conversation_history)}')

    if user_input:
        # Add user input to conversation history
        st.session_state.conversation_history.append(('user', f"My name is {user_name}. I am feeling {user_input}."))

        # Generate chatbot response
        chatbot_response = mental_health_chatbot(st.session_state.conversation_history)
        st.write('Chatbot Response:', chatbot_response)

        # Add chatbot response to conversation history
        st.session_state.conversation_history.append(('assistant', chatbot_response))

# Run the main function
if __name__ == '__main__':
    main()
                              
