# Projeto Correia
## Autor
- Vítor Amorim Fróis 
- vitor0frois@gmail.com; frois@usp.br
- Setembro/2024

## Explicação
Utilizar uma câmera acoplada em um módulo Raspberry Pi para disparar um atuador ao desalinhar de uma correia.

O programa deve ser utilizado via terminal.

## Instalação
Abra um terminal e no diretório principal do programa, digite:
``` bash
chmod +x ./install.sh 
chmod +x ./program.sh 
./install.sh python venv
```

## Uso
No terminal, digite:
Abra um terminal e no diretório principal do programa, digite:
``` bash
./program.sh python venv
```

- Ajuste o Threshold (Opção 1), valor que define a diferença de iluminação entre a correia e o fundo. Um valor ideal de threshold
não deve ter nem muitas sombras nem muitas luzes, mostrando com clareza onde está a correia.
- Ajuste o multiplicador (Opção 2), que define a regularidade da figura que vai aproximar a correia. Um bom valor tem estabilidade, isto é, não fica piscando, e tem poucas pontas.
- Opção 3 para testar o programa e 4 para ver a saída