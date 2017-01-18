# cometaseats web scrapper
Web scrapper simples escrito em Python, utilizando [Scrapy](https://scrapy.org/), utilizado para extrair dados de utilização de poltronas do site da Viação Cometa.


## Instalação

Para usa-lo, é necessário  [instalar a versão atual do Scrapy](https://doc.scrapy.org/en/latest/intro/install.html#intro-install). 

Após isso, faça o download da versão atual do cometaseats, extraia, vá até o diretório cometaseats e execute o comando `scrapy crawl cometaseats`. Se você deseja que o dado extraído seja salvo em um arquivo json, utilize o comando `scrapy crawl cometaseats -o items.json -t json` para salvar no arquivo items.json. 

Após a extração, execute o arquivo `analyze.py` no mesmo diretório que o arquivo `items.json`.
