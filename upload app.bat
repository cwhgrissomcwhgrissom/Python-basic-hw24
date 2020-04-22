@ECHO OFF
git add .

git commit -m app.py

git push -f heroku master

pause

exit
ECHO finish