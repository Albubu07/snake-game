# snake-game

Grupo:  
**João Pedro de Aquino Duarte  
Yasminn Costa Moura Silva  
Arthur Albuquerque Santos  
Pedro de Souza Leão Pereira Magnata  
Heitor Luiz dos Santos Silva  
Nina Schettini Lundgren  **

### Arquitetura do Projeto
O código organiza o jogo Cinsnake no Pygame através de quatro funções principais, cada uma representando um nível, com configurações próprias de tempo, velocidade, cores, quantidade de itens e inimigos. Em cada nível, a lógica funciona na classe Game, que controla todo o ciclo: inicialização, posicionamento de elementos, atualização do estado, controle de colisões, renderização na tela e verificação de vitória ou derrota. Além disso, há classes externas (Snake, Item e Hunter, importadas de outros arquivos) responsáveis por comportamentos específicos: a Snake gerencia o movimento, crescimento e colisões da cobra; a Item representa frutas e vidas no jogo, com reposicionamento controlado; e a Hunter atua como inimigo móvel que atrapalha ou colide com a cobra. O código ainda possui funções auxiliares para tocar músicas e efeitos sonoros, além do menu para iniciar o jogo e escolher os níveis. 

### Screenshots
![image](https://github.com/Albubu07/snake-game/blob/main/versões/images/image1.png)  
Primeiro código de teste realizado, mas ainda adquirindo conhecimentos sobre o pygame e pensando o que poderíamos fazer para atingir as metas.  

![image](https://github.com/Albubu07/snake-game/blob/main/versões/images/image2.png)  
Segundo código concluído, metas parcialmente atingidas, faltava apenas a implementação de POO que estávamos em processo de aprendizagem ainda.  

![image](https://github.com/Albubu07/snake-game/blob/main/versões/images/image3.jpeg)  
Terceiro código completo com todas as metas alcançadas antes do prazo, nos permitindo ampliar nosso jogo para as sprites.  

![image](https://github.com/Albubu07/snake-game/blob/7f1c1992d6a4e9acda99e7d685353b8c31b98bbd/vers%C3%B5es/images/image4.jpeg)  
Último código desenvolvido aplicando sprites e deixando o jogo mais bonito.  

Aqui estão algumas telas do jogo:


### Ferramentas utilizados
Para o desenvolvimento do projeto, utilizamos o GitHub como sistema de controle de versão e o Visual Studio Code como ambiente de desenvolvimento integrado. A implementação do jogo é realizada através da biblioteca Pygame, que oferece funcionalidades essenciais para criação de jogos 2D em Python.
Como fonte de consulta técnica, empregamos o GeeksForGeeks para esclarecimento de conceitos e implementações específicas. Além disso, utilizamos recursos de inteligência artificial de forma pontual para resolução de problemas técnicos no desenvolvimento do código.

### Conceitos implementados
Para realização do código utilizamos os conceitos técnicos aprendidos em sala de aula (loops, funções, classes, condicionais), bem como tentamos realizar o código da maneira mais eficiente e limpa possível, salvando os nomes das variáveis de maneira que qualquer programador possa saber o que cada variável significa no código. Tentamos nos basear no livro "Arquitetura limpa" para nos ajudar a estruturar nosso jogo. Implementamos while loops para o game loop principal de cada nível e for loops para iteração sobre eventos do pygame e múltiplos hunters, garantindo processamento eficiente de coleções. Já para as classes, utilizamos orientação a objetos com classes importadas (Snake, Item, Hunter) e a classe interna Game que encapsula o estado e comportamentos de cada nível, demonstrando encapsulamento e composição. As condicionais para controlar os estados do fluxo do jogo (vitória, derrota), e implementamos gerenciamento de estado com flags booleanas, tratamento de eventos, uso de constantes globais, estruturas de dados (tuplas para cores, listas para exclusões), controle de timing com delta time, e separação de responsabilidades através de métodos específicos.
### Divisão do Trabalho
Quando idealizamos o projeto, cada um de nós fez parte de algo que contribuiu exponencialmente para o desenvolvimento próspero do nosso jogo. Heitor e Artur construiram uma boa parte do jogo bruto, enquanto o resto de nós apenas revisava e realizávamos melhorias no código bruto, Yasminn e Nina fizeram alguns Sprites para as telas de início, fim, coletáveis e ajudaram também a colocar as músicas, enquanto Artur, Pedro e João mexiam no GitHub para enviar as atualizações. Para a organização do código, Pedro estruturou todo o código em classes de maneira clara e organizada, de modo a facilitar a implementação dos níveis do jogo, bem como João, Artur e Pedro ajudaram a escrever o relatório. João fez os slides em ligação no discord junto aos demais membros, o que ajudou de maneira bastante positiva.
### Aprendizado
Ao realizar este trabalho, pudemos aprender e vivenciar na prática na parte de desenvolvimento de jogos utilizando o pygame dentre outras bibliotecas. Aprendemos a trabalhar em equipe e dividir os trabalhos para obtermos uma maior eficiência na realização do jogo, bem como pesquisamos e aprendemos mais sobre POO dentre outras coisas (realização de sprites, implementação dos coletáveis, máquina de estados finitos, etc...). Aprendemos também como organizar e dispor melhor nosso código, no que tange ao versionamento dele (utilizando o GitHub), como também no que tange à organização em si do código, das variáveis e das funções.
### Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
Nosso maior erro foi que ao passarmos a cobra (função) para a cobra (classe) o jogo fica com um bug no qual se o jogador apertar as teclas Baixo-esquerda ou Baixo-Direita, a cobra morre. Tentamos consertar o bug diretamente na classe, mas não obtivemos muito sucesso. Entretando, basta o jogador apertar os botões com parcimônia para que o bug seja evitado.
### Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
Basicamente o pouco tempo para aprendermos POO, bem como a mudança das funções para as classes dos objetos. Acreditamos que o semestre encurtado e as provas de outras cadeiras foram desafios que contornamos através da organização e da divisão das tarefas de maneira dinâmica, o que ajudou bastante nossa equipe à alcançar nosso resultado desejado.




