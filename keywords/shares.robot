*** Settings ***
Library    SikuliLibrary
Library    keywords.py

*** Variables ***
${PATH_IMAGES}    C:/Users/use/Desktop/payments-reports-bot/images
${USERNAME}    julio.franca
${PASSWORD}    franca@2023.

*** Keywords ***
Load Folder images
    Add Image Path    ${PATH_IMAGES}
    Log    Imagens carregadas com sucesso! ${PATH_IMAGES}    console=True
Wait and Click
    [Arguments]    ${image}    ${timeout}=5
    Wait Until Screen Contain    ${image}    ${timeout}
    Click    ${image}

Choice Option
    [Arguments]    ${option}
    Click At Position    (531,360)
    Press Special Key    UP
    Press Special Key    UP
    FOR    ${counter}    IN RANGE    0    ${option}
        Press Special Key    DOWN
        Sleep    1
    END
    Sleep    1    
    Press Special Key    ENTER

Wait Can Open Excel
    ${encontrado}=    Run Keyword And Return Status    Wait Until Screen Contain    alert_excel_icon.png    120
    WHILE    ${encontrado} == False
        Sleep    2
        ${encontrado}=    Run Keyword And Return Status    Wait Until Screen Contain    alert_excel_icon.png    120
    END

 Wait Excel is Opened
    ${encontrado}=    Run Keyword And Return Status    Wait Until Screen Contain    is_opened_excel_icon.png    120
    WHILE    ${encontrado} == False
        Sleep    2
        ${encontrado}=    Run Keyword And Return Status    Wait Until Screen Contain    is_opened_excel_icon.png    120
    END