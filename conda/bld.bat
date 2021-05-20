if "%INSTALL_PREFIX%" == "" set INSTALL_PREFIX=%cd%\pipelines_install & call tools\make_and_install.bat

move %INSTALL_PREFIX%\pipelines-test %CONDA_PREFIX%\lib\
