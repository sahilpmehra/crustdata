# CrustData Challenge

A modern chat application for customer support on the Crustdata API built with FastAPI backend and React TypeScript frontend. The application provides a real-time chat interface powered by OpenAI's API.

## Project Structure

```
crustdata/
├── backend/           # FastAPI server
│   ├── main.py       # Main server file
│   ├── services/     # Business logic
│   └── config.py     # Configuration
└── client/           # React TypeScript frontend
    ├── src/          # Source code
    └── public/       # Static files
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- OpenAI API key

## Setup & Installation

### Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Frontend Setup

1. Navigate to the client directory:

   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

1. Initialize the vector store (from the backend directory):

   ```bash
   python startup.py
   ```

2. Start the backend server (from the backend directory):

   ```bash
   uvicorn main:app --reload
   ```

   The server will run on `http://localhost:8000`

3. Start the frontend development server (from the client directory):
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## Development

- Backend API documentation is available at `http://localhost:8000/docs`
- The frontend is built with React 18, TypeScript, and Tailwind CSS
- The backend uses FastAPI with Python 3.8+

## License

MIT
