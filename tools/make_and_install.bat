mkdir build
cd build

echo building in %cd%
cmake -G"Visual Studio 16 2019" -A x64 -DCMAKE_CXX_STANDARD=20 -DWITH_CTEST=Off -DCMAKE_INSTALL_PREFIX=%INSTALL_PREFIX% -DPYTHON_EXECUTABLE=%CONDA_PREFIX%\python ..\test

:: Show cmake settings
cmake -B . -S .. -LA

:: C++ tests
cmake --build . --target pipelines-test --config Release -- /m:%NUMBER_OF_PROCESSORS% || echo ERROR && exit /b
pipelines-test.exe || echo ERROR && exit /b

:: Build and install Python library
cmake --build . --target install --config Release -- /m:%NUMBER_OF_PROCESSORS% || echo ERROR && exit /b
