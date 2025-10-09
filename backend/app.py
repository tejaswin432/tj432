from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
import io

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def load_data(file):
    """Loads data from an uploaded file."""
    if file.filename.endswith('.csv'):
        return pd.read_csv(file)
    elif file.filename.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type")

def validate_columns(df):
    """Validates that the required columns exist in the DataFrame."""
    return "Description" in df.columns and "Comments" in df.columns

def process_data(df):
    """Processes the data by classifying each row using the Gemini API."""
    try:
        with open("backend/system_prompt.txt", "r") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        system_prompt = "You are an expert in text classification..."

    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    df['Primary'] = ''
    df['Secondary'] = ''

    for index, row in df.iterrows():
        description = row['Description']
        comments = row['Comments']
        combined_text = f"Description: {description}\nComments: {comments}"
        prompt = f"{system_prompt}\n\n{combined_text}"

        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            primary, secondary = "N/A", "N/A"
            for line in response_text.split('\n'):
                if line.startswith("Primary:"):
                    primary = line.split(":", 1)[1].strip()
                elif line.startswith("Secondary:"):
                    secondary = line.split(":", 1)[1].strip()
            df.at[index, 'Primary'] = primary
            df.at[index, 'Secondary'] = secondary
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            df.at[index, 'Primary'] = 'Error'
            df.at[index, 'Secondary'] = 'Error'

    return df

def generate_pie_chart_base64(df):
    """Generates a pie chart and returns it as a base64 encoded string."""
    import matplotlib.pyplot as plt
    primary_counts = df['Primary'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(primary_counts, labels=primary_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Primary Classification Distribution')
    plt.ylabel('')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        df = load_data(file)
        if not validate_columns(df):
            return jsonify({"error": "Low Fuel: 'Description' and 'Comments' columns are required."}), 400

        processed_df = process_data(df.copy())
        pie_chart_base64 = generate_pie_chart_base64(processed_df)

        # Convert DataFrame to JSON serializable format
        report_data = processed_df.to_dict(orient='records')

        return jsonify({
            "report": report_data,
            "pieChart": f"data:image/png;base64,{pie_chart_base64}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)