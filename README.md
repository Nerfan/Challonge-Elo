# Challonge-Elo

## Credits

Many thanks to the good people at [challonge](http://challonge.com) for providing a fantastic platform to run tournaments from and for developing their API.

Thanks also to GitHub user [russ-](https://github.com/russ-) for creating [pychallonge](https://github.com/russ-/pychallonge), a module for python that makes the challonge API a breeze to work with. That repository is the source of the challonge folder in this project.

Authors: Jeremy Lefurge ([Nerfan](https://github.com/Nerfan)) and Scott Csefai ([swc19](https://github.com/swc19))

## Dependencies

The Python 3 modules `iso8601` and `xlsxwriter` are required. They can be obtained by simply running `pip3 install iso8601 xlsxwriter`.

## Usage

1. Assuming that you already have Python 3.5 installed, the first step is to clone this repository.

   ```
   $ git clone https://github.com/Nerfan/Challonge-Elo.git
   ```

   Or if you'd rather not use the terminal, simply download the .zip and unpack it somewhere.

2. Then inside the directory just created, create a file called set\_credentials.py that contains the following two lines:

   ```python
   import challonge
   challonge.set_credentials("USERNAME", "API_KEY")
   ```

   replacing `USERNAME` and `API_KEY` with your information, while keeping the surrounding quotes.

   Alternatively, the script will prompt the user for their information if this file is not found.

3. Create a file called `tournamentlist.py`, and inside the file create a list of tournament ids called `tourneys`. For example:
   ```python
   tourneys = ["id1", "id2", "account-tourneyid"]
   ```
   If the tournaments are from a subdomain on challonge, it should be in the format {subdomain}-{tourney-id} (e.g. 'test-mytourney' for test.challonge.com/mytourney).


4. Once the tournament ids are entered, run `$ ./save_tourneys.py`. If this is your first time running the program, this step is unnecessary. When you run `./calculate_elos.py`, Python will see that the files do not exist yet, and will automatically call `./save_tourneys.py`. If you wish to update the list of tournaments, this step is necessary.

5. After tournaments have been saved, run `$ ./calculate_elos.py`. This will process the tournaments and save the relevant output to the `output` folder.

## Additional Configuration

The `DEFAULT_ELO` variable in `player.py` can be adjusted as you wish in order to change the starting elo for new players.

If `IGNOREGAMES` is set to `True` in `player.py`, then all set scores are treated the same (i.e. a 3-2 win is the same as a 3-0 win).

You can (and most likely will be required to) create a file called aliases.py containing only the declaration of a dictionary called aliases in order to allow for multiple names for the same competitor. For example:

```python
aliases = {
    "JEREMY LEFURGE" : "NERFAN"
}
```

would result in any mentions of JEREMY LEFURGE in a tournament to count towards the elo of NERFAN. Do note that all names should be full caps.
