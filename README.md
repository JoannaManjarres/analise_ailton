# analise_ailton

Para rodar o codigo é necessario colocar na mesma pasta dos arquivos .py os dados armazenados no link: https://drive.google.com/drive/folders/1D_37tLnIMzOp2B3Ke25e_Ci0rFlPZss3?usp=share_link
neste link se encontram os beams inicialmente gerados na analise, na configuracao Tx/Rx [8X1] e TX [16X1].

No arquivo beam_analysis.py é realizado um plot (histogram) dos beams e um diagrama de radiacao do transmissor junto com a posicao do transmissor e dos receptores.
Na figura seguinte apresenta um exemplo.

![beam_2_position_distribution](https://user-images.githubusercontent.com/65310634/218185010-40c50eda-d82b-440b-84b2-6211ea213583.png)

No arquivo mimo_best_beams.py na linha 147 sao gerados os canais mimo, na 150 o canal mimo é pasado pelo DFT e na linha 153 sao geradas as matriz de valores complexos
Essas matrizes sao guardadas en arquivos .npz e depois no git analysis_data sao gerados os indices dos beams.
