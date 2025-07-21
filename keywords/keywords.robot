*** Settings ***
Library    SikuliLibrary
Library    ./keywords.py
Resource    ./shares.robot

*** Keywords ***
Open FJFrigo
    Press Special Key    WIN
    Type With Modifiers    fjfrigo
    Press Special Key    ENTER

Do Login FJFrigo
    Wait Until Screen Contain    menu_fj_login.png    60
    Choice Option    5
    Sleep    2
    Press Special Key    TAB
    Sleep    2
    Press Special Key    TAB
    Sleep    2
    Fill Login Form
Fill Login Form
    Press Keys    ctrl    a
    Sleep    2
    Type With Modifiers    ${USERNAME}
    Press Special Key    TAB
    Sleep    2
    Type With Modifiers    ${PASSWORD}
    Press Special Key    TAB
    Sleep    2
    Press Special Key    ENTER

Select Reports Pending
    Sleep    5
    Key Down    ALT
    Type With Modifiers    313
    Key Up    ALT
    Wait Until Screen Contain    menu_pending.png    10
    Wait and Click    export_excel.png    10
    ${PRINT}    Exists    ok_cancel.png    12
    Run Keyword If    ${PRINT}    Press Special Key    ENTER

Select Reports Lows
    Sleep    5
    Key Down    ALT
    Type With Modifiers    315
    Key Up    ALT
    Sleep    5
    Type With Modifiers    13112024
    Wait and Click    export_excel.png    10

Open Excel
    Wait Can Open Excel
    Wait and Click    alert_excel_icon.png    10
    Wait Excel is Opened

Save Excel File
    [Arguments]    ${filename}
    Press Keys    ctrl    b
    Wait and Click    resources_icon.png    10
    Wait Until Screen Contain    is_opened_explore_icon.png    15
    ${new_filename}    Generate Filename With Date  ${filename}
    Type With Modifiers    ${new_filename}
    Press Special Key    ENTER
    Wait Excel is Opened
    Sleep    10    Espera 10s para o excel salvar a planilha
    Press Keys    alt    f4
    Sleep    3
    ${src}    Set Variable    C:/Users/use/Documents/${new_filename}.xlsx
    ${dst}    Set Variable     C:/Users/use/Desktop/payments-reports-bot/data/${new_filename}.xlsx
    Move    ${src}    ${dst}
    Log    \nPlanilha ${new_filename}.xlsx salva com sucesso!!    console=True 

Close FJFrigo
    Switch To Fj Frigo
    Press Keys    alt    f4
    Log    \nFJFrigo fechado com sucesso!    console=True

Check If Is Possible Generate Report
    ${WARN}    Exists    warning.png    8
    Run Keyword If    ${WARN}    Press Special Key    ENTER
    IF    ${WARN} == True
        RETURN    False
    ELSE
        RETURN    True
    END