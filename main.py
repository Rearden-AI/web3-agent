# pylint: disable=unused-import
import uvicorn
from app import app


if __name__ == '__main__':
    uvicorn.run("main:app", port=6013, host="0.0.0.0", reload=True, reload_excludes=["*.log"])
