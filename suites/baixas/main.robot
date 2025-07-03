*** Settings ***
Resource    ../keywords/keywords.robot
Test Setup    Load Folder images

*** Test Cases ***
Export Reports Lows
    Open FJFrigo
    Do Login FJFrigo
    Select Reports Lows
    Open Excel
    Save Excel File    RelatorioRealizacoesBaixas
    Close FJFrigo