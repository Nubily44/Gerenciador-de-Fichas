
Menu de funções

Mensagens: DM
    - iniciar mesa
        identifica o ip do dm -> id 1
        devolve o código da mesa

    - ver ficha de outra pessoa
    
    - modificar ficha de outra pessoa 

    - fechar mesa

Mensagens gerais:
    - conectar à mesa como player (insere código da mesa) (manda numero de id)

    - criar personagem (ficha) 
        recebe como ack o id do personagem como sucesso
    - alterar alguma informação de ficha existente
        -adicionar atributos
        -dependendo do tipo de atributo vem com info a mais
        (avisa a alteração também para o DM)

    - adicionar item
        dependendo do tipo adiciona caracteristicas a mais

    - ver ficha/salvar/atualizar
    
    - usar atributo (proprio)

    - usar atributo em alguém

    - rolagem de dado simples

    - Status online e dead man switch 
#
    
nome = input("Qual seria o nome do seu personagem?")
classe = input("Qual seria a classe do seu personagem?")
vida = input("Qual seria a quantidade de vida do seu personagem?")
mana = input("Qual seria a quantidade de mana do seu personagem?")
hab1 = input("Qual seria sua primeira habilidade?")
hab2 = input("Qual seria sua segunda habilidade?")    

#