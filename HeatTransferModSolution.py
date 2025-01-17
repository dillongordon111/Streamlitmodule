import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title('Python Automation Module')
st.title('Example BTU Calculator')
st.markdown("""
<div style="padding: 0px; border-radius: 10px; border: 0px solid #ccc; width: 100%;">
    <h3 style="color: White;"></h3>
    For calculations using a .csv, make sure the columns are labelled Hour, Internal Temperature, and OAT.  
</div>
""", unsafe_allow_html=True)


upload_file = st.file_uploader(
    label="Upload CSV",
    type="csv",
    accept_multiple_files=False,
    key=None,
    help=None,
    disabled=False,
    label_visibility="visible"
)

if upload_file is not None:
    
    try:
        df = pd.read_csv(upload_file)
        st.dataframe(df, width=1800, height=400)

        
        # Clean column names to remove extra spaces
        df.columns = df.columns.str.strip()

        # Verify required columns
        required_columns = ['Hour', 'Internal Temperature', 'OAT']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}. Missing: {', '.join(missing_columns)}")


        else:
            # Extract columns
            column_Hour = df['Hour']
            column_Internal_Temperature = df['Internal Temperature']
            column_OAT = df['OAT']

            # Inputs
            gpm = st.number_input("Enter GPM", min_value=0.0, step=0.1, format="%.2f")
            gp = st.number_input("Enter Glycol %", min_value=0.0, max_value=100.0, step=1.0)

            # Calculations
            tinterior = column_Internal_Temperature.mean()
            oat = column_OAT.mean()

            cf = 1  # Default value
            if gp == 50:
                cf = 0.000018 * oat + 0.875
            elif gp == 40:
                cf = 0.0000639 * oat + 0.91
            elif gp == 30:
                cf = 0.00008 * oat + 0.94
            elif gp == 20:
                cf = 1e-05 * oat + 0.97
            elif gp == 0:
                cf = -0.00044 * oat + 1.05

            def water(gph, tinterior2, oat, cf):
                return 500 * gph * (tinterior2 - oat) * cf

            gph = gpm * 60
            heat_transfer = water(gph, tinterior, oat, cf)

            st.write(f"Total Heat Transfer: {round(heat_transfer, 2)} BTU")

            def converttombh(heat_transfer):
                return heat_transfer / 1000

            mbh = converttombh(heat_transfer)
            st.write(f"Total Heat Transfer: {round(mbh, 2)} MBH")

            avgmbh = mbh / 719

            st.write(f"Average Heat Transfer: {round(avgmbh, 2)} MBH")

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file.")


