import streamlit as st
import pandas as pd
import requests
#import plotly.graph_objects as go


st.set_page_config(page_title="ICU Watch - Sepsis Prediction", layout="wide")

st.markdown("""
<style>
    .reportview-container .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        color: white;
        background-color: #4FC3F7; /* Light blue */
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #29B6F6; /* Slightly darker blue */
    }
    .css-1d391kg {
        background-color: #4FC3F7 !important; /* Light blue */
    }
    .css-18e3th9 {
        color: #4FC3F7 !important; /* Light blue */
    }
</style>
""", unsafe_allow_html=True)

API_URL = "https://api-fcf7rbbebq-ew.a.run.app/"
predict_url = f"{API_URL}/predict"

st.title("🏥 ICU Watch - Sepsis Prediction")
st.header("Welcome to our prediction service")
st.markdown("""
Our platform leverages advanced data science to provide predictions and insights,
enhancing patient care and operational efficiency. Our goal is to predict Sepsis 6
hours prior to appearance.""")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type="csv")


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        seqs = []

        for i in range(len(df)-5):
            seqs.append(df[i:i+6].to_csv().encode("utf-8"))

        st.success("File successfully uploaded!")

        # st.subheader("Preview of uploaded data:")
        # st.dataframe(df)

        if st.button("🔮 Get Prediction"):
            with st.spinner('Processing your data...'):
                uploaded_file.seek(0)

                pred_list = []
                for sequence in seqs:

                    files = {'file': sequence}

                    response = requests.post(predict_url, files=files)
                    response.raise_for_status()

                    prediction = response.json().get('predictions')
                    pred_list.append(round(100*prediction[0],1))

                pred_df =df[5:]
                pred_df['Sepsis_Prediction%']=pred_list

                st.subheader("Prediction:")
                st.write("Sepsis probability percentage on each hour")
                st.dataframe(pred_df)
                st.success("🎉 Prediction successful!")

                csv = pred_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Data with Prediction as CSV",
                    data=csv,
                    file_name="patient_data_with_prediction.csv",
                    mime="text/csv",
                )

    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    st.info("👆 Please upload a CSV file to get a prediction.")

st.markdown("---")
st.markdown("© 2024 ICU Watch. All rights reserved.")
