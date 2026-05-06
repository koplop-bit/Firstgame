@echo off
echo Installing requirements...
pip install Pillow pyinstaller

echo Creating icon...
python create_icon.py

echo Building executable...
pyinstaller --noconsole --icon=icon.ico --name "SpaceInvaders" game/main.py

echo Copying assets...
xcopy images dist\SpaceInvaders\images\ /E /I /Y
if exist highscore.txt copy highscore.txt dist\SpaceInvaders\ /Y
if exist life_scores.txt copy life_scores.txt dist\SpaceInvaders\ /Y
if exist upgrades.json copy upgrades.json dist\SpaceInvaders\ /Y

echo Done! The game is in the dist\SpaceInvaders folder.
