# Data Analyzer UI Tool (React + Python)

This application provides a user-friendly interface to analyze data from CSV or Excel files. It uses a React frontend and a Python (Flask) backend. The backend leverages the Google Gemini API to classify text data and presents the results in a visual dashboard on the frontend.

## Features

- **React Frontend:** A modern, responsive UI.
- **Python Backend:** A robust Flask server to handle data processing and API interactions.
- **Screen 1 (S1):** An engaging UI with a red supercar on a racetrack. Users can drop a file into a designated area to start the analysis. A car racing animation is shown during data processing.
- **Screen 2 (S2):** A split-screen dashboard that displays a pie chart of the classified data on the left, and options to download the report, download the pie chart, and email the report on the right.

## Project Structure

-   `/frontend`: Contains the React application.
-   `/backend`: Contains the Flask server.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

### Backend Setup

2.  **Navigate to the backend directory and install dependencies:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    -   Create a file named `.env` in the `backend` directory.
    -   Add your Google Gemini API key to the `.env` file as follows:
        ```
        GOOGLE_API_KEY="your_gemini_api_key_here"
        ```

### Frontend Setup

4.  **Navigate to the frontend directory and install dependencies:**
    ```bash
    cd ../frontend
    npm install
    ```

5.  **Add image assets:**
    -   In the `frontend/public` directory, add two images:
        -   `track.png`: A background image of a racetrack (recommended size: 800x600).
        -   `car.png`: An image of a red supercar with a transparent background.

## How to Run

You will need to run both the backend and frontend servers in separate terminals.

1.  **Run the backend server:**
    -   From the root directory, run:
        ```bash
        python backend/app.py
        ```
    -   The backend will be running on `http://localhost:5001`.

2.  **Run the frontend server:**
    -   From the root directory, run:
        ```bash
        cd frontend
        npm start
        ```
    -   The frontend will open in your browser at `http://localhost:3000`.

## Input File Requirements

The input file (CSV or Excel) must contain the following two columns:
-   `Description`
-   `Comments`

If these columns are not found, the application will display a "low fuel" error message.