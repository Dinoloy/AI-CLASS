import streamlit as st

st.title("BMI Calculator")

st.write("Enter your height and weight to calculate your BMI.")

name = st.text_input("Enter your name")

weight = st.number_input(
    "Enter your weight in kilograms",
    min_value=1.0,
    step=0.5
)

height_cm = st.number_input(
    "Enter your height in centimeters",
    min_value=50.0,
    step=1.0
)

if st.button("Calculate BMI"):

    height_m = height_cm / 100

    bmi = weight / (height_m ** 2)

    st.success(f"Hello {name}, your BMI is {bmi:.2f}")

    if bmi < 18.5:
        st.write("Category: Underweight")

    elif bmi < 25:
        st.write("Category: Normal weight")

    elif bmi < 30:
        st.write("Category: Overweight")

    else:
        st.write("Category: Obese")