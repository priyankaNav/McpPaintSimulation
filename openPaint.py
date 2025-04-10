# basic import 

from PIL import Image as PILImage
import math
import sys
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
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
from pdb import set_trace

def is_paintbrush_running():
    """Check if Paintbrush is currently running"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == "Paintbrush":
            return True
    return False

async def open_paint():
    """Open Paintbrush application on macOS main display"""
    try:
        print("\n=== Starting open_paint ===")
        
        # Check if Paintbrush is installed
        paintbrush_path = "/Applications/Paintbrush.app"
        if not os.path.exists(paintbrush_path):
            print("Paintbrush.app not found in /Applications")
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paintbrush.app not found in /Applications"
                    )
                ]
            }
        
        print("Paintbrush.app found, attempting to open...")
        
        # Simple approach to open Paintbrush
        subprocess.run(["open", paintbrush_path], check=True)
        await asyncio.sleep(3)  # Wait for app to launch
        
        if not is_paintbrush_running():
            print("Failed to launch Paintbrush")
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Failed to launch Paintbrush"
                    )
                ]
            }
        
        print("Paintbrush launched successfully")
        
        # Get main display metrics
        main_display = Quartz.CGMainDisplayID()
        main_width = int(Quartz.CGDisplayPixelsWide(main_display))
        main_height = int(Quartz.CGDisplayPixelsHigh(main_display))
        
        print(f"Main display dimensions: {main_width}x{main_height}")
        
        # Try to maximize the window on main display
        maximize_script = '''
        tell application "Paintbrush"
            activate
        end tell
        delay 1
        tell application "System Events"
            tell process "Paintbrush"
                set frontmost to true
                delay 1
                tell window 1
                    -- Position at top-left of main display
                    set position to {0, 0}
                    delay 1
                    -- Click the green button to maximize
                    click button 1
                end tell
            end tell
        end tell
        '''
        
        subprocess.run(["osascript", "-e", maximize_script], check=True)
        print("Window maximized on main display")
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paintbrush opened and maximized on main display"
                )
            ]
        }
        
    except Exception as e:
        print(f"Error in open_paint: {e}")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paintbrush: {str(e)}"
                )
            ]
        }

# For testing the function directly
if __name__ == "__main__":
    result = asyncio.run(open_paint())
    print(result)