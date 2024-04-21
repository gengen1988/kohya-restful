@echo off

IF NOT EXIST venv (
    echo Creating venv...
    python -m venv .venv
)

:: activate python env
call .\.venv\Scripts\deactivate.bat
call .\.venv\Scripts\activate.bat

:: dependencies for server
pip install -r requirements.txt

:: dependencies for kohya
pushd sd-scripts
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade -r requirements.txt
pip install xformers==0.0.23.post1 --index-url https://download.pytorch.org/whl/cu118
accelerate config
popd ..

:: exit env
call .\.venv\Scripts\deactivate.bat
