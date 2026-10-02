import streamlit as st

st.title("My Streamlit App")

st.write("Hello, World!")

st.header("This is a Header")
st.subheader("This is a Subheader")

st.text("This is some text.")
st.markdown("This is **markdown** text.")

name = st.text_input(
    "Write your name here"
)

age = st.number_input(
    "Write your age here",
    min_value=0,
    step=1
)

value = st.slider(
    "Select a value",
    min_value=0,
    max_value=100,
    value=50,
    step=1
)

if st.button("Submit"):
    st.success("Button clicked!")

    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Selected value: {value}")