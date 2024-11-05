import streamlit as st
import base64
from PIL import Image
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

goal_img = Image.open("Images/about img.png")
lottie_robo = load_lottieurl("https://lottie.host/163566a4-aa6a-4317-8da9-38488f3a179e/eHSnBc2526.json")

def app():

    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    img = get_img_as_base64("Images/main bg.png")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url("data:Images/home.png;base64,{img}");
    background-size: cover;
    opacity: 100%;  # Adjust the opacity as needed
    z-index: -1;  # Ensure it's in the background
    }}
    
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    .subheader-text {{
    font-style: Medium italic;
      /* Medium font weight */
    }}

    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    title = "PriceProbe"

    st.markdown(f"""
        <h1 
        style='color: #65F6FF;
         font-weight: Extra bold;
         font-size: 100px;'>
            {title}
        </h1>""", unsafe_allow_html=True)
    with st.container():
        st.write("##")
        st.markdown(
            """
            *Welcome to Price Probe, your go-to destination for E-commerce products at the lowest prices.
            We understand the importance of affordability without compromising on quality, 
            and we are here to make your online shopping experience more budget-friendly.*
            """
        )

    st.write("##")
    st.write("##")
    with st.container():
        st.write(" --- ")
        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.write(goal_img)

        with text_column:
            st.header("About Price Probe")
            st.write("##")
            st.write("""
            At Price Probe, we pride ourselves on offering a wide range of E-commerce products ranging from electronics to fashion,
            all carefully selected to provide you with the best value for your money. 
            Our team works tirelessly to ensure that our inventory is up-to-date with the latest trends and deals in the market.
            """)

    st.write("##")
    st.write("##")

    with st.container():
        st.write(" --- ")
        st.header("....Compares Websites....")
        st.image('Images/web_main.png', caption='Websites Available in our website', use_column_width=True)

    st.write("##")

    with st.container():
        st.write(" --- ")
        st.write("##")
        st.write("##")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("Product Categories")
            st.write("##")
            st.write(
                """
                Explore our diverse product categories to find exactly what you're looking for at a fraction of the cost.
                From gadgets and accessories to clothing and home essentials, Price Probe has everything you need and more.
                """
            )

        with right_column:
            st_lottie(lottie_robo, height=300, key="coding")



# Remember to call the app function to display the app
if __name__ == "__main__":
    app()


