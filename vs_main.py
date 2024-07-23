import uvicorn
from vectorstore_updater_app import vectorstore_updater_app

if __name__ == '__main__':
    uvicorn.run("vs_main:vectorstore_updater_app", port=6017, host="0.0.0.0", reload=True, reload_excludes=["*.log"])
