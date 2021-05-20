if "%INSTALL_PREFIX%" == "" set INSTALL_PREFIX=%cd%\pipelines_install & call tools\make_and_install.bat

dir /s /b %INSTALL_PREFIX%

move %INSTALL_PREFIX%\pipelines-test %CONDA_PREFIX%\lib\
