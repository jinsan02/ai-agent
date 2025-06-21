from mcp.server.fastmcp import FastMCP
import subprocess
import os
import traceback

mcp = FastMCP(
    name="ExplorerCommander",
    instructions="You can open a specific folder using Windows Explorer. Accepts folder keywords like 'downloads', 'desktop', etc.",
    host="0.0.0.0",
    port=8008,
)

# 기본 경로 매핑
FOLDER_MAP = {
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "videos": os.path.join(os.path.expanduser("~"), "Videos"),
}


@mcp.tool()
async def open_folder(name: str = "downloads") -> str:
    """
    Open a specified folder using Windows Explorer.

    Args:
        name (str): One of: downloads, desktop, documents, pictures, videos

    Returns:
        str: Message indicating result
    """
    try:
        name = name.lower()
        if name not in FOLDER_MAP:
            return (
                f"❌ 지원하지 않는 폴더입니다: '{name}'. "
                f"다음 중 하나를 사용해주세요: {', '.join(FOLDER_MAP.keys())}"
            )

        folder = FOLDER_MAP[name]
        if not os.path.exists(folder):
            return f"❌ 폴더 경로가 존재하지 않습니다: {folder}"

        subprocess.Popen(["explorer", folder])
        return f"✅ '{name}' 폴더를 열었습니다."

    except Exception as e:
        print("📛 오류 발생:", traceback.format_exc())
        return f"❌ 폴더 열기 중 시스템 오류 발생: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
