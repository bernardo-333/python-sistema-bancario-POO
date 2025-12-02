# Sistema Bancário — Desafio DIO Backend Python (Luizalabs)

Este repositório contém uma implementação de um sistema bancário simples em Python, desenvolvido como parte do **desafio do curso DIO - Backend Python Luizalabs**.

O objetivo deste projeto é consolidar os conceitos básicos de Python e aplicar os princípios de Programação Orientada a Objetos (POO) em um contexto prático e didático.

---

## 💡 Sobre o código

O sistema simula operações bancárias essenciais, como cadastro de clientes, abertura de contas, depósitos, saques e consulta de extrato. Todos os recursos são acessíveis por meio de um menu interativo, diretamente no terminal.

Principais conceitos utilizados:
- Classes, herança e encapsulamento
- Abstração com classes abstratas (`abc`)
- Organização modular e reutilização de código
- Uso de listas para armazenar clientes e contas
- Registro de histórico de operações (extratos)

---

## 🗂️ Estrutura de Classes

- `Cliente`: Classe base para clientes, responsável por vincular contas e efetuar transações.
- `PessoaFisica`: Herda de Cliente, adicionando atributos como nome, CPF e data de nascimento.
- `Conta`: Classe base para contas bancárias, controla saldo, número e agência.
- `ContaCorrente`: Herda de Conta, implementa limites e restrições de saque.
- `Historico`: Armazena movimentações (depósitos, saques) feitas na conta.
- `Transacao` (abstrata): Interface para operações de depósito e saque.
- `Deposito` e `Saque`: Implementações concretas de operações financeiras.

---

## 🛠️ Como executar

1. Tenha o **Python 3** instalado na sua máquina.
2. Clone o repositório:
   ```bash
   git clone https://github.com/bernardo-333/python-sistema-bancario-POO.git
   cd python-sistema-bancario-POO
   ```
3. Execute o arquivo principal:
   ```bash
   python desafio-POO.py
   ```
4. Siga o menu apresentado no terminal para interagir com o sistema.

---

## ✨ Funcionalidades

- **Cadastro de cliente** (Pessoa Física)
- **Abertura de conta corrente**
- **Depósito e saque** (com limites de valor e quantidade)
- **Extrato bancário** (lista movimentações e saldo)
- Organização e histórico por cliente e conta

---

## 🎯 Objetivo do desafio

Este exercício foi proposto no curso da DIO com objetivo de:
- Consolidar conceitos de POO (herança, encapsulamento, abstração)
- Praticar a modelagem de classes e atributos em Python
- Simular as regras de negócios de um sistema bancário básico

---

## 📄 Observações

- **Não há persistência em banco de dados:** Todas as informações existem apenas durante a execução.
- **Sistema 100% terminal:** Não possui interface gráfica ou web.
- O código pode ser expandido para novos requisitos — sugestões são bem-vindas!

---

## 📚 Licença

Este projeto é livre para estudos, aprimoramento e uso não comercial, seguindo os termos da licença MIT.

---

Se tiver dúvidas sobre funcionamento do código, sua estrutura ou conceitos de POO em Python, fique à vontade para perguntar ou sugerir melhorias!
