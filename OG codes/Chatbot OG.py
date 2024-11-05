import streamlit as st
import base64
import speech_recognition as sr
from comparison import compare_prices


def app():
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    img = get_img_as_base64("Images/chatbot bg.png")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url("data:Images/chatbot bg.png;base64,{img}");
    background-size: cover;
    opacity: 100%;
    z-index: -1;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Welcome message
    st.write("Welcome to the E-commerce Price Comparison Chatbot!")

    # Add a radio button for input method selection
    input_method = st.radio("Select input method:", ("Text", "Speech"))

    if input_method == "Speech":
        # Speech recognition using microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio = r.listen(source)
        try:
            st.write("Processing...")
            user_input = r.recognize_google(audio)
            st.write(f"You said: {user_input}")
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
    else:
        user_input = st.text_input("You:", key="user_input_chatbot")

    while True:
        if not user_input:
            continue

        if any(word in user_input.lower() for word in ["bye", "see you later", "goodbye"]):
            st.write("Thank you for using the E-commerce Price Comparison Chatbot. Goodbye!")
            break
        elif any(
                word in user_input.lower() for word in ["nice chatting to you, bye", "see you till next time", "exit"]):
            st.write("Bye! Have a nice day, come back again soon.")
            break

        # Rule 2: Greeting
        if any(word in user_input.lower() for word in ["hi", "hello", "hey", "good day", "hola"]):
            st.write("Chatbot: Hello, thanks for asking!")
        elif any(word in user_input.lower() for word in ["how are you"]):
            st.write("Chatbot: I am fine, how are you?")
        elif any(word in user_input.lower() for word in ["hi there", "is anyone there?"]):
            st.write("Chatbot: Hi there, how can I help?")
        elif any(word in user_input.lower() for word in ["goodbye", "bye", "see you later", "nice chatting to you"]):
            st.write("Chatbot: Thank you for using the E-commerce Price Comparison Chatbot. Goodbye!")
            break

        # Rule 2: Providing help
        if any(word in user_input.lower() for word in ["help", "support", "guide"]):
            st.write(
                "Chatbot: I can guide you through different websites and find great offers for the products you want to buy.")
        elif any(word in user_input.lower() for word in
                 ["what you can do", "what help you provide", "what support is offered"]):
            st.write("Chatbot: Offering support to get the best deal out of your purchase.")

        # Rule 3: Websites comparison
        if any(word in user_input.lower() for word in ["websites", "compare with", "how many websites"]):
            st.write("Chatbot: Comparing products from Flipkart, Amazon, and Croma...")

        # Rule 4: Product comparison
        if any(word in user_input.lower() for word in ["find best deal", "product comparison"]):
            st.write("Sure, please provide me with the product names or keywords you want to compare.")
        elif any(word in user_input.lower() for word in ["compare products", "product comparison", "which one is better", "compare"]):
            product_name = st.text_input("Chatbot: What product would you like to compare prices for?")
            if product_name:
                lowest_price, _ = compare_prices(product_name)
                if isinstance(lowest_price, str):
                    st.write(lowest_price)
                else:
                    st.write(f"The lowest price found is ₹{lowest_price}.")

                st.write("")
                st.write("Here are the URLs for your comparison:")
                st.write("Flipkart:", f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}')
                st.write("Amazon:",
                         f'https://www.amazon.in/{product_name.replace(" ", "-")}/s?k={product_name.replace(" ", "+")}')
                st.write("Croma:", f'https://www.croma.com/search/?text={product_name.replace(" ", "-")}')
                st.write("")

                more_queries = st.text_input(
                    "Chatbot: Would you like to compare prices for another product? (yes/no)").lower()
                if any(word in more_queries for word in ["no", "bye", "see you later", "goodbye"]):
                    # Rule 7
                    st.write("Bye! Have a nice day, come back again soon.")
                    break
                elif any(word in more_queries for word in
                         ["nice chatting to you, bye", "see you till next time", "exit"]):
                    st.write("Thank you for using the E-commerce Price Comparison Chatbot. Goodbye!")
                    break
                else:
                    st.write("See you!")

        # Rule 5: Thank you
        if any(word in user_input.lower() for word in ["thanks", "thank you", "that's helpful", "awesome, thanks"]):
            st.write("Chatbot: Happy to help!")


# Remember to call the app function to display the app
if __name__ == "__main__":
    app()




