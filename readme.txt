Equipe:
- David Alves Soares (511125)
- Francisco Breno da Silveira (511429)
- Pedro Emanuel Ferreira Paiva das Neves (510727)

Para executar este código é necessário ter o Python3 (ou superior) instalado. Além disso, é necessário instalar a biblioteca matplotlib, que pode ser instalado com o comando 'pip install matplotlib' no terminal. As bibliotecas 'random' e 'os' também foram utilizadas, mas por serem padrões do python, não precisam ser instaladas separadamente.

Esse programa possui uma "interface" iterativa onde o usuário poderá escolher o que deseja realizar. Siga os passos abaixo para execução.
1 - Abra o terminal (cmd) na pasta do arquivo do programa.
2 - Rode o comando 'python3 main.py'. OBS: utilizo Linux, mas creio que em outro SO deva funcionar igualmente.
3 - Digite 1 para ir ao menu das experimentações ou digite 2 para execução padrão do programa.
    - Se a opção 1 for escolhida, o usuário terá mais duas opções: digitar 1 para executar a experimentação 01 ou digitar 2 para executar a experimentação 02.
      - Observação: Os parâmetros utilizados para os testes só podem ser alterados a nível de código, dentro do método correspondente. A seguir é listado o nome do método utilizado para implementar cada experimento.
        - Experimentação 01: experimentation_01();
        - Experimentação 02: experimentation_02().
    - Se a opção 2 for escolhida, será realizada a execução padrão do programa que solicitará ao usuário os valores para os seguintes parâmetros:
      - Tamanho da população;
      - Número de interações;
      - Taxa de eletismo;
      - Taxa de mutação.
    - Os demais parâmetros só podem ser alterados a nível de código.

Na raiz do projeto há uma pasta chamada "resultadoExperimentacao". Dentro dessa pasta há mais duas pastas representando cada bloco de experimentação.
Na pata correspondente a cada bloco, há um arquivo log.txt que guardará o log da execução de cada experimentação (experimentation_01() escreve no log.txt em "resultadoExperimentacao/bloco01" e experimentation_02 escreve no log.txt em "resultadoExperimentacao/bloco02").
Um gráfico será gerado para cada experimento contendo os valores da média do total de interações por taxa de eletismo (bloco 01) ou tamanho da população (bloco 02).

Logs também serão gerados na saída do programa (terminal) exibindo o resultado de cada interação do algoritmo e o resultado final após o término de uma interação.
