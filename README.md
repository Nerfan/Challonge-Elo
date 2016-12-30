# Challonge-Elo

## Credits

Many thanks to the good people at [challonge](http://challonge.com) for providing a fantastic platform to run tournaments from and for developing their API.

Thanks also to GitHub user [russ-](https://github.com/russ-) for creating [pychallonge](https://github.com/russ-/pychallonge), a module for python that makes the challonge API a breeze to work with. That repository is the source of the challonge folder in this project.

Authors: Jeremy Lefurge ([Nerfan](https://github.com/Nerfan)) and Scott Csefai ([swc19](https://github.com/swc19))

## Usage

1. Assuming that you already have Python 3.5 installed, the first step is to clone this repository.

   ```
   $ git clone https://github.com/Nerfan/Challonge-Elo.git
   ```

   Or if you'd rather not use the terminal, simply download the .zip and unpack it somewhere.

2. Then inside the directory just created, create a file called setCredentials.py that contains the following two lines:

   ```python
   import challonge
   challonge.set_credentials("USERNAME", "API_KEY")
   ```

   replacing `USERNAME` and `API_KEY` with your information, while keeping the surrounding quotes.

   Alternatively, you could edit readTourney.py and replace the line

   ```python
   import setCredentials
   ```

   with the code block above.

3. Then, in readTourney.py edit the list of tournaments. The variable `TOURNAMENT_IDS_SEPARATED_BY_COMMAS` represents this list. Spaces are optional in the listing.

4. OPTIONAL: One the tournament ids are entered, run `$ ./save_tournaments.py`. If this is your first time running the program, this step is unnecessary. When you run `./calculate_elos.py`, Python will see that the files do not exist yet, and will automatically call `./save_tourneys.py`. If you wish to update the list of tournaments, this step is necessary.

5. After that, you should be good to simply run `$ ./calculate_elos.py`, and elo rankings will be displayed and saved to elos.txt.

6. If you would like to see a specific player's head-to-head records against all other players, type their name when prompted. If you would like to see details (match scores, dates) about their head-to-head with another specific player, enter their name when prompted. No input will back out of either prompt.

## Additional Configuration

The `DEFAULT_ELO` variable in readTourney.py can be adjusted as you wish in order to change the starting elo for new players.

The function calculateWin in player.py can be changed as you like. For example, you can change the k value to have a larger fluctuation in elos following a match. The entire formula could be changed, though it must still take arguments for elos befrore calculations and must return a tuple of the resulting elos.

If you do not wish for elos to be displayed or saved, comment out the respective line at the end of readTourney.py.

You can create a file called aliases.py containing only the declaration of a dictionary called aliases in order to allow for multiple names for the same competitor. For example:

```python
aliases = {
    "JEREMY LEFURGE" : "NERFAN"
}
```

would result in any mentions of JEREMY LEFURGE in a tournament to count towards the elo of NERFAN. Do note that all names should be full caps.
