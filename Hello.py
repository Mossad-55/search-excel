import streamlit as st
import pandas as pd


@st.cache_resource
def read_data(file, sheet_name):
    return pd.read_excel(file, sheet_name=sheet_name)


def main():
    hide_st_style = """
        <style>
            #MainMenu {visibility: hidden;}
            #deploy-button-wrapper {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """

    st.set_page_config(
        page_title="Searching",
        page_icon="📊",
        layout="wide",
    )

    st.header("Search your Excel file 📊")

    st.markdown(hide_st_style, unsafe_allow_html=True)

    csv_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"], accept_multiple_files=False)

    if csv_file is not None:
        # Get the list of sheet names in the Excel file
        sheet_names = pd.ExcelFile(csv_file).sheet_names

        # Let the user choose a sheet
        selected_sheet = st.selectbox("Select a sheet:", sheet_names)

        # Lazy loading: Read data only when needed
        df = read_data(csv_file, sheet_name=selected_sheet)

        # Display the column selection dropdown
        selected_column = st.selectbox("Select a column to begin the search:", df.columns)

        # Display a text input for the user to enter a character
        search_char = st.text_input(f"Enter a character to search in {selected_column}:", "")

        if search_char != '':
            # Convert column values to strings and filter based on user input
            filtered_df = df[df[selected_column].astype(str).str.contains(search_char, case=False, na=False)]

            # Remove duplicates from the filtered results
            filtered_df = filtered_df.drop_duplicates()

            # Display the filtered results with pagination
            page_size = st.slider("Results per page", min_value=1, max_value=len(filtered_df), value=10)

            # Display paginated results using st.table
            current_page = st.number_input("Page", min_value=1, max_value=len(filtered_df) // page_size + 1, value=1)
            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            st.dataframe(
                filtered_df.iloc[start_idx:end_idx].style.set_properties(**{'text-align': 'left'}).set_table_styles(
                    [dict(selector='th', props=[('text-align', 'left')])]))


if __name__ == '__main__':
    main()
