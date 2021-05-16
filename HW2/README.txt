Content:
  - result.txt:         The log file of my training and solving.
                        This file will be OVERWRITTEN next time the program run.
                        So please make a backup if you need.

  - sliding_puzzle.py:  The program including training part and solving part.

  - my_matrix.q:        My trained Q-Matrix to the optimal result with given puzzle.

  - pseudo_code.txt:    Pseudo code for my Q Learning algoirhtm.


Usage example:
1)
python3 sliding_puzzle.py
Start 100000(default value) episodes of training

2)
python3 sliding_puzzle.py -e 0 -l
Load a pretrained Q-Matrix and skip training

3)
python3 sliding_puzzle.py -e 30000 -l
Load a pretrained Q-Matrix and do 30000 more episodes of training on it.


For reproducing the same result:
I have included Q-Matrix I used to get the best result.
You can use load that Q-Matrix to reproduce my result.
Usage example 2 would be proper for that.


Final words:
Because the training process involve randon searching,
a new training from empty Q-Matrix may not give the best answer.
And my Q-Matrix may not give the optimal solution to other puzzles.


Thank you for reading.
