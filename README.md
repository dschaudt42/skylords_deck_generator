# Skylords Deck Generator

This is a streamlit app, which allows you to generate random decks for Skylords Reborn.

## Basic usage

### Requirements

You need to have `python3` installed on your system. It is also recommended to use `pip` to install the required
packages. This can be done by running

```pip install -r requirements.txt```

### Starting the app

In order to start the app, you just have to run the command

```streamlit run app.py```

And that's it!
You now can generate random PvE and PvP decks.

### Changing parameters

Withing the file `config.txt`, you can find several parameters, which influence how the deck generation is done.
There are two different sections, one for PvE deck generation and one for PvP deck generation.

The first three lines in each section determine, how many units, buildings and spells the deck must contain at each
tier.
The default PvE configuration for example will always generate a deck with at least two units, one building and one
spell at each tier.

The last two lines determine, how many colors the deck may consist of.
So again, the default PvE configuration allows for decks with 1-2 different colors.

All of these parameters may be changed at will, but going to unreasonable numbers (e.g. requiring more than 20 cards
minimum) might result in unexpected behavior.
