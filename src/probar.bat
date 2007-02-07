echo off
for %%v in (*.java) do (
echo -------------------------%%v-------------------
type %%v  
echo --------------------------------------------------
echo pulse intro para iniciar el analisis
python lexico.py %%v | more
pause

)
