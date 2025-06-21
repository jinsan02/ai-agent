from mcp.server.fastmcp import FastMCP
import pyautogui
import os
from datetime import datetime
import traceback

mcp = FastMCP(
    name="ScreenshotCommander",
    instructions="You can take a screenshot of the entire screen and save it to a file.",
    host="0.0.0.0",
    port=8009,
)

# 저장 폴더 설정
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
os.makedirs(SAVE_DIR, exist_ok=True)

@mcp.tool()
async def take_screenshot() -> str:
    """
    Capture a screenshot and save it as a PNG file.

    Returns:
        str: Path to the saved screenshot
    """
    try:
        # 타임스탬프 기반 파일 이름 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SAVE_DIR, filename)

        # 스크린샷 촬영 및 저장
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        return f"✅ 스크린샷이 저장되었습니다: {filepath}"
    
    except Exception as e:
        # traceback 정보도 함께 출력
        err = traceback.format_exc()
        print("ERROR (screenshot tool):", err)
        return f"❌ 스크린샷 저장 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
