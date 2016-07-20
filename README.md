# Challonge-Elo

## Credits

Many thanks to the good people at [challonge](http://challonge.com) for providing a fantastic platform to run tournaments from and for developing their API.

Thanks also to GitHub user russ- for creating [pychallonge](https://github.com/russ-/pychallonge), a module for python that makes the challonge API a breeze to work with. That repository is the source of the challonge folder in this project.

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

   replacing USERNAME and API_KEY with your information, while keeping the surrounding quotes.

   Alternatively, you could edit readTourney.py and replace the line

   ```python
   import setCredentials
   ```

   with the second line of the code block above.

3. Then, in readTourney.py edit the list of tournaments. The variable TOURNAMENT_IDS_SEPARATED_BY_COMMAS represents this list. Spaces are optional in the listing.

4. After that, you could be good to simply run `$ python readTourney.py`, and elo rankings will be saved to elos.txt.

## Additional Configuration

The DEFAULT_ELO variable in readTourney.py can be adjusted as you wish in order to change the starting elo for new players.

The function calculateWin in readTourney.py can be changed as you like. For example, you can change the k value to have a larger fluctuation in elos following a match. The entire formula could be changed, though it must still take arguments for elos befrore calculations and must return a tuple of the resulting elos.

If you do not wish for elos to be displayed or saved or a plot made, comment out the respective line at the end of readTourney.py.

You can create a file called aliases.py containing only the declaration of a dictionary called aliases in order to allow for multiple names for the same competitor. For example:

```python
aliases = {
    "JEREMY LEFURGE" : "NERFAN"
}
```

would result in any mentions of JEREMY LEFURGE in a tournament to count towards the elo of NERFAN. Do note that all names should be full caps.
