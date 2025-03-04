import streamlit as st
import tempfile
import os
import pandas as pd
import logging
import camelot
import re
from PyPDF2 import PdfReader, errors
import base64
import json
import io  # <--- Added this line
import tabula #<--Added this library
import fitz
from streamlit_image_coordinates import streamlit_image_coordinates

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def pdf_table_extraction_page():
    st.markdown(
        """
        <div style='background-color: #e0f2f7; padding: 20px; border-radius: 10px;'>
            <h1 style='text-align: center; color: #007BFF;'>📊 PDF Table Extraction</h1>
        </div>
        """,
        unsafe_allow_html=True,
        )
    st.markdown("### 📤 Upload PDF files to extract tables")
    st.markdown(
        """
    **Instructions:**
    1.  Upload one or more PDF files.
    2.  Select the extraction engine (Camelot or Tabula-py) and its parameters.
    3.  Select the pages to process for each file.
    4.  Click the "🚀 Extract Tables" button.
    5.  Review, edit, and download the extracted tables in your preferred format.
    """
    )
    st.markdown("---")
    def clear_all_inputs():
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
    with st.sidebar:
        st.header("⚙️ Controls")
        if st.button("🔄 Clear All Inputs", type="primary", key="clear_all_button", help="Clear all the input fields and selections"):
            clear_all_inputs()

    uploaded_files = st.file_uploader(
        "Choose PDF files", type=["pdf"], accept_multiple_files=True, help="Select one or more PDF files to upload."
    )

    if uploaded_files:
        if 'camelot' not in globals():
            st.error("Camelot library not installed. Please install it using 'pip install camelot-py[cv]'.")
            return

        if 'tabula' not in globals():
            st.error("Tabula-py library not installed. Please install it using 'pip install tabula-py'.")
            return

        # Extraction Options in the Main Content Area
        st.subheader("⚙️ Extraction Method")
        with st.container():
            extraction_engine = st.selectbox(
                "Extraction Engine",
                options=["Camelot", "Tabula-py"],
                index=0,
                help="""Select the table extraction engine. **Camelot** is more robust and **Tabula-py** might work better with certain table structures.""",
            )

            if extraction_engine == "Camelot":
                extraction_method = st.selectbox(
                    "Camelot Flavor",
                    options=["", "lattice", "stream"],
                    index=0,
                    help="""
                        **lattice**: Best for tables with clear lines.
                        **stream**: Best for tables with no clear lines or gaps.
                    """,
                )
            
            elif extraction_engine == "Tabula-py":
                extraction_method = st.selectbox(
                    "Tabula-py Mode",
                    options=["", "lattice", "stream"],
                    index=0,
                    help="""
                        **lattice**: Best for tables with clear lines.
                        **stream**: Best for tables with no clear lines or gaps.
                    """,
                )

        st.markdown("---")
        # Page Selection for each uploaded file.
        page_selections = {}
        for uploaded_file in uploaded_files:
            logging.info(f"Processing file: {uploaded_file.name}")
            num_pages = 0
            # Determine the number of pages
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_file_path = temp_file.name
                with open(temp_file_path, 'rb') as f:
                    try:
                        pdf_reader = PdfReader(f)
                        num_pages = len(pdf_reader.pages)
                    except errors.PdfReadError as e:
                        st.error(f"Error reading PDF file {uploaded_file.name}: {e}. Is it encrypted or corrupted?")
                        logging.error(f"Error reading PDF file {uploaded_file.name}: {e}")
                        continue
            except Exception as e:
                st.error(f"Error determining the number of pages in file {uploaded_file.name}: {e}")
                logging.error(f"Error determining the number of pages in file {uploaded_file.name}: {e}")
                continue
            finally:
                f.close()
            os.remove(temp_file_path)

            # Page selection options
            st.subheader(f"📄 Page Selection")
            pages_options = ["all"] + list(range(1, num_pages + 1))
            selected_pages = st.multiselect(
                "Select pages to process:",
                pages_options,
                default="all",
                key=f"{uploaded_file.name}_pages_multiselect",
                help="Select 'all' to process all pages or select specific pages to extract tables from."
            )

            if "all" in selected_pages:
                pages_str = "all"
            else:
                pages_str = ",".join(map(str, selected_pages))

            page_selections[uploaded_file.name] = pages_str


        st.markdown("---")
        # Extract Button
        if st.button("🚀 Extract Tables", help="Click to start the extraction process with the current settings."):
            with st.spinner("🔄 Extracting tables..."):
                all_tables = []
                for uploaded_file in uploaded_files:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                            temp_file.write(uploaded_file.getbuffer())
                            temp_file_path = temp_file.name
                        try:
                            if extraction_engine == "Camelot":
                                tables = camelot.read_pdf(
                                    temp_file_path,
                                    pages=page_selections.get(uploaded_file.name, "all"),
                                    flavor=extraction_method,
                                    strip_text='\n',
                                    line_scale=40
                                )
                            elif extraction_engine == "Tabula-py":
                                tables = tabula.read_pdf(
                                     temp_file_path,
                                     pages=page_selections.get(uploaded_file.name, "all"),
                                     lattice=True if extraction_method == "lattice" else False,
                                     stream=True if extraction_method == "stream" else False,
                                     multiple_tables=True
                                 )

                                
                            else:
                                raise ValueError("Invalid extraction engine selected.")

                        except ValueError as e:
                            st.error(f"Error extracting tables from file {uploaded_file.name}: {e}")
                            logging.error(f"Error extracting tables from file {uploaded_file.name}: {e}")
                            continue
                        except Exception as e:
                            st.error(f"Error extracting tables from file {uploaded_file.name}: {e}")
                            logging.error(f"Error extracting tables from file {uploaded_file.name}: {e}")
                            continue
                        all_tables.append((uploaded_file.name, tables))

                    except Exception as e:
                        st.error(f"Error processing file {uploaded_file.name}: {e}")
                        logging.error(f"Error processing file {uploaded_file.name}: {e}")
                    finally:
                        os.remove(temp_file_path)

                if not all_tables:
                    st.warning("⚠️ No tables found in any of the uploaded PDFs.")
                    return
                else:
                    st.success("✅ PDF(s) processed successfully!")

                for file_name, tables in all_tables:
                    if extraction_engine=="Tabula-py":
                        try:
                            for j, table in enumerate(tables):
                                df = pd.DataFrame(table)
                                if df is None or df.empty:
                                    st.warning(f"⚠️ Empty Table found {j+1} in {file_name}")
                                    logging.warning(f"Empty table found {j+1} in {file_name}")
                                    continue

                                st.markdown(f"**Table {j+1}**")
                                edited_df = st.data_editor(df, key=f"{file_name}_table_{j+1}", hide_index=True)

                                # Export to different formats
                                export_formats = ["CSV", "Excel", "JSON"]
                                selected_format = st.selectbox("Select export format:", export_formats, key=f"{file_name}_table_{j+1}_format", index=0)
                                
                                csv = edited_df.to_csv(index=False).encode("utf-8")
                                excel_buffer = io.BytesIO()
                                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                    edited_df.to_excel(writer, index=False, sheet_name='Sheet1')
                                excel_data = excel_buffer.getvalue()
                                json_data = json.dumps(edited_df.to_dict(orient='records'), indent=4)

                                if selected_format == "CSV":
                                    st.download_button(
                                        label=f"💾 Download Table {j+1} from {file_name} as {selected_format}",
                                        data=csv,
                                        file_name=f"{file_name}_table_{j+1}.csv",
                                        mime="text/csv",
                                        key=f"{file_name}_table_{j+1}_csv"
                                    )
                                elif selected_format == "Excel":
                                    st.download_button(
                                        label=f"💾 Download Table {j+1} from {file_name} as {selected_format}",
                                        data=excel_data,
                                        file_name=f"{file_name}_table_{j+1}.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        key=f"{file_name}_table_{j+1}_xlsx"
                                    )
                                elif selected_format == "JSON":
                                    st.download_button(
                                        label=f"💾 Download Table {j+1} from {file_name} as {selected_format}",
                                        data=json_data,
                                        file_name=f"{file_name}_table_{j+1}.json",
                                        mime="application/json",
                                        key=f"{file_name}_table_{j+1}_json"
                                    )
                        except Exception as e:
                             st.error(f"Error processing extracted tables {file_name}: {e}")
                             logging.error(f"Error processing extracted tables {file_name}: {e}")
                    
                    elif tables.n > 0:
                        st.markdown(f"**📄 Tables found in: {file_name}**")
                        for i, table in enumerate(tables, start=1):
                            df = table.df
                            if df is None or df.empty:
                                st.warning(f"⚠️ Empty Table found {i} in {file_name}")
                                logging.warning(f"Empty table found {i} in {file_name}")
                                continue

                            st.markdown(f"**Table {i}**")
                            # Table Editing (using st.data_editor)
                            edited_df = st.data_editor(df, key=f"{file_name}_table_{i}", hide_index=True)

                            # Export to different formats
                            export_formats = ["CSV", "Excel", "JSON"]
                            selected_format = st.selectbox("Select export format:", export_formats, key=f"{file_name}_table_{i}_format", index=0)
                            
                            csv = edited_df.to_csv(index=False).encode("utf-8")
                            excel_buffer = io.BytesIO()
                            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                                edited_df.to_excel(writer, index=False, sheet_name='Sheet1')
                            excel_data = excel_buffer.getvalue()
                            json_data = json.dumps(edited_df.to_dict(orient='records'), indent=4)

                            if selected_format == "CSV":
                                st.download_button(
                                    label=f"💾 Download Table {i} from {file_name} as {selected_format}",
                                    data=csv,
                                    file_name=f"{file_name}_table_{i}.csv",
                                    mime="text/csv",
                                    key=f"{file_name}_table_{i}_csv"
                                )
                            elif selected_format == "Excel":
                                st.download_button(
                                    label=f"💾 Download Table {i} from {file_name} as {selected_format}",
                                    data=excel_data,
                                    file_name=f"{file_name}_table_{i}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key=f"{file_name}_table_{i}_xlsx"
                                )
                            elif selected_format == "JSON":
                                st.download_button(
                                    label=f"💾 Download Table {i} from {file_name} as {selected_format}",
                                    data=json_data,
                                    file_name=f"{file_name}_table_{i}.json",
                                    mime="application/json",
                                    key=f"{file_name}_table_{i}_json"
                                )

                    else:
                        st.warning(f"⚠️ No tables found in: {file_name}")
