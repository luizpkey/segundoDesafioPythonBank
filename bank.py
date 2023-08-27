def clear():
   try:
      import os
      lines = os.get_terminal_size().lines
   except AttributeError:
      lines = 130
   print("\n" * lines)

def realizar_saque(*, saldo, numero_saques, extrato, limite_saques, limite_valor_saque):
   saque = input("Digite o valor do saque: ")
   try:
      saque = float(saque)
      if numero_saques >= limite_saques:
         print("Você já efetuou seu limite de {} saques hoje".format(numero_saques))
      elif saque>0:
         if saque>(limite_valor_saque):
            print("Essa operação ultrapassa o limite da operacao")
         elif saque>(saldo):
            print("Essa operação ultrapassa o seu saldo")
         else:
            numero_saques += 1
            extrato +="{}".format(numero_saques) + ".o saque de R${:.2f}\n".format(saque)
            saldo -= saque
      else:
         print("Saque inválido")
   except:
      print("Valor inválido")
   return saldo, extrato, numero_saques

def efetuar_deposito(saldo, extrato, /):
   deposito = input("Digite o valor do deposito: ")
   try:
      deposito = float(deposito)
      if deposito>0:
         extrato+= "Deposito de R${:.2f}\n".format(deposito)
         saldo += deposito
      else:
         print("Deposito inválido")
   except:
      print("Valor digitado inválido")
   return saldo, extrato

def exibir_extrato(saldo,/,*,extrato):
   clear()
   print("="*50)
   print("Sem operações executadas" if not extrato else extrato)
   print("="*50)
   print("Seu saldo é de R${:.2f}".format(saldo))

def filtrar_usuario(usuarios, cpf):
   usuario_selecionado=[usuario for usuario in usuarios if usuario["cpf"] == cpf]
   return usuario_selecionado[0] if usuario_selecionado else None
def criar_usuario(usuarios):
   nome=input("Digite o nome: ")
   cpf=input("Digite o cpf: ")
   if cpf=="":
      print("CPF não pode ser vazio")
   elif not filtrar_usuario(usuarios, cpf):
      usuarios.append({"nome": nome, "cpf": cpf})
   else:
      print("CPF já cadastrado")
   return

def main():
   menu_inicial = """
      Bem vindo ao banco
      Selecione uma opção:
      1. [u] Cadastrar usuario (Create user)
      2. [c] Criar conta (Create account)
      3. [x] Selecionar conta (Select account)
      4. [q] Sair (Exit)
   """
   menu = """
   1. [e] Extrato (Check Balance)
   2. [d] Deposito (Deposit)
   3. [s] Saque (Withdraw)
   4. [q] Sair (Exit)
   """

   LIMITE_VALOR_SAQUE=500
   LIMITE_SAQUES=3

   conta_selecionada = []
   contas=[]
   usuarios=[]

   while True:
      if conta_selecionada:
         print(menu)
         opcao = input("Digite uma opção: ")
         opcao=opcao.lower()

         if opcao == "e" or opcao=="1":
            exibir_extrato(saldo,extrato=extrato)
         elif opcao == "d" or opcao=="2":
            saldo,extrato=efetuar_deposito(saldo, extrato)
         elif opcao == "s" or opcao=="3":
            saldo,extrato,numero_saques=realizar_saque(extrato=extrato,
                                                       saldo=saldo,
                                                       numero_saques=numero_saques,
                                                       limite_saques=LIMITE_SAQUES,
                                                       limite_valor_saque=LIMITE_VALOR_SAQUE)
         elif opcao == "q" or opcao=="4":
            conta_selecionada["saldo"]=saldo
            conta_selecionada["extrato"]=extrato
            conta_selecionada["numero_saques"]=numero_saques
            conta_selecionada=[]
         else:
            print("Opção inválida")
      else:
         print(menu_inicial)
         opcao = input("")
         opcao=opcao.lower()
         if opcao=="x" or opcao=="3":
            if len(contas)>0:
               conta_selecionada=selecionar_conta(contas)
               if conta_selecionada:
                  saldo=conta_selecionada["saldo"]
                  extrato=conta_selecionada["extrato"]
                  numero_saques=conta_selecionada["numero_saques"]
            else:
               print("Nenhuma conta cadastrada")
         elif opcao=="u" or opcao=="1":
            criar_usuario(usuarios)
         elif opcao=="c" or opcao=="2":
            cadastrar_conta(usuarios,contas)
         elif opcao=="q" or opcao=="4":
            break

def selecionar_conta(contas):
   clear()
   print("="*50)
   print("Selecione uma conta")
   for i, conta in enumerate(contas):
      print("[{}] - {}".format(conta["conta"], conta["nome"]))
   print("="*50)
   while True:
      print("Digite -1 para sair")
      numero = input("Digite o numero da conta: ")
      try:
         numero = int(numero)
         if numero == -1:
            break
         conta_selecionada=[conta for conta in contas if conta["conta"] == numero]
         if conta_selecionada[0]:
            break
      except:
         print("Opção inválida")
   return conta_selecionada[0] if conta_selecionada else None

def criar_conta(usuario, contas):
   saldo=0
   extrato=""
   numero_saques=0
   return { "agencia":"0001", "conta": len(contas)+1, "nome": usuario["nome"], "cpf": usuario["cpf"], "saldo": saldo, "extrato": extrato, "numero_saques": numero_saques}
def cadastrar_conta(usuarios, contas ):
   print("Bem vindo ao banco")
   print("Dados do cliente:")
   cpf = ""
   while True:
      if not cpf:
         cpf=input("Digite o cpf: ")
      else:
         print("cpf {}".format(cpf))
      usuario=filtrar_usuario(usuarios, cpf)
      if usuario:
         conta = criar_conta(usuario, contas)

         contas.append(conta)
         break
      else:
         print("CPF não cadastrado")
         break
   return contas

main()