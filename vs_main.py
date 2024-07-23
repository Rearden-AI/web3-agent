import uvicorn
from vectorstore_updater_app import app

if __name__ == '__main__':
    uvicorn.run("vs_main:vectorstore_updater_app", port=6017, host="0.0.0.0", reload=True, reload_excludes=["*.log"])
