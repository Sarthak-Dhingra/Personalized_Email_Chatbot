import streamlit as st
import groq
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()


# Read the bot role from the file
try:
    with open('100xEngineers.txt', 'r') as file:
        receiver_background = file.read().strip()
    if not receiver_background:
        receiver_background = "100xEngineers is an education company based in Bangalore, India that offers cohort-based programs to teach generative AI and software development skills." 
except FileNotFoundError:
    receiver_background = "100xEngineers is an education company based in Bangalore, India that offers cohort-based programs to teach generative AI and software development skills." 

# Try to get the API key from the environment variable
api_key = os.getenv("GROQ_API_KEY")

client = groq.Groq(api_key=api_key)
def generate_email(subject, word_count, tone, sender_name, receiver_name,receiver_background):
    prompt = f"""
    Write a personalized email to 100xEngineers (https://www.100xengineers.com/) with the following details:

    Subject: {subject}
    Word Count: Approximately {word_count} words
    Tone: {tone}
    Sender: {sender_name}
    Receiver: {receiver_name}

    Information about the receiver: {receiver_background}

    Structure the email as follows:
    1. Greeting
    2. Introduction of the project
    3. Key benefits and relevance to 100xEngineers
    4. Request for collaboration or next steps
    5. Closing

    Ensure the email is {tone} in tone and approximately {word_count} words long.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        stream=False,
    )

    return chat_completion.choices[0].message.content

# Streamlit UI
st.title("Personalized Email Generator for 100xEngineers")

subject = st.text_input("Enter the subject of the email:")
word_count = st.slider("Select the approximate word count:", 100, 500, 250)
tone = st.selectbox("Select the tone of the email:", ["Friendly", "Professional", "Persuasive"])
sender_name = st.text_input("Enter your name (sender):")
receiver_name = st.text_input("Enter the receiver's name:")

if st.button("Generate Email"):
    if subject and sender_name and receiver_name:
        email_content = generate_email(subject, word_count, tone.lower(), sender_name, receiver_name)
        st.subheader("Generated Email:")
        st.write(email_content)
    else:
        st.warning("Please fill in all the required fields.")
