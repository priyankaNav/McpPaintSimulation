# MCP Paint

A powerful paint application simulation with integrated Gmail functionality, built using the Model Context Protocol (MCP) framework. This project uses the Paintbrush application on macOS to simulate a paint environment.

## Features

### Paint Tools
- **Rectangle Tool**: Draw rectangles on the Paintbrush canvas
- **Text Tool**: Add text to your Paintbrush drawings
- **Window Management**: Automatically positions and maximizes Paintbrush windows on extended displays using applescript and PyAutoGUI

### Gmail Integration
- Send emails directly from the application
- OAuth2 authentication with Google
- Asynchronous email sending

### Calculator Functions
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced math functions (power, square root, cube root, factorial)
- Trigonometric functions (sin, cos, tan)
- Logarithmic functions

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Paintbrush application on your macOS system
4. Set up Gmail API credentials:
   - Create a project in Google Cloud Console
   - Enable the Gmail API
   - Create OAuth 2.0 credentials
   - Download the credentials and save as `credentials.json` in the project root

## Usage

### Running the Application

For development mode:
```
python talk2mcp-2.py dev
```

The application will automatically launch Paintbrush, position its windows, and prepare the environment for you to use the paint tools.

### Sending Emails

The application provides a Gmail integration tool that allows you to send emails:

```python
@mcp.tool()
async def gmail_send(to: str, subject: str, message: str):
    """Send an email using the Gmail client"""
    if not to or not subject or not message:
        return {"status": "error", "error": "Missing required parameters"}
    return await gmail_client.send_email(to, subject, message)
```

## Architecture

The application is built using:
- **FastMCP**: A framework for building mission control applications
- **Gmail API**: For email functionality
- **AppleScript**: For window management on macOS
- **PyAutoGUI**: For UI automation
- **Paintbrush**: Used as the simulation environment for paint operations

## Note

This project simulates a paint application by controlling the Paintbrush application on macOS. It does not create its own paint interface but rather automates and extends the functionality of the existing Paintbrush application.

