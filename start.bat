:: activate python env
call .\.venv\Scripts\deactivate.bat
call .\.venv\Scripts\activate.bat

:: start server
uvicorn main:app