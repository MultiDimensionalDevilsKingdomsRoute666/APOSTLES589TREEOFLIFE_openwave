@echo off
setlocal enabledelayedexpansion
pushd "%~dp0..\..\..\.."

REM Remove __pycache__ under pipeline_engine
for /d /r "openwave\xperiments\m4_ewt\pipeline_engine" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

cls

REM ---------------------------------------------------------------
REM Test list. One module per line, trailing caret for continuation,
REM last line no caret. Add new tests here.
REM ---------------------------------------------------------------
set TESTS=^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_units ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_units_integration ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_features ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_wc_factory ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_sampling ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_evolution_multifield ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_nonlinearity ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_emc ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_variable_coeff ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_sources ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_boundary ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_wc_reflector ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_motion ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_energy_budget ^
 openwave.xperiments.m4_ewt.pipeline_engine.physics._test_stability ^
 openwave.xperiments.m4_ewt.pipeline_engine._test_experiment_runner ^
 openwave.xperiments.m4_ewt.pipeline_engine._check_dimensional_literals ^
 openwave.xperiments.m4_ewt.pipeline_engine._smoke_test

set FAILED=0

echo ============================================================
echo   M4 pipeline_engine test suite
echo ============================================================
echo.

for %%T in (%TESTS%) do (
    echo [run] %%T
    python -m %%T
    if errorlevel 1 (
        echo   *** FAIL: %%T ***
        set FAILED=1
    )
    echo.
)

REM ---------------------------------------------------------------
REM Tests with extra arguments. Kept out of TESTS because cmd's
REM for-loop parses the pipe character in the parenthesised list
REM before the loop body runs, which aborts the block.
REM ---------------------------------------------------------------
echo [run] openwave.xperiments.m4_ewt.pipeline_engine.physics._demo --no-window --steps 300
python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo --no-window --steps 300
if errorlevel 1 (
    echo   *** FAIL: _demo ***
    set FAILED=1
)
echo.

echo [run] openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_k_sweep --grid 32 --steps 20 --out "%TEMP%\m4_k_sweep_smoke"
python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_k_sweep --grid 32 --steps 20 --out "%TEMP%\m4_k_sweep_smoke"
if errorlevel 1 (
    echo   *** FAIL: _demo_k_sweep ***
    set FAILED=1
)
echo.

echo ============================================================
if !FAILED!==1 (
    echo   *** SOME TESTS FAILED ***
    popd
    exit /b 1
)
echo   *** ALL TESTS PASSED ***
popd
exit /b 0
