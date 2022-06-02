# MDCards
Python/Kivy Event Card app (CHAOS)

## Overview
A 'virtual Event Deck', for use in wargames.

Each deck is user-defined, via a CSV file.

## Operation
### Load CSV 'Event Deck' file.
Click on top RH icon to show File Chooser pop-up.

On Load, the current deck will be replaced.


## CSV file format
1. Weight: number of (card) Type in deck.
   1. Could be total of 100, for percentage allocation.
2. Type: user-defined classification of card type, shown in toolbar.
3. Header: title of card etc.
4. Body: main text
5. Extra: additional information
6. Action Code: key paired to an action - shuffle(), for example.


