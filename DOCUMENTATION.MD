## Relatórios:

### Borderô:

**Relatório de borderô** extraído do banco de dados, com dados feitos a partir do **Relatório de Clientes** e **Relatório Borderô** enviado pelo e-mail.

- Colunas em banco uteis para confronto:
    
    `filial`; `emissao`; `vencimento`; `nf`; `valor_da_parcela`; `valor_pendente`; `emitente` 
    

### Relatório de Parcelas Pendentes:

- Colunas da planilha baixada:
    
    `id`; `Valor da parcela`; `Documento`; `Valor_pendente`; `Emitente`; `C.N.P.J./C.P.F.`; `grupo_centro_de_custo`; `Centro de custo`.
    
- Regras de execução:
    - As execuções devem ocorrer somente em dia útil, isto é, de segunda a sexta-feira.
    - Os arquivos gerados em cada extração, de cada unidade devem ter o seguinte nome: **RelatorioParcelasPendentes_aaaammdd_hhmm**.xls. Neste caso, colocar a data invertida seguida do nome da unidade.
    - Gravar os dados em banco. **Não gravar todas as colunas**, somente as colunas indicadas no
    exemplo acima de parcelas pendentes.

### Relatório de Baixas:

- Colunas da planilha baixada:
    
    `data_baixa`; `id`; `valor`; `documento`; `emitente`; `cnpj_cpf`;`idcentro_custo`; `grupo_centro_custo`; `centro_custo` .
    
- Regras de preenchimento do filtro:
    - Colocar a data inicial para 13/11/2024. A data final já vem preenchida com a data do dia, então manter.
- Regras de execução:
    - As execuções devem ocorrer somente em dia útil, isto é, de segunda a sexta-feira.
    - Os arquivos gerados em cada extração, de cada unidade devem ter o seguinte nome: **RelatorioRealizacoesBaixas_aaaammdd_hhmm**.xls. Neste caso, colocar a data invertida seguida do nome da unidade.
    - Gravar os dados em banco. Não gravar todas as colunas, somente as colunas indicadas no exemplo acima de baixadas.

### Relatório de Pagamentos:

- Após extrair os dados dos relatórios do FJ, confrontar os dados do borderô com os dados dos relatórios. (ainda não entendi)
- Gerar um relatório **(.xlsx)** com as seguintes colunas:
    
    `CNPJ-CPF`;`Emitente`;`Documento`;`Valor`;`Valor Pendente`;`Data da Baixa`;`idcentro_custo`;`grupo_centro_custo`;`centro_custo` .
    
- Considerando que nessa geração terão título baixados e pendentes, sendo que nestes casos as colunas
Valor Pendente e Data da Baixa (pintadas) serão de preenchimento excludentes, ou seja, neste exemplo
na marca em amarelo o valor pendente está em branco pois o título foi baixado (pago) na referida data
da baixa. A marca em marrom indica que ainda existe valores pendentes, logo da data da baixa estão em
branco. Dessa forma a BMG Crédito terá visão dos emitentes que chegaram no borderô e quais pagaram
todo o valor devido e quanto dada emitente ainda está devendo.