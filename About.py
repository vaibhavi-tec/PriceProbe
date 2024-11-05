import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_chat = load_lottieurl("https://lottie.host/5ffa2a08-5d35-471b-9bfd-0674c8f6e509/LpYaKfQbPj.json")
goal_img = Image.open("Images/about img.png")


def app():
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Introduction to the Team")
            st.write("##")
            st.write(
            """
            Our team at priceProbe is a dedicated group of individuals with a passion for technology and e-commerce. 
            From software engineers to data scientists, each member brings a unique skillset that drives our mission to provide top-notch service to our customers.
            Together, we work tirelessly to enhance the user experience and deliver exceptional results.
            """
             )

        with right_column:
            st_lottie(lottie_chat, height=300, key="coding")
    with st.container():
        st.write(" --- ")

        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.write(goal_img)

        with text_column:
            st.header("Purpose and Goals")
            st.write("##")
            st.write("""
            Our primary goal at priceProbe is to offer our customers a seamless shopping experience by 
            comparing prices from various websites and providing personalized recommendations based on their preferences.
            We strive to help our customers save time and money by ensuring they receive the best deals available in the market.
            """)

    with st.container():
        st.write(" --- ")
        text_column, image_column = st.columns((2, 1))
        with text_column:
            st.header("Offerings")
            st.write("##")
            st.write("""
            At priceProbe, we offer a wide range of products across various categories, including electronics, fashion, home goods, and more.
            Our platform uses machine learning algorithms to analyze pricing data and make personalized recommendations to help you find the best deals.
            With our user-friendly interface, shopping has never been easier.

            """)
        with image_column:
            st.write(goal_img)

    st.image('Images/Websites.png', caption='Websites Available in our website', use_column_width=True)




# Remember to call the app function to display the app
if __name__ == "__main__":
    app()
