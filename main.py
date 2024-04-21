import sys
import os
import asyncio
from typing import Annotated
from fastapi import Body, FastAPI, HTTPException

app = FastAPI()


@app.post("/{url_path:path}")
async def proxy(url_path: str, args: Annotated[list[str] | None, Body()] = None):

    script_path = os.path.abspath(f"{url_path}.py")
    print("request:", script_path, args)
    if not os.path.exists(script_path):
        raise HTTPException(status_code=404, detail="Script not found")

    # Create subprocess with dynamic arguments
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        script_path,
        *args,
        stdout=asyncio.subprocess.PIPE,  # Capture standard output
    )

    # Stream output directly to current process stdout
    async for line in proc.stdout:
        sys.stdout.buffer.write(line)
        sys.stdout.buffer.flush()

    await proc.wait()
    return script_path
