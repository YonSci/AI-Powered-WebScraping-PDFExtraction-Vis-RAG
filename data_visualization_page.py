import streamlit as st
import pandas as pd
import altair as alt
from typing import Optional

def data_visualization_page():

    st.markdown(
    """
    <div style='background-color: #e0f2f7; padding: 20px; border-radius: 10px;'>
        <h1 style='text-align: center; color: #007BFF;'>📊 Data Visualization Tool</h1>
    </div>
    """,
    unsafe_allow_html=True,
    )
    
    st.markdown("""
    **How it works:**

    1. 📂 Upload a CSV or Excel file.
    2. 🔄 Adjust column data types if needed.
    3. 📊 Visualize your data using various plot types.
    4. 📥 Download the transformed data.
    """)

    st.markdown("### 📂 Upload a CSV or Excel file to visualize your data")
    
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xls", "xlsx"])
    if uploaded_file is not None:
        with st.spinner("Loading file..."):
            # Read file based on extension.
            try:
                if uploaded_file.name.lower().endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"Error reading file: {e}")
                return
        
        # Display data summary.
        st.markdown("### 📊 Data Summary (Before Transformation)")
        st.markdown(f"**Shape:** {df.shape}")
        st.markdown("**Columns:** " + ", ".join(df.columns.astype(str)))
        st.markdown("**Data Types:**")
        st.write(df.dtypes)
        st.markdown("**Summary Statistics:**")
        st.dataframe(df.describe())
        
        # Option to display full data.
        if st.checkbox("Display full data"):
            st.markdown("### 📋 Full Data")
            st.dataframe(df)
        
        st.markdown("---")
        st.markdown("### 🔄 Adjust Column Data Types")
        st.markdown("For each column, select a new data type. Choose **No Change** to keep the original type.")
        with st.form("dtype_form"):
            new_types = {}
            for col in df.columns:
                current_dtype = str(df[col].dtype)
                new_dtype = st.selectbox(
                    f"Column: {col} (Current: {current_dtype})",
                    ["No Change", "int", "float", "str", "datetime64[ns]"],
                    key=f"dtype_{col}"
                )
                new_types[col] = new_dtype
            dtype_submitted = st.form_submit_button("Apply Data Type Changes")
        
        if dtype_submitted:
            with st.spinner("Applying data type changes..."):
                df_transformed = df.copy()
                for col, dtype in new_types.items():
                    if dtype != "No Change":
                        try:
                            if dtype == "int":
                                df_transformed[col] = pd.to_numeric(df_transformed[col], errors="coerce").astype("Int64")
                            elif dtype == "float":
                                # Clean the column by removing non-numeric characters (commas, currency symbols, etc.)
                                if df_transformed[col].dtype == "object":
                                    df_transformed[col] = df_transformed[col].str.replace(r'[^\d\.-]', '', regex=True)
                                df_transformed[col] = pd.to_numeric(df_transformed[col], errors="coerce")
                                if df_transformed[col].isnull().all():
                                    st.warning(f"Warning: Converting column '{col}' to float resulted in all NaN values. Please check the data.")
                            elif dtype == "str":
                                df_transformed[col] = df_transformed[col].astype(str)
                            elif dtype == "datetime64[ns]":
                                df_transformed[col] = pd.to_datetime(df_transformed[col], errors="coerce")
                        except Exception as e:
                            st.error(f"Error converting column {col}: {e}")
                st.markdown("### 🔍 Transformed Data Preview")
                st.dataframe(df_transformed.head())
                csv_data = df_transformed.to_csv(index=False).encode("utf-8")
                st.download_button(label="Download Transformed Data as CSV", data=csv_data, file_name="transformed_data.csv", mime="text/csv")
                # Use the transformed DataFrame for subsequent visualization.
                df = df_transformed
        
        st.markdown("---")
        st.markdown("### 📊 Data Summary (After Transformation)")
        st.markdown(f"**Shape:** {df.shape}")
        st.dataframe(df.describe())
        
        # Allow user to select a row range for plotting.
        row_min = 0
        row_max = df.shape[0] - 1
        selected_rows = st.slider("Select row range for plotting", min_value=row_min, max_value=row_max, value=(row_min, row_max))
        filtered_data = df.iloc[selected_rows[0]: selected_rows[1] + 1]
        st.markdown(f"Using rows {selected_rows[0]} to {selected_rows[1]} for visualization.")
        
        st.markdown("---")
        st.markdown("### 📈 Visualization Options")
        plot_type = st.selectbox("Select Plot Type", ["Histogram", "Scatter Plot", "Line Chart", "Bar Chart"])
        
        # Helper function to determine if a column is datetime
        def is_datetime(col: str) -> bool:
            return pd.api.types.is_datetime64_any_dtype(filtered_data[col])
        
        if plot_type == "Histogram":
            numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                col = st.selectbox("Select a numeric column for Histogram", numeric_cols, key="hist_col")
                set_limits = st.checkbox("Set x-axis limits for Histogram", key="hist_limits")
                if set_limits:
                    # Check if column is datetime (unlikely for histogram) otherwise use number input.
                    if is_datetime(col):
                        x_min = st.date_input("X-axis minimum", value=filtered_data[col].min(), key="hist_xmin")
                        x_max = st.date_input("X-axis maximum", value=filtered_data[col].max(), key="hist_xmax")
                    else:
                        x_min = st.number_input("X-axis minimum", value=float(filtered_data[col].min()), key="hist_xmin")
                        x_max = st.number_input("X-axis maximum", value=float(filtered_data[col].max()), key="hist_xmax")
                    scale = alt.Scale(domain=[x_min, x_max])
                else:
                    scale = alt.Scale()
                chart = alt.Chart(filtered_data).mark_bar().encode(
                    x=alt.X(col, bin=True, scale=scale, title=col),
                    y=alt.Y("count()", title="Count")
                ).properties(width=600, height=400)
                st.altair_chart(chart)
            else:
                st.warning("No numeric columns available for histogram.")
        
        elif plot_type == "Scatter Plot":
            numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()
            if len(numeric_cols) >= 2:
                x_col = st.selectbox("Select X-axis for Scatter Plot", numeric_cols, key="scatter_x")
                y_col = st.selectbox("Select Y-axis for Scatter Plot", numeric_cols, key="scatter_y")
                set_limits = st.checkbox("Set axis limits for Scatter Plot", key="scatter_limits")
                if set_limits:
                    # For each axis, check if the column is datetime.
                    if is_datetime(x_col):
                        x_min = st.date_input("X-axis minimum", value=filtered_data[x_col].min(), key="scatter_xmin")
                        x_max = st.date_input("X-axis maximum", value=filtered_data[x_col].max(), key="scatter_xmax")
                    else:
                        x_min = st.number_input("X-axis minimum", value=float(filtered_data[x_col].min()), key="scatter_xmin")
                        x_max = st.number_input("X-axis maximum", value=float(filtered_data[x_col].max()), key="scatter_xmax")
                    if is_datetime(y_col):
                        y_min = st.date_input("Y-axis minimum", value=filtered_data[y_col].min(), key="scatter_ymin")
                        y_max = st.date_input("Y-axis maximum", value=filtered_data[y_col].max(), key="scatter_ymax")
                    else:
                        y_min = st.number_input("Y-axis minimum", value=float(filtered_data[y_col].min()), key="scatter_ymin")
                        y_max = st.number_input("Y-axis maximum", value=float(filtered_data[y_col].max()), key="scatter_ymax")
                    x_scale = alt.Scale(domain=[x_min, x_max])
                    y_scale = alt.Scale(domain=[y_min, y_max])
                else:
                    x_scale = alt.Scale()
                    y_scale = alt.Scale()
                chart = alt.Chart(filtered_data).mark_circle(size=60).encode(
                    x=alt.X(x_col, scale=x_scale),
                    y=alt.Y(y_col, scale=y_scale),
                    tooltip=numeric_cols
                ).interactive().properties(width=600, height=400)
                st.altair_chart(chart)
            else:
                st.warning("Need at least two numeric columns for scatter plot.")
        
        elif plot_type == "Line Chart":
            all_cols = filtered_data.columns.tolist()
            numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()
            if all_cols:
                x_col = st.selectbox("Select X-axis (e.g., time or index) for Line Chart", all_cols, key="line_x")
                y_col = st.selectbox("Select Y-axis (numeric) for Line Chart", numeric_cols, key="line_y")
                set_limits = st.checkbox("Set axis limits for Line Chart", key="line_limits")
                if set_limits:
                    if is_datetime(x_col):
                        x_min = st.date_input("X-axis minimum", value=filtered_data[x_col].min(), key="line_xmin")
                        x_max = st.date_input("X-axis maximum", value=filtered_data[x_col].max(), key="line_xmax")
                    else:
                        x_min = st.number_input("X-axis minimum", value=float(filtered_data[x_col].min()), key="line_xmin")
                        x_max = st.number_input("X-axis maximum", value=float(filtered_data[x_col].max()), key="line_xmax")
                    y_min = st.number_input("Y-axis minimum", value=float(filtered_data[y_col].min()), key="line_ymin")
                    y_max = st.number_input("Y-axis maximum", value=float(filtered_data[y_col].max()), key="line_ymax")
                    x_scale = alt.Scale(domain=[x_min, x_max])
                    y_scale = alt.Scale(domain=[y_min, y_max])
                else:
                    x_scale = alt.Scale()
                    y_scale = alt.Scale()
                chart = alt.Chart(filtered_data).mark_line().encode(
                    x=alt.X(x_col, scale=x_scale),
                    y=alt.Y(y_col, scale=y_scale),
                    tooltip=all_cols
                ).interactive().properties(width=600, height=400)
                st.altair_chart(chart)
            else:
                st.warning("No numeric columns available for line chart.")
        
        elif plot_type == "Bar Chart":
            categorical_cols = filtered_data.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()
            if categorical_cols and numeric_cols:
                cat_col = st.selectbox("Select categorical column for Bar Chart", categorical_cols, key="bar_cat")
                num_col = st.selectbox("Select numeric column for Bar Chart", numeric_cols, key="bar_num")
                set_y_limits = st.checkbox("Set y-axis limits for Bar Chart", key="bar_limits")
                if set_y_limits:
                    y_min = st.number_input("Y-axis minimum", value=float(filtered_data[num_col].min()), key="bar_ymin")
                    y_max = st.number_input("Y-axis maximum", value=float(filtered_data[num_col].max()), key="bar_ymax")
                    y_scale = alt.Scale(domain=[y_min, y_max])
                else:
                    y_scale = alt.Scale()
                chart = alt.Chart(filtered_data).mark_bar().encode(
                    x=cat_col,
                    y=alt.Y(num_col, aggregate="sum", scale=y_scale, title=f"Sum of {num_col}"),
                    tooltip=[cat_col, num_col]
                ).interactive().properties(width=600, height=400)
                st.altair_chart(chart)
            else:
                st.warning("Need both a categorical and a numeric column for bar chart.")
    else:
        st.info("Please upload a file to begin visualization.")

data_visualization_page()