import streamlit as st

def app():
    st.title("Feedback")
    st.write("We would love to hear your feedback!")
    
    # Star rating slider
    st.subheader("Rate your experience (out of 5 stars):")
    rating = st.slider("", 1, 5, 3)  # Slider for rating from 1 to 5, default at 3
    
    # Convert rating to star symbols
    stars = '⭐' * rating
    
    # Display selected rating
    st.write("You selected:", stars)
    
    # Text area for feedback
    feedback = st.text_area("Please leave your feedback here:")
    
    if st.button("Submit Feedback"):
        # Process the feedback and rating (e.g., save to a database)
        st.success("Thank you for your feedback!")

# Run the app
if __name__ == "__main__":
    app()