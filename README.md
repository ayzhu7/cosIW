# cosIW
Install PyDealer using pip with the following line

pip install pydealer

Additional information about installing PyDealer can be found here: https://pydealer.readthedocs.io/en/latest/usage.html#install-uninstall-with-pip

Within the file shortened_game.py, in line 278 and 279, these are the two variables which can be changed. Line 278, num_trials is the number of trials that will be averaged across. In line 279, cards_in_round is the amount of cards dealt to each player. 

Once these two values are fixed, to run the file, open terminal and type the line
python3 shortened_game.py

The output is an array with 2 values, where the first value is the average score per trick for the random agent, and the second value is the average score per trick for the Monte Carlo agent.

All of the code is my own work, except for the package that I used to import the cards.
