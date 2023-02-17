Lista para o chá de casamento
==========================================

## 1. Pré-requisitos


- `Python 3.8.8` e `pip`;
  - Recomendação de utilização do `pyenv` (<https://github.com/pyenv/pyenv>);
- Usuário local adicionado ao grupo `docker` (<https://docs.docker.com/install/linux/linux-postinstall/>);
  - Caso queira ignorar esse passo, execute comandos docker com 'sudo';

## 2. Desenvolvimento

Para instalar as dependências do projeto utilize o seguinte comando:

```bash
pip install -r requirements.txt
```
É preciso entrar no ambiente virtual para rodar o projeto.

Para rodar o projeto utlize:
```bash
 django-admin runserver
 ```
 em caso de erro com o banco, rode a migração com:

```bash
 django-admin migrate
 ```

Para criar um super usuário utilize:

```bash
 django-admin createsuperuser
 ```
