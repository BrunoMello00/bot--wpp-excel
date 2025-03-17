# Bot WhatsApp com Excel

Este projeto é um bot que envia mensagens personalizadas via WhatsApp Web utilizando dados de uma planilha Excel.

## Descrição

O bot lê dados de uma planilha Excel, formata os números de telefone e envia mensagens personalizadas via WhatsApp Web para cada contato.

## Pré-requisitos

- Python 3.x
- ChromeDriver compatível com a versão do seu Google Chrome
- Bibliotecas Python:
  - pandas
  - selenium

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/BrunoMello00/bot--wpp-excel.git
    cd bot--wpp-excel
    ```

2. Instale as bibliotecas necessárias:
    ```bash
    pip install pandas selenium
    ```

3. Baixe o [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) e coloque-o no caminho especificado no script (`chrome_driver_path`).

## Uso

1. Prepare seu arquivo Excel (`pg.xlsx`) com as seguintes colunas:
   - `Nome`: Nome do contato
   - `Numero`: Número de telefone (com ou sem código do país e DDD)
   - `Link`: Link para ser enviado na mensagem

2. Execute o script:
    ```bash
    python bot_wpp_excel.py
    ```

3. Escaneie o QR Code no WhatsApp Web para logar.

4. O bot enviará as mensagens para os contatos listados na planilha.

## Contribuição

Se você deseja contribuir com este projeto, por favor, siga os passos abaixo:
1. Faça um fork deste repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

