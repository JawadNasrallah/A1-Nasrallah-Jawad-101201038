# Game of Quests - Assignment 1

## Responsibilities Table

| Responsibility ID | Description                                                                          | Use Case Steps    |
| ----------------- | ------------------------------------------------------------------------------------ | ----------------- |
| RESP-1            | Game sets up adventure and event decks                                               | UC-01-1           |
| RESP-2            | Game distributes 12 cards from the adventure deck to each player, updating the deck  | UC-01-2           |
| RESP-3            | Game determines if one or more players have 7 shields at the end of a turn           | UC-01-3, UC-02-5a |
| RESP-4            | Game displays the ID of each winner and then terminates                              | UC-01-4           |
| RESP-5            | Player draws an event card and the game processes the event                          | UC-02-2a          |
| RESP-6            | Player sponsors a quest and sets up stages                                           | UC-04-3, UC-05    |
| RESP-7            | Game prompts participants to decide on joining the quest                             | UC-04-4.2         |
| RESP-8            | Game resolves each stage of the quest and determines participants for the next stage | UC-04-4.6         |
| RESP-9            | Player sets up an attack against the current stage                                   | UC-06             |


## Correction Grid

| Correction Criteria                        | Completed (Yes/No) | Comments                                            |
| ------------------------------------------ | ------------------ | --------------------------------------------------- |
| Adventure and event decks set up           | Yes                | Decks correctly initialized with required cards     |
| Distribution of adventure cards to players | Yes                | Each player receives 12 adventure cards             |
| Drawing and processing event cards         | Yes                | Event cards correctly affect players                |
| Quest sponsorship and stage setup          | Yes                | Players can sponsor and set up stages               |
| Participant decision and attack setup      | Yes                | Participants can join and prepare attacks           |
| Quest resolution and shield awarding       | Yes                | Shields awarded correctly based on quest completion |
| Winner determination                       | Yes                | Game ends when a player reaches 7 shields           |

## How to Run the Game

1. Save the provided code into a Python file named `game_of_quests.py`.
2. Run the script using Python:
   ```sh
   python game_of_quests.py
   ```
3. Follow the prompts in the terminal to play the game.

## Game Flow

- The game starts with 4 players, each receiving 12 adventure cards.
- Players take turns drawing event cards from the event deck. Event cards may cause various effects, such as losing shields or drawing additional cards.
- When a quest card is drawn, players are prompted to sponsor the quest. The sponsor sets up stages using Foe and Weapon cards.
- Other players can choose to participate in the quest and must prepare attacks for each stage.
- Participants that successfully complete all stages earn shields equal to the number of stages in the quest.
- The game ends when one or more players accumulate 7 shields, and the winner(s) are announced.

## Testing

- run game_of_quests_test.py

