# CHance Organising System (CHAOS)
A 'virtual Event Deck', for use in wargames.

## Overview
- Each deck is user-defined, via a CSV file.
- Hidden CSV file acts a 'deck database'

## Card Layout
- Title ('Type')
- Header
- Body
- Extra

## Text Parameters (CSV)
- Card Count - based on unique Type (e.g. 'Red Flag')

## Operation
### Load CSV 'Event Deck' file.
Click on top RH icon to show File Chooser pop-up.

On Load, the current deck (hidden file) will be replaced.

### Buttons
- Footer: Back, Next navigation.
- Delete: Remove card from deck.

## CSV file format
1. Weight: number of (card) Type in deck.
   1. Could be total of 100, for percentage allocation.
2. Type: user-defined classification of card type, shown in toolbar.
3. Header: title of card etc.
4. Body: main text
5. Extra: additional information
6. Action Code: key paired to an action
   1. Shuffle
   2. Count
   3. Delete - remove card from deck



