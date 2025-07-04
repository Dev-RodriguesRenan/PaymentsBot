*** Settings ***
Resource    ../../keywords/keywords.robot
Test Setup    Load Folder images

*** Test Cases ***
Export Reports Lows
    Open FJFrigo
    Do Login FJFrigo
    Select Reports Lows
    ${result}    Check If Is Possible Generate Report
    IF    ${result} == False
        Log    Não é possível gerar o relatório de parcelas pendentes. Verifique se há parcelas pendentes no sistema.    console=True
    ELSE
        Log    Gerando relatório de baixas...    console=True
        Open Excel
        Save Excel File    RelatorioRealizacoesBaixas
        Close FJFrigo
    END