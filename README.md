IHC-projeto
===========

Repositório para o projeto de IHC - protótipo de interface para comunicação com crianças com deficiência


Para Executar
-----------

Só rodar no terminal um dos seguintes comandos
* ./main.py
* python3 main.py


Dependências
-----------

* Python3 (3.2)
* Qt 5.2.1
* PyQt 5.2.1
(testado com essas versões)

Para a vocalização de símbolos (opcional):
* Módulo QtMultimedia do Qt5 devidamente instalado e funcionando.
* Conexão a internet (somente na primeira vez que um símbolo é vocalizado)
* Engine de Text-to-Speech comum do sistema instalada (exemplo, eSpeak em Linux, SAPI5 que já com Windows Vista/7/8)

O sistema tenta primeiro tocar um símbolo se o arquivo .mp3 de áudio dele existir, se não existir, ele tenta adquirir
o arquivo pela API online do Google Translate. Se por alguma razão não conseguir (sem internet, por exemplo), ele
irá tentar usar alguma engine TTS comum que esteja instalada adequadamente no sistema.
É recomendado rodar algumas vezes com conexão e QtMultimedia para adquirir os arquivos de TTS da google, pois 
usualmente a qualidade deles é bem melhor que TTSs do sistema.


Conteúdo do Repositório
------------

* esse README
* main.py: script principal, o ponto de partida.
* simbolos: pasta com as imagens de símbolos que fizemos, organizadas hierarquicamente.
* dpcs: pasta com os scripts do programa.
* dpcs/steel: uma biblioteca open source que usamos, com poucas modificações, para facilitar o uso de engines TTS do sistema.
* dpcs-database.dat: arquivo gerado pelo programa - é o database de simbolos, categorias e outros atributos salvos.
* speeches: pasta gerada pelo programa, contendo os arquivos .mp3 gerados pelo Google Translate para vocalização dos símbolos.
* generate.py: script utilitário para gerar o database inicial do projeto de forma mais rápida
