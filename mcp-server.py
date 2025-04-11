# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import asyncio
import asyncio
import subprocess
import pyautogui
import re
import shlex
import gmailClient
# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]



# Function to open Paintbrush and move it to secondary monitor and maximize
@mcp.tool()
async def open_paint() -> dict:
    """
    Open Paintbrush on macOS, move all its windows (toolbox and main canvas) to
    the extended display (laptop: 1470x956) and trigger full-screen mode.
    Assumes the extended display is positioned to the left of your main monitor.
    """
    try:
        # Launch Paintbrush with the macOS 'open' command.
        subprocess.Popen(["open", "-a", "Paintbrush"])
        await asyncio.sleep(2.0)  # Allow extra time for Paintbrush to fully launch

        # AppleScript that iterates over all windows of Paintbrush,
        # sets each window’s position and size, and then simulates the full screen shortcut.
        applescript = '''
        tell application "System Events"
            tell process "Paintbrush"
                set frontmost to true
                delay 0.5
                set winList to windows
                repeat with w in winList
                    try
                        set position of w to {-1470, 0}
                        set size of w to {1470, 956}
                    end try
                end repeat
                delay 0.5
                -- Attempt to trigger full screen mode using the keyboard shortcut.
                keystroke "f" using {control down, command down}
            end tell
        end tell
        '''
        subprocess.Popen(["osascript", "-e", applescript])
        await asyncio.sleep(1.0)  # Allow time for full screen action

        return {
            "content": [
                {"type": "text", "text": "Paintbrush windows repositioned and maximized on extended display."}
            ]
        }
    except Exception as e:
        return {
            "content": [
                {"type": "text", "text": f"Error opening Paintbrush: {str(e)}"}
            ]
        }

async def reposition_window(window_index: int, left: int, top: int, width: int, height: int, app_name="Paintbrush"):
    """
    Repositions the specified window of the given application using AppleScript.
    """
    applescript = f'''
    tell application "System Events"
        tell process "{app_name}"
            if (count of windows) ≥ {window_index} then
                set position of window {window_index} to {{{left}, {top}}}
                set size of window {window_index} to {{{width}, {height}}}
            end if
        end tell
    end tell
    '''
    try:
        subprocess.check_call(["osascript", "-e", applescript])
        print(f"Window {window_index} repositioned to ({left}, {top}) with size ({width}x{height}).")
    except subprocess.CalledProcessError as e:
        print(f"Error repositioning window {window_index}:", e)

async def get_window_bounds(window_index: int, app_name="Paintbrush") -> list:
    """
    Retrieves the AXFrame of the specified window of the application.
    The AXFrame typically returns a record in the form: {{x, y}, {width, height}}.
    This function returns the bounds as a list: [left, top, right, bottom].
    """
    applescript = f'''
    tell application "System Events"
        tell process "{app_name}"
            if (count of windows) < {window_index} then error "Window {window_index} not available"
            set theFrame to value of attribute "AXFrame" of window {window_index}
            return theFrame
        end tell
    end tell
    '''
    try:
        output = subprocess.check_output(["osascript", "-e", applescript])
        frame_str = output.decode().strip()  # e.g. "{{x, y}, {width, height}}"
        numbers = list(map(int, re.findall(r'-?\d+', frame_str)))
        if len(numbers) != 4:
            print("Unexpected frame format:", frame_str)
            return []
        x, y, w, h = numbers
        left = x
        top = y
        right = x + w
        bottom = y + h
        print(f"Window {window_index} AXFrame: x={x}, y={y}, width={w}, height={h}")
        return [left, top, w, h]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving bounds for window {window_index}:", e)
        return []
    
async def select_rectangle_tool() -> dict:
    """
    Simulate clicking on the rectangle tool button in the Paintbrush toolbox.
    
    Adjust the coordinates below (currently set to (-1440, 100)) 
    so that they point to the location of the rectangle tool in your Paintbrush UI.
    """
    try:
        # Example coordinate for the rectangle tool on the toolbox.
        # (This coordinate is in global space; adjust as needed.)
        tool_x, tool_y = -1450, 689
        pyautogui.moveTo(tool_x, tool_y, duration=0.5)
        await asyncio.sleep(0.2)
        pyautogui.click()  # Click to select the rectangle tool
        await asyncio.sleep(0.5)
        # while True:
        #     # Get the current mouse position
        #     x, y = pyautogui.position()

        #     # Check for mouse click (this checks for left-click)
        #     if pyautogui.mouseInfo() == "left":
        #         print(f"Mouse clicked at coordinates: ({x}, {y})")
        #         break

        # await asyncio.sleep(0.1)  # Add a small delay to avoid excessive CPU usage

        return {"content": [{"type": "text", "text": "Rectangle tool selected."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error selecting rectangle tool: {str(e)}"}]}


# Function to draw rectangle in Paintbrush
@mcp.tool()
async def draw_rectangle() -> dict:

    """
    Draw a 400x200 rectangle at the center of the Paintbrush window using the rectangle tool.
    
    Assumptions:
      - The Paintbrush window (on the extended display) is positioned with its top-left at (-1470, 0)
        and has size 1470x956.
      - The canvas uses global screen coordinates (i.e. full window area).
      
    The center of this window is at (-735, 478). A rectangle of 400x200 pixels centered there will
    span from (-935, 378) to (-535, 578).
    """
    try:
        await reposition_window(window_index=1, left=-1470, top=0, width=1470, height=956, app_name="Paintbrush")
        await reposition_window(window_index=2, left=-1470, top=0, width=1470, height=956, app_name="Paintbrush")
        await asyncio.sleep(2)

        # Select the rectangle tool from the Toolbox.
        result_tool = await select_rectangle_tool()
        print(result_tool)
        await asyncio.sleep(2)

        bounds = await get_window_bounds( window_index=2)
        if not bounds or len(bounds) != 4:
            print("Canvas window bounds could not be retrieved.")
            return

        window_x, window_y, width, height = bounds
        print(f"Window bounds: {bounds}")

        # Calculate the center of the window.
       
        center_x = -700
        center_y = 900

        # Define rectangle dimensions.
        rect_width, rect_height = 800, 400
        half_rect_width = rect_width // 2  # 200
        half_rect_height = rect_height // 2  # 100

        # Calculate rectangle boundaries relative to the global coordinates.
        start_x = center_x - half_rect_width  # -735 - 200 = -935
        start_y = center_y - half_rect_height # 478 - 100 = 378
        end_x = center_x + half_rect_width     # -735 + 200 = -535
        end_y = center_y + half_rect_height    # 478 + 100 = 578

        # Debug print.
        print(f"Drawing rectangle from global ({start_x}, {start_y}) to ({end_x}, {end_y})")

        # Ensure pyautogui's fail-safe is disabled.
        pyautogui.FAILSAFE = False

        # Simulate the click-drag to draw the rectangle.
        pyautogui.moveTo(start_x, start_y, duration=0.5)
        await asyncio.sleep(0.2)
        pyautogui.mouseDown()  # Start drawing
        await asyncio.sleep(0.2)
        pyautogui.moveTo(end_x, end_y, duration=0.5)
        await asyncio.sleep(0.2)
        pyautogui.mouseUp()  # Finish drawing
        await asyncio.sleep(0.2)
       
        # while True:
        #     # Get the current mouse position
        #     x, y = pyautogui.position()

        #     # Check for mouse click (this checks for left-click)
        #     if pyautogui.mouseInfo() == "left":
        #         print(f"Mouse clicked at coordinates: ({x}, {y})")
        #         break

        # await asyncio.sleep(0.1)  # Add a small delay to avoid excessive CPU usage

        return {"content": [{"type": "text", "text": "Rectangle drawn at the center of the Paintbrush window."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error drawing rectangle with tool: {str(e)}"}]}



# Function to add text to the center of the rectangle
async def select_text_tool() -> dict:
    """
    Selects the Text tool from the toolbox.
    Adjust these coordinates until you reliably select the Text tool.
    """
    try:
        # Example global coordinate for the Text tool.
        # (These values should be adjusted based on your Paintbrush UI.)
        text_tool_x, text_tool_y = -1420, 720  # Adjust as needed.
        pyautogui.moveTo(text_tool_x, text_tool_y, duration=0.5)
        await asyncio.sleep(0.2)
        pyautogui.click()
        await asyncio.sleep(0.5)
        return {"content": [{"type": "text", "text": "Text tool selected."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error selecting text tool: {str(e)}"}]}

@mcp.tool()
async def add_text_in_paint(text: str) -> dict:
    """
    Copies the provided text to the clipboard, simulates pasting via Command+V,
    then simulates pressing the Return key to "Place" the text, and finally
    clicks at the center of the rectangle (assumed at given coordinates) so that
    the placed text is centered.
    
    This method bypasses interacting with a popup text dialog by directly issuing
    the paste and return commands.
    """
    try:
        # selects text tool
        result_text_tool = await select_text_tool()
        print(result_text_tool)
        await asyncio.sleep(2)
        
        # double clicks on the text entry area
        text_entry_x, text_entry_y = -700, 900
        pyautogui.moveTo(text_entry_x, text_entry_y, duration=0.5)
        await asyncio.sleep(0.2)
        pyautogui.doubleClick()
        await asyncio.sleep(0.5)

        # Copy the provided text to the clipboard using pbcopy.
        cmd = "echo " + shlex.quote(text) + " | pbcopy"
        subprocess.run(cmd, shell=True, check=True)
        await asyncio.sleep(0.3)
        
        # Activate Paintbrush (assumed to be frontmost) and paste the text.
        # This simulates pressing Command+V.
        pyautogui.hotkey("command", "v")
        await asyncio.sleep(0.3)
        place_x, place_y = -620, 1054
        pyautogui.moveTo(place_x, place_y, duration=0.5)
        await asyncio.sleep(0.3)
        pyautogui.click()
        await asyncio.sleep(0.3)

        center_x, center_y = -800, 900  # Adjust based on your actual rectangle center.
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        await asyncio.sleep(0.3)
        pyautogui.click()
        await asyncio.sleep(0.3)

        # while True:
        #     # Get the current mouse position
        #     x, y = pyautogui.position()

        #     # Check for mouse click (this checks for left-click)
        #     if pyautogui.mouseInfo() == "left":
        #         print(f"Mouse clicked at coordinates: ({x}, {y})")
        #         break

        # await asyncio.sleep(0.1)  # Add a small delay to avoid excessive CPU usage
        return {"content": [{"type": "text", "text": f"Text '{text}' placed inside the rectangle."}]}


            # return {"content": [{"type": "text", "text": f"Error clicking Place button: {stderr.decode().strip()}"}]}

            
       
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error in paste_and_place_text: {str(e)}"}]}




@mcp.tool()
async def gmail_send(to:str, subject:str, message:str):
    """Send an email using the Gmail client"""
    gmail_client = await gmailClient.GmailClient().create()
    if not to or not subject  or not message:
        return {"status": "error", "error": "Missing required parameters: 'to', 'subject', 'message'"}
    # Call the Gmail client to send the email
    return await gmail_client.send_email(to, subject, message)


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
