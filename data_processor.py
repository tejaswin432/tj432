import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
# Make sure to set your GOOGLE_API_KEY in a .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def load_data(file_path):
    """Loads data from a CSV or Excel file."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type")

def validate_columns(df):
    """Validates that the required columns exist in the DataFrame."""
    return "Description" in df.columns and "Comments" in df.columns

def process_data(df):
    """Processes the data by classifying each row using the Gemini API."""
    try:
        with open("system_prompt.txt", "r") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        # Fallback if the system prompt file is missing
        system_prompt = "You are an expert in text classification..."

    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    df['Primary'] = ''
    df['Secondary'] = ''

    for index, row in df.iterrows():
        description = row['Description']
        comments = row['Comments']

        # Concatenate the text from the two columns
        combined_text = f"Description: {description}\nComments: {comments}"

        # Prepare the prompt for the API
        prompt = f"{system_prompt}\n\n{combined_text}"

        try:
            # Generate content using the model
            response = model.generate_content(prompt)

            # Parse the response to extract classifications
            response_text = response.text.strip()
            primary = "N/A"
            secondary = "N/A"

            for line in response_text.split('\n'):
                if line.startswith("Primary:"):
                    primary = line.split(":", 1)[1].strip()
                elif line.startswith("Secondary:"):
                    secondary = line.split(":", 1)[1].strip()

            df.at[index, 'Primary'] = primary
            df.at[index, 'Secondary'] = secondary

        except Exception as e:
            # Handle potential API errors for a single row
            print(f"Error processing row {index}: {e}")
            df.at[index, 'Primary'] = 'Error'
            df.at[index, 'Secondary'] = 'Error'

    return df

def generate_pie_chart(df, output_path):
    """Generates a pie chart of the primary classifications."""
    import matplotlib.pyplot as plt
    primary_counts = df['Primary'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(primary_counts, labels=primary_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Primary Classification Distribution')
    plt.ylabel('') # Hides the 'None' label on the y-axis
    plt.savefig(output_path)
    plt.close()