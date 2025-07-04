*** Settings ***
Resource    ../../keywords/keywords.robot
Test Setup    Load Folder images

*** Test Cases ***
Export Reports Pending
    Open FJFrigo
    Do Login FJFrigo
    Select Reports Pending
    Open Excel
    Save Excel File    RelatorioParcelasPendentes
    Close FJFrigo