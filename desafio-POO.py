import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime


# --- Cliente ------------------------------------
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.lista_contas = []

    def efetuar_transacao(self, conta, operacao):
        operacao.executar(conta)

    def vincular_conta(self, conta):
        self.lista_contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


# --- Conta --------------------------------------
class Conta:
    def __init__(self, numero, titular):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._titular = titular
        self._historico = Historico()

    @classmethod
    def abrir_conta(cls, titular, numero):
        return cls(numero, titular)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def titular(self):
        return self._titular

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito efetuado! ===")
            return True
        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, titular, limite=500, max_saques=3):
        super().__init__(numero, titular)
        self._limite = limite
        self._max_saques = max_saques

    def sacar(self, valor):
        saques_realizados = len(
            [
                mov
                for mov in self.historico.movimentacoes
                if mov["tipo"] == Saque.__name__
            ]
        )
        passou_limite = valor > self._limite
        excedeu_saques = saques_realizados >= self._max_saques
        if passou_limite:
            print("\n@@@ Operação falhou! Valor ultrapassa o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques atingido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return textwrap.dedent(
            f"""
            Agência:\t{self.agencia}
            Nº Conta:\t{self.numero}
            Titular:\t{self.titular.nome}
        """
        )


# --- Historico ----------------------------------
class Historico:
    def __init__(self):
        self._movimentacoes = []

    @property
    def movimentacoes(self):
        return self._movimentacoes

    def registrar_movimentacao(self, operacao):
        self._movimentacoes.append(
            {
                "tipo": operacao.__class__.__name__,
                "valor": operacao.valor,
                "momento": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


# --- Transacao ----------------------------------
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def executar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.registrar_movimentacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def executar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.registrar_movimentacao(self)


# --- Utilidades e Interface ---------------------
def menu():
    opcoes = """\n
    ================ MENU BANCÁRIO ================
    [d]\tDepositar
    [s]\tSacar
    [x]\tExtrato
    [ac]\tAbrir conta
    [lc]\tListar contas
    [cu]\tCadastrar cliente
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes))


def buscar_cliente_por_cpf(cpf, clientes):
    filtro = [cli for cli in clientes if cli.cpf == cpf]
    return filtro[0] if filtro else None


def recuperar_conta_cliente(cliente):
    if not cliente.lista_contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    # FIXME: Permitir escolher conta se houver mais de uma
    return cliente.lista_contas[0]


def opcao_deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    valor = float(input("Informe o valor do depósito: "))
    deposito = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.efetuar_transacao(conta, deposito)


def opcao_saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    valor = float(input("Informe o valor do saque: "))
    saque = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.efetuar_transacao(conta, saque)


def mostrar_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n================ EXTRATO ================")
    movimentos = conta.historico.movimentacoes
    extrato = ""
    if not movimentos:
        extrato = "Nenhuma movimentação registrada."
    else:
        for mov in movimentos:
            extrato += f"\n{mov['tipo']}:\n\tR$ {mov['valor']:.2f} em {mov['momento']}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF: ")
    if buscar_cliente_por_cpf(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (rua, nro - bairro - cidade/UF): ")
    cliente = PessoaFisica(nome=nome, nascimento=nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente cadastrado com sucesso! ===")


def abrir_conta(prox_numero, clientes, contas):
    cpf = input("Informe o CPF do titular: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado, abertura cancelada! @@@")
        return
    conta = ContaCorrente.abrir_conta(titular=cliente, numero=prox_numero)
    contas.append(conta)
    cliente.vincular_conta(conta)
    print("\n=== Conta aberta com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(str(conta))


# --- Loop Principal -----------------------------
def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "d":
            opcao_deposito(clientes)
        elif opcao == "s":
            opcao_saque(clientes)
        elif opcao == "x":
            mostrar_extrato(clientes)
        elif opcao == "cu":
            cadastrar_cliente(clientes)
        elif opcao == "ac":
            prox_numero = len(contas) + 1
            abrir_conta(prox_numero, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Opção inválida, tente novamente. @@@")


if __name__ == "__main__":
    main()
