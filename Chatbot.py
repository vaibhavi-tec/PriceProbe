import streamlit as st
import base64
from comparison import compare_prices

def app(user_input=None):
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
    opacity: 100%;  # Adjust the opacity as needed
    z-index: -1;  # Ensure it's in the background
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    .chat-container {{
        height: 400px;
        overflow-y: scroll;
    }}

    .chat-message-container {{
        padding: 5px;
        margin-bottom: 10px;
        border-radius: 10px;
        display: flex;
        align-items: center;
    }}

    
    .avatar {{
        width: 20px;
        height: 20px;
        border-radius: 20%;
        margin-right: 10px;
    }}


    .user-input {{
        margin-top: 20px;
        position: absolute;
        bottom: 10px;
        width: calc(100% - 40px);
    }}

    .send-icon {{
        position: absolute;
        bottom: 22px;
        right: 10px;
        cursor: pointer;
    }}
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Welcome message
    st.title('Welcome to :violet[PriceProbe] :sunglasses:')

    # Container for chat messages
    chat_container = st.container()
    with chat_container:
        st.write("")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "assistant":
                st.image(r"Images\chatbot_avatar.png", width=35, use_column_width=False)
                st.markdown("""
                <div style="padding: 10px; margin-bottom: 10px; max-width: 70%; border-radius: 10px; background-color: #7B7DBE; float: left;">
                <p>{}</p>
                </div>
                """.format(message["content"]), unsafe_allow_html=True)
            else:
                st.image(r"Images\user_avatar.png", width=35, use_column_width=False)
                st.markdown("""
                <div style="padding: 10px; margin-bottom: 10px; max-width: 70%; border-radius: 10px; background-color: #1B1464; float: right;">
                <p>You: {}</p>
                </div>
                """.format(message["content"]), unsafe_allow_html=True)

    # Accept user input
    user_input = st.text_input("You:", key="user-input")
    send_button = "<span class='send-icon'>&#x27A4;</span>"
    st.markdown(send_button, unsafe_allow_html=True)

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Rule 1: Greeting
        if any(word in user_input.lower() for word in ["hi", "hello", "hey", "good day", "hola"]):
            st.session_state.messages.append({"role": "assistant", "content": "Hi, I am Price probe ,How can I help you!"})

        # Rule 2: Greeting
        if any(word in user_input.lower() for word in ["how are you","how are you doing", "how are you?","How r u"]):
            st.session_state.messages.append({"role": "assistant", "content": "I am fine, how are you?"})

        # Rule 2: Greeting
        if any(word in user_input.lower() for word in ["I am fine","I am good", "I'm fyn","gud","Good","Great"]):
            st.session_state.messages.append({"role": "assistant", "content": "Happy to hear that, How can i help you!"})

        # Rule 3: Providing help
        if any(word in user_input.lower() for word in ["help", "support", "guide"]):
            st.session_state.messages.append({"role": "assistant", "content": "I can guide you through different websites and find great offers for the products you want to buy."})

        # Rule 4: Websites comparison
        if any(word in user_input.lower() for word in ["websites", "compare with", "how many websites"]):
            st.session_state.messages.append({"role": "assistant", "content": "Comparing products from Flipkart and Amazon..."})

        # Rule 5: Product comparison
        if any(word in user_input.lower() for word in ["find best deal", "product comparison"]):
            st.session_state.messages.append({"role": "assistant", "content": "Sure, please provide me with the product names or keywords you want to compare."})

        # Rule 6: Thank you
        if any(word in user_input.lower() for word in ["thanks", "thank you", "that's helpful", "awesome, thanks"]):
            st.session_state.messages.append({"role": "assistant", "content": "Happy to help!"})

        # Rule 7: Product comparison
        if any(word in user_input.lower() for word in ["compare products", "product comparison", "which one is better", "compare"]):
            product_name = st.text_input("Chatbot: What product would you like to compare prices for?")
            if product_name:
                lowest_price, urls = compare_prices(product_name)  # Modify to unpack only lowest_price and urls
                if lowest_price is not None:
                    # Display assistant response in chat message container
                    st.session_state.messages.append({"role": "assistant", "content": f"The lowest price found is ₹{lowest_price}"})

                    # Display lowest price platform URL
                    if urls:
                        st.session_state.messages.append({"role": "assistant", "content": f"Platform URL: {urls[min(urls, key=urls.get)]}"})

                    
                    st.session_state.messages.append({"role": "assistant", "content": "Here are the URLs for your comparison:"})
                    st.session_state.messages.append({"role": "assistant", "content": f"Flipkart: https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"})
                    st.session_state.messages.append({"role": "assistant", "content": f"Amazon: https://www.amazon.in/{product_name.replace(' ', '-')}/s?k={product_name.replace(' ', '+')}"})

                else:
                    # Display assistant response in chat message container
                    st.session_state.messages.append({"role": "assistant", "content": f"Flipkart: https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"})
        
        
        # Rule 8: Bye
        if any(word in user_input.lower() for word in ["Bye", "Good bye", "bye", "see you later", "nice chatting to you, bye", "see you till next time", "exit", "goodbye"]):
            st.session_state.messages.append({"role": "assistant", "content": "Thank you for using the E-commerce Price Comparison Chatbot. Goodbye!"})


# Remember to call the app function to display the app
if __name__ == "__main__":
    app()