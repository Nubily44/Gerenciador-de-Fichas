# Documentação

# Server - Side
Armazena todas as informações sobre as fichas, atualiza valores e executa métodos da ficha segundo solicitado por players e pelo DungeonMaster.

#
Ficha: 
#
    Atributos: 
        Atributo_B (duas variáveis int): Atributo básico, possui um valor em número: atual, valor máximo, e pode ser atualizado conforme uso. Armazena valores como Vida, Mana, Esforço, etc.
            Métodos: Setters, Getters, ModifyAtr(valor), isZero(), isLessthan()
        Atributo_C (string): Atributo categórico, possui um valor, geralmente em texto (string), e é raramente alterado. Armazena valores como Raça, Cor, Classe, etc.
            Métodos: Setname, Getname

        Atributo_V (int): Atributo valorado, possui um valor fixo (variável dependendo de upgrades), que serve de base para rolagens de perícia. Armazena valores como destreza, força, inteligência, etc
            Métodos: GetValue, RollAtr, UpgradAtr, Advantage(), Disadvantage()
#
    Equipamentos:
        estão organizados em diferentes listas
        Para equipamentos como Utilizáveis é necessário que se adicione na mao os valores nos atributos que são afetados por buff, ou será necessário adicionar um método para cada atributo (como acontece em equipamentos permanentes)

        Armas: possuem caractéristicas como dano, nome e dados atrelados a ele etc
           Métodos: Get/Set, Rolldice, calculatedamage, Advantage, Disadvantage, 
        
        Utilizáveis: possuem características como custo, nome, usos etc
            Métodos: Use(), Capacity(),

        Permanentes: Que não tem limite de uso, como objetos, cordas
            Métodos: , Add(), Get()
#
    Métodos:
        Roll_dados: rola dados para ações ou mudanças na ficha genéricos
#
Implementações na main:
        Trocas de mensagens: trocas de mensagens entre o cliente e o servidor

        Implementação de comandos de ataque, buffs, etc

Metódos para criar pós conexão:
RollUse()

