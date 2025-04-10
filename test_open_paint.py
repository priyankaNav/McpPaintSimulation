import asyncio
import subprocess
import pyautogui
import re

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

async def draw_rectangle_with_tool() -> dict:
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

        bounds = await get_window_bounds( window_index=2)
        if not bounds or len(bounds) != 4:
            print("Canvas window bounds could not be retrieved.")
            return

        window_x, window_y, width, height = bounds
        print(f"Window bounds: {bounds}")

        # Calculate the center of the window.
       
        center_x = -700
        center_y = 900

        # For better results, first ensure the canvas is focused by clicking at its center.
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        await asyncio.sleep(0.2)
        pyautogui.click()  # Focus the canvas
        await asyncio.sleep(0.5)

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
       
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()

            # Check for mouse click (this checks for left-click)
            if pyautogui.mouseInfo() == "left":
                print(f"Mouse clicked at coordinates: ({x}, {y})")
                break

        await asyncio.sleep(0.1)  # Add a small delay to avoid excessive CPU usage

        return {"content": [{"type": "text", "text": "Rectangle drawn at the center of the Paintbrush window."}]}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error drawing rectangle with tool: {str(e)}"}]}


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



# Example usage:
if __name__ == "__main__":
    async def main():
        # result_open = await open_paint()
        # print(result_open)
        
        # # Wait for the window to reposition.
        # await asyncio.sleep(3)
        
        # result_tool = await select_rectangle_tool()
        # print(result_tool)
        
        # # Wait a moment for the tool selection to settle.
        # await asyncio.sleep(2)
        
        # result_draw = await draw_rectangle_with_tool()
        # print(result_draw)

        result_open = await open_paint()
        print(result_open)

        # Allow time for windows to settle.
        await asyncio.sleep(3)
        
        # Optionally, reposition individual windows if needed. For example:
        # Reposition Toolbox (window 1) and Canvas (window 2) to your extended display.
        await reposition_window(window_index=1, left=-1470, top=0, width=1470, height=956, app_name="Paintbrush")
        await reposition_window(window_index=2, left=-1470, top=0, width=1470, height=956, app_name="Paintbrush")
        await asyncio.sleep(2)

        # Select the rectangle tool from the Toolbox.
        result_tool = await select_rectangle_tool()
        print(result_tool)
        await asyncio.sleep(2)
        
        # Draw the rectangle on the Canvas.
        result_draw = await draw_rectangle_with_tool()
        print(result_draw)

        
    asyncio.run(main())