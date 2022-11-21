# Back-end

Comando responsavel para instalar o ambiente virtual no nosso projeto:  

```python -m venv venv```

Inicializar o ambiente virtual:  
```source venv/bin/activate```

Instalar as dependências do projeto:  
```pip install -r requirements.txt```

Atualizar o arquivo de dependências, caso haja novas dependencias:  

``pip freeze > requirements.txt``

Inicializar o Projeto

`` uvicorn main:app --reload ``

Criacao do Banco de Dados

`` python create_tables_database.py ``

