import streamlit as st

# CSS styling for the iframe to set width, height, and center it
iframe_html = """
    <style>
        .iframe-container {
            margin-left:-300px;
        }
        
        iframe {
            width: 1300px;
            height: 800px;
            
        }
    </style>
    <div class="iframe-container">
        <iframe src='http://localhost:3000/'></iframe>
    </div>
"""

# Display the styled iframe in Streamlit
st.markdown(iframe_html, unsafe_allow_html=True)
