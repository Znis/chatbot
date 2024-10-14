import streamlit as st
import requests
import json

# Function to call the API
def get_chat_response(user_input):
    api_url = st.secrets['API_ENDPOINT']
    headers = {
        "ngrok-skip-browser-warning": "1",
        "Content-Type": "application/json"
    }
    payload = {
        "model": st.secrets['MODEL'],
        "messages": [
                    { "role": "user", "content": user_input }
                ],
        "stream": True
            }       
    
    with requests.post(api_url, json=payload, headers=headers, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    yield json.loads(data)
        else:
            yield {"error": f"Error: {response.status_code} - {response.text}"}    
    if response.status_code == 200:
        return response.json().get('response', 'No response from API')
    else:
        return f"Error: {response.status_code} - {response.text}"

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot similar to ChatGPT. It is just an uncensored conversational",
    "bot with no access to internet or any other tool. Please don't be too naughty. 😛😛"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Ask anything"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Generating response..."):
        stream = get_chat_response(prompt)
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})


