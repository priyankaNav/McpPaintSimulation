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
import pyautogui
import Quartz
import time
import os
import psutil
import asyncio
import ctypes
import pdb
# instantiate an MCP server client
mcp = FastMCP("Calculator")
rectangle_info = {
    'start_x': None,
    'start_y': None,
    'rect_width': None,
    'rect_height': None
}
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


# @mcp.tool()
# async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
#     """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
#     global paint_app
#     try:
#         if not paint_app:
#             return {
#                 "content": [
#                     TextContent(
#                         type="text",
#                         text="Paint is not open. Please call open_paint first."
#                     )
#                 ]
#             }
        
#         # Get the Paint window
#         paint_window = paint_app.window(class_name='MSPaintApp')
        
#         # Get primary monitor width to adjust coordinates
#         primary_width = GetSystemMetrics(0)
        
#         # Ensure Paint window is active
#         if not paint_window.has_focus():
#             paint_window.set_focus()
#             time.sleep(0.2)
        
#         # Click on the Rectangle tool using the correct coordinates for secondary screen
#         paint_window.click_input(coords=(530, 82 ))
#         time.sleep(0.2)
        
#         # Get the canvas area
#         canvas = paint_window.child_window(class_name='MSPaintView')
        
#         # Draw rectangle - coordinates should already be relative to the Paint window
#         # No need to add primary_width since we're clicking within the Paint window
#         canvas.press_mouse_input(coords=(x1+2560, y1))
#         canvas.move_mouse_input(coords=(x2+2560, y2))
#         canvas.release_mouse_input(coords=(x2+2560, y2))
        
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
#                 )
#             ]
#         }
#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error drawing rectangle: {str(e)}"
#                 )
#             ]
#         }

# @mcp.tool()
# async def add_text_in_paint(text: str) -> dict:
#     """Add text in Paint"""
#     global paint_app
#     try:
#         if not paint_app:
#             return {
#                 "content": [
#                     TextContent(
#                         type="text",
#                         text="Paint is not open. Please call open_paint first."
#                     )
#                 ]
#             }
        
#         # Get the Paint window
#         paint_window = paint_app.window(class_name='MSPaintApp')
        
#         # Ensure Paint window is active
#         if not paint_window.has_focus():
#             paint_window.set_focus()
#             time.sleep(0.5)
        
#         # Click on the Rectangle tool
#         paint_window.click_input(coords=(528, 92))
#         time.sleep(0.5)
        
#         # Get the canvas area
#         canvas = paint_window.child_window(class_name='MSPaintView')
        
#         # Select text tool using keyboard shortcuts
#         paint_window.type_keys('t')
#         time.sleep(0.5)
#         paint_window.type_keys('x')
#         time.sleep(0.5)
        
#         # Click where to start typing
#         canvas.click_input(coords=(810, 533))
#         time.sleep(0.5)
        
#         # Type the text passed from client
#         paint_window.type_keys(text)
#         time.sleep(0.5)
        
#         # Click to exit text mode
#         canvas.click_input(coords=(1050, 800))
        
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Text:'{text}' added successfully"
#                 )
#             ]
#         }
#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error: {str(e)}"
#                 )
#             ]
#         }

# @mcp.tool()
# async def open_paint() -> dict:
#     """Open Microsoft Paint maximized on secondary monitor"""
#     global paint_app
#     try:
#         paint_app = Application().start('mspaint.exe')
#         time.sleep(0.2)
        
#         # Get the Paint window
#         paint_window = paint_app.window(class_name='MSPaintApp')
        
#         # Get primary monitor width
#         primary_width = GetSystemMetrics(0)
        
#         # First move to secondary monitor without specifying size
#         win32gui.SetWindowPos(
#             paint_window.handle,
#             win32con.HWND_TOP,
#             primary_width + 1, 0,  # Position it on secondary monitor
#             0, 0,  # Let Windows handle the size
#             win32con.SWP_NOSIZE  # Don't change the size
#         )
        
#         # Now maximize the window
#         win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
#         time.sleep(0.2)
        
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text="Paint opened successfully on secondary monitor and maximized"
#                 )
#             ]
#         }
#     except Exception as e:
#         return {
#             "content": [
#                 TextContent(
#                     type="text",
#                     text=f"Error opening Paint: {str(e)}"
#                 )
#             ]
#         }
# DEFINE RESOURCES


# Function to open Paintbrush and move it to secondary monitor and maximize
@mcp.tool()
async def open_paint():
    global paint_app
    try:
        print("\n=== Starting open_paint debug ===")
        
        # Debug: Check Paintbrush installation
        paintbrush_path = "/Applications/Paintbrush.app"
        print(f"Checking Paintbrush at: {paintbrush_path}")
        if os.path.exists(paintbrush_path):
            print("✓ Paintbrush.app found")
        else:
            print("✗ Paintbrush.app not found")
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paintbrush.app not found in /Applications"
                    )
                ]
            }

        # Debug: Check display setup
        print("\nChecking display setup...")
        maxDisplays = 16
        CGDirectDisplayIDArrayType = Quartz.CGDirectDisplayID * maxDisplays
        activeDisplays = CGDirectDisplayIDArrayType()
        displayCount = ctypes.c_uint32()

        status = Quartz.CGGetActiveDisplayList(
            maxDisplays,
            activeDisplays,
            ctypes.byref(displayCount)
        )
        pdb.set_trace()
        print(f"Display status: {status}")
        print(f"Number of displays: {displayCount.value}")

        if status != 0 or displayCount.value < 2:
            print("✗ No extended display found")
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Extended display not found. Please connect a second monitor."
                    )
                ]
            }

        # Debug: Get display metrics
        print("\nGetting display metrics...")
        primary_display = activeDisplays[0]
        secondary_display = activeDisplays[1]
        
        primary_width = int(Quartz.CGDisplayPixelsWide(primary_display))
        secondary_x = int(Quartz.CGDisplayBounds(secondary_display).origin.x)
        secondary_y = int(Quartz.CGDisplayBounds(secondary_display).origin.y)
        
        print(f"Primary display width: {primary_width}")
        print(f"Secondary display position: ({secondary_x}, {secondary_y})")

        # Debug: Launch Paintbrush
        print("\nLaunching Paintbrush...")
        try:
            # Method 1: Direct launch
            print("Trying direct launch...")
            subprocess.run(["open", paintbrush_path], check=True)
            await asyncio.sleep(3)
            
            if is_paintbrush_running():
                print("✓ Paintbrush launched successfully")
            else:
                print("✗ Direct launch failed, trying NSWorkspace...")
                # Method 2: NSWorkspace
                workspace = Quartz.NSWorkspace.sharedWorkspace()
                app_url = Quartz.NSURL.fileURLWithPath_(paintbrush_path)
                workspace.openURL_(app_url)
                await asyncio.sleep(3)
                
                if is_paintbrush_running():
                    print("✓ Paintbrush launched with NSWorkspace")
                else:
                    print("✗ NSWorkspace launch failed")
                    return {
                        "content": [
                            TextContent(
                                type="text",
                                text="Failed to launch Paintbrush"
                            )
                        ]
                    }

            # Debug: Position and maximize
            print("\nPositioning and maximizing window...")
            position_script = f'''
            tell application "System Events"
                tell process "Paintbrush"
                    set frontmost to true
                    delay 1
                    if exists window 1 then
                        set position of window 1 to {{{secondary_x}, {secondary_y}}}
                        delay 1
                        tell window 1
                            click button 1
                        end tell
                    end if
                end tell
            end tell
            '''
            
            print("Executing position script...")
            subprocess.run(["osascript", "-e", position_script], check=True)
            print("✓ Position script executed")

            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paintbrush opened and positioned on extended display"
                    )
                ]
            }

        except subprocess.CalledProcessError as e:
            print(f"✗ Script error: {e}")
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Error executing script: {str(e)}"
                    )
                ]
            }

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }
    finally:
        print("=== End of open_paint debug ===\n")

# Helper function to check if Paintbrush is running
def is_paintbrush_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "Paintbrush":
            return True
    return False


# Function to draw rectangle in Paintbrush
@mcp.tool()
async def draw_rectangle() -> dict:
    try:
        if not is_paintbrush_running():
             return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }

        maxDisplays = 16
        activeDisplays = (Quartz.CGDirectDisplayID * maxDisplays)()
        displayCount = Quartz.uint32_t()
        Quartz.CGGetActiveDisplayList(maxDisplays, activeDisplays, Quartz.pointer(displayCount))

        if displayCount.value < 2:
            raise Exception("No second monitor detected.")

        second_display = activeDisplays[1]
        x_offset = Quartz.CGDisplayBounds(second_display).origin.x
        y_offset = Quartz.CGDisplayBounds(second_display).origin.y

        global start_x, start_y, rect_width, rect_height
        rectangle_info['start_x']  = x_offset + 200
        rectangle_info['start_y'] = y_offset + 200
        rectangle_info['rect_width'] = 300
        rectangle_info['rect_height'] = 200

        pyautogui.moveTo(start_x, start_y)
        pyautogui.mouseDown()
        pyautogui.moveRel(rect_width, 0)
        pyautogui.moveRel(0, rect_height)
        pyautogui.moveRel(-rect_width, 0)
        pyautogui.moveRel(0, -rect_height)
        pyautogui.mouseUp()

        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({rectangle_info['start_x']},{rectangle_info['start_y']}))"
                )
            ]
        }

    except Exception as e:
        print(f"Error in draw_rectangle: {e}")
        return {"status": "error", "message": str(e)}

@mcp.tool()
# Function to add text to the center of the rectangle
async def add_text_in_paint(text: str):
    try:
        if not is_paintbrush_running():
            print("Paintbrush is not open. Please open it first.")
            return {"status": "error", "message": "Paintbrush is not open."}
        
        if None in rectangle_info.values():
            print("Rectangle not drawn yet. Cannot add text.")
            return {"status": "error", "message": "Rectangle not drawn yet."}


        center_x = rectangle_info['start_x'] + rectangle_info['rect_width'] // 2
        center_y = rectangle_info['start_y'] + rectangle_info['rect_height'] // 2

        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        pyautogui.write(text, interval=0.1)

        return {"status": "success", "message": f"Text added: {text}"}

    except Exception as e:
        print(f"Error in add_text_to_rectangle: {e}")
        return {"status": "error", "message": str(e)}


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
