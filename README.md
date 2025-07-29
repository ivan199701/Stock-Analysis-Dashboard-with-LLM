# Stock Analysis Dashboard with LLM

This project is a web-based dashboard that provides stock analysis by combining technical indicators with AI-powered insights from Google's Gemini 2.5 Pro.

## Features
- **Interactive Candlestick Charts:** Visualize historical price data with Plotly.
- **Technical Indicators:** Overlay key indicators like SMA and Bollinger Bands on the price chart.
- **Automated Technical Analysis:** The system automatically analyzes trends, momentum, and key support/resistance levels.
- **AI-Powered Insights:** Leverages a Large Language Model (LLM) to provide a qualitative analysis, recommendation, and risk assessment in a structured format.
- **Configurable Timeframes:** Analyze stocks over short, medium, or long-term periods.

## How to Run the Application

There are two ways to run the application: locally using a Python environment, or with Docker.

### Method 1: Running Locally

#### 1. Prerequisites
- Python 3.9+
- An environment management tool like `venv` or `conda`.

#### 2. Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    - Create a file named `.env` in the root directory of the project.
    - Add your Google API key to the `.env` file like this:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

#### 3. Launch the Application
- Run the following command in your terminal from the project root directory:
  ```bash
  streamlit run src/presentation/ui/pages/main.py
  ```
- The application should now be open in your web browser at `http://localhost:8501`.

### Method 2: Running with Docker

#### 1. Prerequisites
- Docker and Docker Compose installed on your machine.

#### 2. Setup
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Set up your environment variables:**
    - Create a file named `.env` in the root directory of the project.
    - Add your Google API key to the `.env` file like this:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

#### 3. Launch the Application
- Run the following command in your terminal from the project root directory:
  ```bash
  docker-compose up --build
  ```
- The application will be built and started. You can access it in your web browser at `http://localhost:8501`.

## Deployment Guide (Windows & macOS)

The recommended method for deploying this application is by using Docker, as it creates a consistent and isolated environment. The steps are the same for both Windows and macOS.

### Prerequisites
- **Docker Desktop:** You must have Docker Desktop installed and running on your system. You can download it from the official Docker website.

### Steps
1.  **Clone the Repository:**
    Open your terminal (or PowerShell on Windows) and clone the project to your machine:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create the Environment File:**
    Create a file named `.env` in the root of the project directory. This file will hold your secret API key. Add your Gemini API key to it like so:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

3.  **Build and Run the Container:**
    Run the following command from the root of the project directory. This command will build the Docker image and start the application in the background (detached mode).
    ```bash
    docker-compose up --build -d
    ```

4.  **Access the Application:**
    Open your web browser and navigate to `http://localhost:8501`. The Stock Analysis Dashboard should now be running.

### Stopping the Application
To stop the running application, open a terminal in the project directory and run:
```bash
docker-compose down
```

## Project Structure
The project follows a 4-layer architecture based on Domain-Driven Design:
- **`src/presentation`**: Contains the Streamlit UI code.
- **`src/application`**: The application layer that orchestrates the business logic.
- **`src/domain`**: The core of the application, containing the business logic, entities, and rules.
- **`src/infrastructure`**: Handles external concerns like data fetching from APIs and configuration.
