# Library-Management-System


## Requirements

Before running the FastAPI app, ensure you have the following installed:

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:5h15h1r/Library-Management-System.git
    cd Library-Management-System
    ```

2. Create a virtual environment (optional but recommended):
    
    - On Windows:
    ```bash
    python -m venv venv
    ```
    
    - On macOS and Linux:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

    ```bash
    venv\Scripts\activate
    ```

    - On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the app locally, follow these steps:

1. Make sure you are in the root directory of the project.

2. Run the following command to start the Uvicorn server:

    ```bash
    uvicorn app.server.app:app --reload
    ```
    OR
    ```bash
    python3 app/main.py
    ```
    

3. Open your web browser and navigate to `http://localhost:8000` 

## Environment Variables

The following environment variables can be used to configure the FastAPI app:

- `MONGO_URI`: The Mongo connection URI used to connect to a self-hosted MongoDB standalone deployment or Mongo Atlas (format: `mongodb+srv://[username:password@]host[/[defaultauthdb][?options]]`).


You can set these variables as needed before starting the server.