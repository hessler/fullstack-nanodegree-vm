# rdb-fullstack
Common code for the Relational Databases and Full Stack Fundamentals courses.

# Tournament Results Project
The code for the Tournament Results Project can be found in the `vagrant/tournament` directory.

## Project Setup and Testing
To set up and test the Tournament Results Project, you will need to do the following:

1. Clone the repository: `git clone https://github.com/hessler/fullstack-nanodegree-vm.git`
2. Navigate to the cloned repository directory. For example, if you cloned to your Desktop on a Mac: `cd ~/Desktop/fullstack-nanodegree-vm/`.
3. Navigate to the `tournament` directory: `cd vagrant/tournament`
4. Launch the Vagrant Virtual Machine: `vagrant up`
5. Once the VM is powered on, log in to it: `vagrant ssh`
6. Navigate to the `tournament` directory: `cd /vagrant/tournament`
7. Create the SQL database:
    - `psql` _(enters psql command line interface)_
    - `\i tournament.sql` _(imports and runs SQL scripts)_
    - `\q` _(quits the psql command line interface)_
8. Run the testing file: `python tournament_test.py`
    - If all tests pass, you should see the output listed below.
9. Once you are done testing, log out of the VM: `exit`
10. Turn off the VM: `vagrant halt`

## Testing Output
If all of the tests pass successfully, you should see the following output. Note that after items 1-8 and the "Success!" message, there is additional output that is the result of an additional function in the `tournament_test.py` file, which creates and simulates a tournament of 16 players. The output from this function includes the number of players, number of rounds, round-by-round match-ups, and the final standings.

```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!

IT'S TOURNAMENT TIME!
------------------------

Number of Players: 16
Number of Rounds: 4

ROUND #1
------------------------
  > Match 1: Player Name (0-0) vs. Player Name (0-0)
  ...
  > Match 8: Player Name (0-0) vs. Player Name (0-0)

ROUND #2
------------------------
  > Match 1: Player Name (1-0) vs. Player Name (1-0)
  ...
  > Match 8: Player Name (0-1) vs. Player Name (0-1)

ROUND #3
------------------------
  > Match 1: Player Name (2-0) vs. Player Name (2-0)
  ...
  > Match 8: Player Name (0-2) vs. Player Name (0-2)

ROUND #4
------------------------
  > Match 1: Player Name (3-0) vs. Player Name (3-0)
  ...
  > Match 8: Player Name (0-3) vs. Player Name (0-3)

FINAL STANDINGS
------------------------
  1. Player Name (4-0)
  ...
  16. Player Name (0-4)

```
