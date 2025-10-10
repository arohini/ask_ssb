"""
Author: Rohini
Email: rolearnings@yahoo.com
Date: 2025-10-10
Description: This script intened to have chat from the UI using streamlit
"""

import streamlit as st
import requests

# class DocumentModelConnector:
#     """
#     DocumentModel
#     """
#     def __init__(self, model_name, model_url, model_url_timeout):
#         self.model_name = model_name
#         self.model_url = model_url
#         self.model_url_timeout = model_url_timeout


class LifeLight():
    """
    ModelQuery
    """
    def __init__(self, model_name, model_url, model_url_timeout):
        self.model_name = model_name
        self.model_url = model_url
        self.model_url_timeout = model_url_timeout
        self._prompt = None

    def query_ollama(self, prompt: str) -> str:
        """
        For the prompt given, it will query the Model and return back the response

        Args:
            prompt (str): Question from the user

        Returns:
            str: Either response received from the model or no response
        """
        self._prompt = prompt
        payload = {
            "model": self.model_name,
            "prompt": self._prompt,
            "stream": False
        }

        try:
            ollama_response = requests.post(self.model_url, json=payload, timeout=self.model_url_timeout)
            ollama_response.raise_for_status()
            received_data = ollama_response.json()
            return received_data.get("response", "No response.")
        except requests.exceptions.RequestException as e:
            return f"Error retrieving the data: {e}"

    # Streamlit UI
    def chat_box(self):
        """
        A simple chat box to enter the user question and receive the response
        
        """
        try:
            st.title("🧘 Sri Sai Satcharita Q&A")
            st.markdown("Ask any question based on Sai Baba's teachings.")
            # # Path to your image file
            # image_path = "assets/Application/ssb.jpg" 

            # # Add the image to the sidebar
            # st.sidebar.image(image_path, width="stretch", title= "Om Sai Ram")

            question = st.text_input("Your question:")

            if st.button("Ask"):
                if question.strip() == "":
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Thinking..."):
                        response = self.query_ollama(question)
                    st.success("Answer:")
                    st.write(response)
        except Exception as e:
            print(f"Error writing the response to chat window {str(e)}")

if __name__ == "__main__":
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "mistral"
    MODEL_TIMEOUT = 300
    mq = LifeLight(MODEL_NAME, OLLAMA_URL,MODEL_TIMEOUT)
    mq.chat_box()
