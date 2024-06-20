import pandas as pd
import streamlit as st
import ENGLISH_CERF_WORDS as EG  # Import your module

# Function to identify CREF levels
def identify_cref_level(input_excel_path, cref_csv_path):
    # Load the CREF levels dataset from CSV
    cref_df = pd.read_csv(cref_csv_path)
    
    # Create a dictionary for fast lookup, converting keys to lowercase
    cref_dict = pd.Series(cref_df['CEFR'].values, index=cref_df['headword'].str.lower()).to_dict()
    
    # Load the input Excel sheet with words
    input_df = pd.read_excel(input_excel_path)
    
    # Assuming words are in the first column
    words = input_df.iloc[:, 0]
    
    # Identify CREF levels for the words, converting words to lowercase for lookup
    cref_levels = words.apply(lambda x: cref_dict.get(str(x).lower(), "Unknown"))
    
    # Create output DataFrame
    output_df = pd.DataFrame({
        'Word': words,
        'CREF Level': cref_levels
    })
    
    # Write to an in-memory Excel file
    output_excel_path = "output_words_with_cref.xlsx"
    with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
        output_df.to_excel(writer, index=False)
    
    return output_excel_path

# Streamlit app main function
def main():
    st.title("CREF Level Identifier")
    st.write("Upload an Excel file to identify CREF levels.")
    
    # File uploader for input Excel file
    uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        input_excel_path = pd.ExcelFile(uploaded_file)
        st.write("File uploaded successfully!")
        
        # Use the cref_csv_path from your module
        cref_csv_path = EG.cref_csv_path
        
        output_excel = identify_cref_level(input_excel_path, cref_csv_path)
        
        # Download button for output Excel file
        st.download_button(
            label="Download Output File",
            data=open(output_excel, 'rb').read(),
            file_name="output_words_with_cref.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Run the Streamlit app
if __name__ == "__main__":
    main()
