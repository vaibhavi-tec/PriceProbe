import streamlit as st
from streamlit_option_menu import option_menu


import Account, About, Feedback, Contact, Chatbot, Home


st.set_page_config(
        page_title="PriceProbe", layout="wide", page_icon=":heavy_dollar_sign:"
)

class MultiApp:

        def __init__(self):
                self.apps = []



        def add_app(self, title, func):

                self.apps.append({
                        "title": title,
                        "function": func
                })

        def run(self):
                # app = st.sidebar(
                with st.sidebar:
                        app = option_menu(
                                menu_title='PriceProbe',
                                options=['Home', 'Account', 'About', 'Feedback', 'Contact', 'ChatBot'],
                                icons=['house-fill', 'person-circle', 'info-circle-fill', 'gear-wide-connected', 'telephone-fill', 'chat-left-dots-fill'],
                                menu_icon='bag-heart',
                                default_index=1,
                                styles={
                                        "container": {"padding": "5!important", "background-color": '#403B83'},
                                        "icon": {"color": "white", "font-size": "23px"},
                                        "nav-link": {"color": "white", "font-size": "20px", "text-align": "left",
                                                     "margin": "0px", "--hover-color": "#36316D"},
                                        "nav-link-selected": {"background-color": "#797AC5"}

                                }

                        )

                if app == "Home":
                        Home.app()
                if app == "Account":
                        Account.app()
                if app == "About":
                        About.app()
                if app == 'Feedback':
                        Feedback.app()
                if app == 'Contact':
                        Contact.app()
                if app == 'ChatBot':
                        Chatbot.app()

multi_app = MultiApp()
# Add Chatbot as an app
multi_app.add_app('ChatBot', Chatbot.app)
# Run the app
multi_app.run()

custom_css = """
<style>
[data-testid="stSidebar"] > div:first-child {
    background-color: #797AC5; /* Sidebar background color */
}
.sidebar-image {
    width: 40px; /* Adjust width as needed */
    height: 0.2px; /* Maintain aspect ratio */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# Assuming your image is named 'sidebar_image.png' and located in an 'images' folder within your project
image_path = 'Images/Slide.png'
st.sidebar.image(image_path, use_column_width=True)