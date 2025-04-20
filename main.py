import sys
import os
import streamlit as st
import pandas as pd

# ✅ Add 'utils' to path to support absolute imports on Streamlit Cloud
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.data_loader import load_all_data
from utils.model import load_model, predict_home_runs  # Adjust if model.py is elsewhere
from utils.display import style_projection_table  # Optional: for nice styling

st.set_page_config(page_title="MLB Home Run Projections", layout="wide")

def main():
    st.title("💥 MLB Home Run AI Projections")
    st.markdown("Real data. AI-powered predictions. Adjusted for matchups, weather, and park factors.")

    with st.spinner("Loading data..."):
        data = load_all_data()

    if data is None or data.empty:
        st.error("No data loaded. Please check your data sources.")
        return

    # Show raw data toggle
    if st.checkbox("Show raw input data"):
        st.dataframe(data)

    # Load trained model (or placeholder logic)
    model = load_model()

    with st.spinner("Predicting home runs..."):
        predictions = predict_home_runs(data, model)

    # Combine predictions into final table
    result_df = data.copy()
    result_df["HR_Probability"] = predictions
    result_df = result_df.sort_values(by="HR_Probability", ascending=False)

    # Optional: Style the table nicely
    styled_df = style_projection_table(result_df) if "style_projection_table" in globals() else result_df

    st.subheader("🔝 Top Home Run Picks Today")
    st.dataframe(styled_df, use_container_width=True)

    # Download option
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Projections", csv, "hr_projections.csv", "text/csv")

if __name__ == "__main__":
    main()
