# Data Analyzer UI Tool

This application provides a user-friendly interface to analyze data from CSV or Excel files. It uses the Google Gemini API to classify text data and presents the results in a visual dashboard.

## Features

- **Screen 1 (S1):** An engaging UI with a red supercar on a racetrack. Users can drop a file into a designated area to start the analysis. A car racing animation is shown during data processing.
- **Screen 2 (S2):** A split-screen dashboard that displays a pie chart of the classified data on the left, and options to download the report, download the pie chart, and email the report on the right.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    -   Create a file named `.env` in the root of the project.
    -   Add your Google Gemini API key to the `.env` file as follows:
        ```
        GOOGLE_API_KEY="your_gemini_api_key_here"
        ```

5.  **Add image assets:**
    -   Create an `assets` folder in the root of the project.
    -   Add two images to this folder:
        -   `track.png`: A background image of a racetrack (recommended size: 800x600).
        -   `car.png`: An image of a red supercar with a transparent background.

## How to Run

Once you have completed the setup, you can run the application with the following command:

```bash
python app.py
```

The application window will open, and you can start analyzing your data by dropping a file or using the upload button.

## Input File Requirements

The input file (CSV or Excel) must contain the following two columns:
-   `Description`
-   `Comments`

If these columns are not found, the application will display a "low fuel" error message.