# Documentação

## Lado Servidor
Servidor armazena as fichas, permite troca de informação entre as fichas e a consulta e manutenção do usuário quanto a elas. 
As classes implementam diferentes tipos de atributos que o Dungeon Master (quem cria a ficha base, implementando-a no código segundo o código base), vai poder personalizar de acordo com o seu uso e regras de combate.


- Atributos: 
    (se classificam como atributos características do próprio personagem)

    Atributo_C 
    (nessa classe são criados atributos que não são modificados, inatos do personagem como nome, classe, raça, são atributos de string)

        - nome
        - classe
        set_nome
        get_nome

    Atributo_V
    (atributos que tem um valor em número que são habilidades e são usados como base para rolagem de dados)

        - nome
        - valor
        - dado
        
        set_nome
        get_nome
        rola_dado
        set_valor
        get_valor
    
    Equipamentos
    (itens coletaveis permanentes)

        - nome
        - quantidade
        - [nomes]

        set_nome
        get_nome
        add_item
        remove_item


    Atributo_B
    (características do personagem que são consumidos)
    
        - nome
        - valor
        - valor_max

        set_nome
        get_nome
        set_valor
        get_valor
        receive_number

- Utilizaveis: 
    
    Arma

        - nome
        - dado
        - cartucho
        - n_cartuchos

        set_nome
        get_nome
        roll_dano
        set_cartucho

    Habilidade:

        -nome
        -dado
        -custo
        
        set_nome
        get_nome
        roll_dado
        set_custo
        get_custo
        

- Sheet: 
    SheetType(template)
        - number = 0
        - atributos_count
        - Table_ref

        display (att, hab, arma)
        
    SheetInstance
        - number
        - atributos_count


- Table:
    - name
    - user

    setname
    getname
    setuser
    getuser



Backups
Thread join de backup
csv para salvar as mesas e fichas
#PREOCUPAÇÃO COM O LAG ALTO


///////////////////////////////////////
/////////////////FICHA/////////////////
///////////////////////////////////////
///Nome:      Clover              /////
///Classe:         Humano         /////
///Vida:                          /////
///Mana:                          /////
///Equipamentos:                  /////
///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////