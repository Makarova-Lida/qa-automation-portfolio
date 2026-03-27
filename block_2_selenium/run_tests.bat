@echo off
chcp 65001 > nul
echo === Selenium Test Runner ===

if "%1"=="" goto show_help
if "%1"=="show_cases" goto show_cases
if "%1"=="run_tests" goto run_tests
if "%1"=="test_skillbox" goto test_skillbox
if "%1"=="clean" goto clean
goto show_help

:show_cases
echo Показываю все тест-кейсы...
C:\User_1\envs\test_env_v2\.venv\Scripts\python.exe -m pytest src/tests --collect-only -q
goto end

:run_tests
echo Запускаю все тесты...
C:\User_1\envs\test_env_v2\.venv\Scripts\python.exe -m pytest src/tests -v
goto end

:test_skillbox
echo Запускаю только тест Skillbox...
C:\User_1\envs\test_env_v2\.venv\Scripts\python.exe -m pytest src/tests/test_skillbox.py::TestSkillbox::test_skillbox_title -v
goto end

:clean
echo Очищаю кеш pytest...
C:\User_1\envs\test_env_v2\.venv\Scripts\python.exe -m pytest --cache-clear
echo Кеш очищен
goto end

:show_help
echo Доступные команды:
echo   run_tests.bat show_cases  - показать все тест-кейсы
echo   run_tests.bat run_tests   - запустить все тесты
echo   run_tests.bat test_skillbox - запустить только тест Skillbox
echo   run_tests.bat clean       - очистить кеш pytest

:end