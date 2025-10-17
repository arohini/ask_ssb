"""
Author: Rohini
Email: rolearnings@yahoo.com
Date: 2025-10-10
Description: This script intened to have chat from the UI using streamlit
"""

import streamlit as st
from annotated_text import annotated_text
from deep_translator import GoogleTranslator
from ssb_values import *
import requests
import re


class LifeLight():
    """
    ModelQuery
    """
    def __init__(self, model_name, model_url, model_url_timeout):
        self.model_name = model_name
        self.model_url = model_url
        self.model_url_timeout = model_url_timeout
        self._prompt = None

    def query_ollama(self, prompt: str, lang_pref: str='English') -> str:
        """
        For the prompt given, it will query the Model and return back the response

        Args:
            prompt (str): Question from the user

        Returns:
            str: Either response received from the model or no response
        """
        self._prompt = prompt
        self.lang_pref = lang_pref.lower()
        payload = {
            "model": self.model_name,
            "prompt": self._prompt,
            "stream": False
        }

        try:
            ollama_response = requests.post(self.model_url, json=payload, timeout=self.model_url_timeout)
            ollama_response.raise_for_status()
            received_data = ollama_response.json()
            retrieved_response = received_data.get("response", "No response.")
            try:
                translated_text = self.translate_text(retrieved_response, self.lang_pref)
            except Exception as e:
                print(f"Unable to translate text {e}")

            return translated_text
        except requests.exceptions.RequestException as e:
            return f"Error retrieving the data: {e}"

    def translate_text(self, text, target_lang="ta"):
        """
        For the provided promt text and based on the target language,
        text is converted and sent bask as an response
        """
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text)
        except Exception as e:
            print(f"Unable to translate the text: {text} due to {str(e)}")
    
    def keyword_highlight(self, text: str, word: str, color: str) -> str:
        """
        For the text, keywords provided finds the match of the keyword and
        then with corresponding colors provided it is highligted using markdown

        Args:
            text (str): _description_
            word (str): _description_
            color (str): _description_

        Returns:
            str: _description_
        """
        highlighted_txt = text
        # Highlight function: wrap matched words in a <span>
        try:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            highlighted_txt = pattern.sub(
                lambda m: f"<span style='background-color: {color}; font-weight: bold;'>{m.group(0)}</span>",
                text
            )
            return highlighted_txt
        
        except Exception as e:
            print(f"Error highlighting the text {str(e)}")

    def add_legends(self):
        try:
            # Sidebar content
            st.sidebar.image("assets/Application/ssb.jpg", caption="Om Sai Ram", width='stretch')

            # Highlight map: word -> color
            highlight_map = {
                "Core Values": "#a0f0ed",     
                "Practices": "#ffc07a", 
                "Things Accepted": "#d5a6ff",  
                "Popular Sayings": "#ffd700"
            }

            # Add spacing below image
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🔍 Color Reference")

            # Display each legend item in the sidebar
            for word, color in highlight_map.items():
                st.sidebar.markdown(
                    f"""
                    <div style='display: flex; align-items: center; margin-bottom: 6px;'>
                        <div style='width: 16px; height: 16px; background-color: {color}; 
                                    border: 1px solid #000; margin-right: 8px;'></div>
                        <span style='font-size: 24px;'>{word}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except Exception as e:
            print(f"Error creating legends {str(e)}")

    def get_ssb_annotations(self) -> dict:
        """
        For the list of ssb_values respective annotations are tagged 
        and sent back as dict

        Returns:
            dict: dict of annotated text
        """
        try:
            ssb_annotations_keyword_mapping = {}
            for cv in ssb_core_values:
                ssb_annotations_keyword_mapping[cv] = "#a0f0ed"
            for prac in ssb_practices:
                ssb_annotations_keyword_mapping[prac] = "#ffc07a"
            for ta in ssb_things_accepted:
                ssb_annotations_keyword_mapping[ta] = "#d5a6ff"
            for sa in ssb_sayings:
                ssb_annotations_keyword_mapping[sa] = "#ffd700"

            return ssb_annotations_keyword_mapping

            # ssb_annotations_text = []
            # for cv in ssb_core_values:
            #     ssb_annotations_text.append((cv, "#a0f0ed"))
            # for prac in ssb_practices:
            #     ssb_annotations_text.append((prac, "#ffc07a"))
            # for ta in ssb_things_accepted:
            #     ssb_annotations_text.append((ta, "#d5a6ff"))
            # for sa in ssb_sayings:
            #     ssb_annotations_text.append((sa, "#ffd700"))
            # return ssb_annotations_text
            
        except Exception as e:
            print(f"Error fetching SSB annotations {str(e)}")



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
            lang_option = st.selectbox(
                 "Please choose the language",
                 ("English", "Marathi", "Tamil", "Hindi"),
                 )
            
            self.add_legends()
            
            if st.button("Ask"):
                if question.strip() == "":
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Thinking..."):
                        response = self.query_ollama(question, lang_option)
                    st.success("Answer:")
                    # st.write(response)

                    try:
                        concat_highlighted_text = ""

                        for word, color in self.get_ssb_annotations().items():
                            # Apply highlighting
                            concat_highlighted_text = self.keyword_highlight(response, word=word, color=color)
                            response = concat_highlighted_text
                    except Exception as e:
                        print(f"Error highlighting the keyword {e}")

                    try:   
                        if concat_highlighted_text:
                            # Display in Streamlit
                            st.markdown(concat_highlighted_text, unsafe_allow_html=True)
                        else:
                            st.write(response)
                        
                    except Exception as e:
                        print(f"Error writing respone after annotating {e}")

        except Exception as e:
            print(f"Error writing the response to chat window {str(e)}")

if __name__ == "__main__":
    OLLAMA_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "mistral"
    MODEL_TIMEOUT = 300
    mq = LifeLight(MODEL_NAME, OLLAMA_URL,MODEL_TIMEOUT)
    mq.chat_box()
