Estrutura do Banco de Dados
O banco de dados utilizado é o clinica_veterinaria.db, que contém as seguintes tabelas:

1- clientes

id: Identificador único do cliente (chave primária).
nome: Nome do cliente.
telefone: Número de telefone do cliente.
email: Endereço de e-mail do cliente.
endereco: Endereço do cliente.
cpf: Número do CPF do cliente (único).

2- pets

id: Identificador único do pet (chave primária).
nome_pet: Nome do pet.
cliente_id: ID do cliente a quem o pet pertence (chave estrangeira).

3- amostras

id: Identificador único da amostra (chave primária).
nome_racao: Nome da amostra de ração.

4- distribuicoes

id: Identificador único da distribuição (chave primária).
cliente_id: ID do cliente que recebe a amostra (chave estrangeira).
amostra_id: ID da amostra distribuída (chave estrangeira).

5- usuarios

id: Identificador único do usuário (chave primária).
username: Nome de usuário para login.
senha: Senha do usuário.
email: Endereço de e-mail do usuário.
Funções Relacionadas ao Banco de Dados

1. conectar_bd()
Esta função estabelece uma conexão com o banco de dados clinica_veterinaria.db utilizando a biblioteca sqlite3. Em caso de erro na conexão, um aviso é exibido.

2. cadastrar_cliente()
Descrição: Esta função coleta informações do cliente, pet e amostra de ração a partir da interface gráfica e registra essas informações nas tabelas apropriadas do banco de dados.
Processo:
Conecta ao banco de dados.
Verifica se os campos obrigatórios estão preenchidos.
Verifica se o CPF já está cadastrado.
Insere os dados do cliente na tabela clientes.
Insere os dados do pet na tabela pets, se fornecidos.
Insere a amostra de ração na tabela amostras, se fornecida, e registra a distribuição na tabela distribuicoes.
Exibe uma mensagem de sucesso ou erro conforme o resultado da operação.

3. buscar_cliente_ou_pet()
Descrição: Esta função busca informações de clientes, pets ou amostras de ração com base nos critérios fornecidos pelo usuário na interface.
Processo:
Conecta ao banco de dados.
Monta uma query SQL com base nos campos de busca preenchidos.
Executa a query e recupera os resultados.
Exibe os resultados ou um erro, caso não haja resultados.

4. registrar_usuario(username, senha, email, confirmacao_senha)
Descrição: Registra um novo usuário no sistema.
Processo:
Verifica se todos os campos estão preenchidos e se as senhas coincidem.
Conecta ao banco de dados e insere os dados do novo usuário na tabela usuarios.
Exibe uma mensagem de sucesso ou erro conforme o resultado da operação.
Interface Gráfica
A interface gráfica é construída com Tkinter e é dividida em três abas:

Login: Permite que usuários se autentiquem.
Cadastrar: Onde os usuários podem cadastrar novos clientes, pets e amostras.
Buscar: Para procurar informações de clientes, pets e amostras.
