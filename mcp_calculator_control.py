from mcp.server.fastmcp import FastMCP
import subprocess
import psutil

mcp = FastMCP(
    name="CalculatorCommander",
    instructions="You can launch or close the Windows Calculator.",
    host="0.0.0.0",
    port=8007,
)

@mcp.tool()
async def launch_calculator() -> str:
    """Launch Windows Calculator."""
    try:
        subprocess.Popen(["calc.exe"])
        return "✅ 계산기가 실행되었습니다."
    except Exception as e:
        return f"❌ 계산기 실행 중 오류 발생: {str(e)}"

@mcp.tool()
async def close_calculator() -> str:
    """Close all Calculator processes."""
    try:
        count = 0
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"] and "calc" in proc.info["name"].lower():
                proc.kill()
                count += 1
        return f"✅ 계산기 {count}개 종료됨." if count > 0 else "ℹ️ 실행 중인 계산기가 없습니다."
    except Exception as e:
        return f"❌ 계산기 종료 중 오류 발생: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
