"""
Author: Rohini
Email: rolearnings@yahoo.com
Date: 2025-10-10
Description: This script intened to have chat from the UI using streamlit
"""
            

class InvalidInputError(Exception):
    def __init__(self, value, message="Invalid input provided"):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: '{self.value}' was provided."

