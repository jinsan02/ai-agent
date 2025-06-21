from mcp.server.fastmcp import FastMCP
import subprocess
import os
import signal
import psutil

mcp = FastMCP(
    name="DesktopCommander",
    instructions="You can launch or close desktop applications such as notepad.",
    host="0.0.0.0",
    port=8006,  # 필요 시 포트 변경 가능
)

# 메모장 실행을 위한 프로세스 저장
notepad_process = None


@mcp.tool()
async def launch_notepad() -> str:
    """
    Launch Windows Notepad application.

    Returns:
        str: Success message
    """
    global notepad_process
    try:
        notepad_process = subprocess.Popen(["notepad.exe"])
        return "✅ 메모장이 실행되었습니다."
    except Exception as e:
        return f"❌ 메모장 실행 중 오류 발생: {str(e)}"


@mcp.tool()
async def close_notepad() -> str:
    """
    Forcefully close all running Notepad processes.

    Returns:
        str: Success message
    """
    try:
        count = 0
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"] and "notepad.exe" in proc.info["name"].lower():
                proc.kill()
                count += 1
        if count > 0:
            return f"✅ 메모장 {count}개 종료됨."
        else:
            return "ℹ️ 실행 중인 메모장이 없습니다."
    except Exception as e:
        return f"❌ 메모장 종료 중 오류 발생: {str(e)}"


if __name__ == "__main__":
    # stdio 기반 MCP로 실행
    mcp.run(transport="stdio")

