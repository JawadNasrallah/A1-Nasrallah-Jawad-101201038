import random

class Game:
    def __init__(self):
        self.players = [Player(f"P{i}") for i in range(1, 5)]
        self.current_player_index = 0
        self.adventure_deck = []
        self.event_deck = []
        self.adventure_discard_pile = []
        self.event_discard_pile = []

    def setup_adventure_deck(self):
        # Add Foe cards
        foe_values = [(5, 8), (10, 7), (15, 8), (20, 7), (25, 7), (30, 4), (35, 4), (40, 2), (50, 2), (70, 1)]
        for value, count in foe_values:
            for _ in range(count):
                self.adventure_deck.append(FoeCard(f"F{value}", value))
        # Add Weapon cards
        weapon_values = [("Dagger", 5, 6), ("Horse", 10, 12), ("Sword", 10, 16), ("Battle-axe", 15, 8), ("Lance", 20, 6), ("Excalibur", 30, 2)]
        for name, value, count in weapon_values:
            for _ in range(count):
                self.adventure_deck.append(WeaponCard(name, value))
        random.shuffle(self.adventure_deck)

    def setup_event_deck(self):
        # Add Quest cards
        quest_counts = [(2, 3), (3, 4), (4, 3), (5, 2)]
        for stages, count in quest_counts:
            for _ in range(count):
                self.event_deck.append(QuestCard(f"Q{stages}", stages))
        # Add Event cards
        self.event_deck.append(EventCard("Plague"))
        self.event_deck.extend([EventCard("Queen's Favor")] * 2)
        self.event_deck.extend([EventCard("Prosperity")] * 2)
        random.shuffle(self.event_deck)

    def distribute_adventure_cards(self):
        for player in self.players:
            for _ in range(12):
                player.add_card(self.adventure_deck.pop(0))

    def start_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"It's {current_player.name}'s turn.")
        self.draw_event_card(current_player)

    def draw_event_card(self, player):
        if not self.event_deck:
            self.event_deck = self.event_discard_pile[:]
            self.event_discard_pile.clear()
            random.shuffle(self.event_deck)
        card = self.event_deck.pop(0)
        print(f"{player.name} draws an event card: {card.name}")
        self.process_event_card(card, player)
        self.event_discard_pile.append(card)

    def process_event_card(self, card, player):
        if card.name == "Plague":
            player.reduce_shields(2)
            print(f"{player.name} loses 2 shields. Current shields: {player.shields}")
        elif card.name == "Queen's Favor":
            player.add_card(self.adventure_deck.pop(0))
            player.add_card(self.adventure_deck.pop(0))
            print(f"{player.name} draws 2 adventure cards.")
        elif card.name == "Prosperity":
            for p in self.players:
                p.add_card(self.adventure_deck.pop(0))
                p.add_card(self.adventure_deck.pop(0))
                print(f"{p.name} draws 2 adventure cards.")
        elif isinstance(card, QuestCard):
            self.handle_quest_card(card, player)

    def handle_quest_card(self, quest_card, player):
        sponsor = self.find_sponsor(quest_card)
        if sponsor:
            self.play_quest(sponsor, quest_card)
        else:
            print(f"No one chose to sponsor the quest {quest_card.name}. It is discarded.")

    def find_sponsor(self, quest_card):
        for i in range(len(self.players)):
            current_index = (self.current_player_index + i) % len(self.players)
            player = self.players[current_index]
            response = input(f"{player.name}, would you like to sponsor the quest {quest_card.name}? (yes/no): ")
            if response.lower() == "yes":
                return player
        return None

    def play_quest(self, sponsor, quest_card):
        stages = []
        for stage_num in range(quest_card.stages):
            print(f"Setting up stage {stage_num + 1} of {quest_card.stages}.")
            stage = self.setup_stage(sponsor)
            if stage:
                stages.append(stage)
            else:
                print("Invalid stage setup. Quest sponsorship canceled.")
                return
        participants = [p for p in self.players if p != sponsor]
        for stage in stages:
            participants = self.resolve_stage(stage, participants)
            if not participants:
                print("All participants have failed. The quest ends with no winners.")
                return
        for participant in participants:
            participant.add_shields(quest_card.stages)
            print(f"{participant.name} has completed the quest and earned {quest_card.stages} shields.")

    def setup_stage(self, sponsor):
        stage = []
        while True:
            print(f"{sponsor.name}, set up your stage. Your hand: {sponsor.display_hand()}")
            card_index = input("Enter the index of the card to add to the stage or 'quit' to finish: ")
            if card_index.lower() == 'quit':
                if not stage:
                    print("A stage cannot be empty.")
                    continue
                if len([card for card in stage if isinstance(card, FoeCard)]) != 1:
                    print("A stage must contain exactly one Foe card.")
                    continue
                return stage
            try:
                card_index = int(card_index)
                card = sponsor.hand[card_index]
                stage.append(card)
                sponsor.hand.remove(card)
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

    def resolve_stage(self, stage, participants):
        stage_value = sum(card.value for card in stage)
        print(f"Resolving stage with value {stage_value}.")
        remaining_participants = []
        for participant in participants:
            attack_value = participant.prepare_attack()
            if attack_value >= stage_value:
                remaining_participants.append(participant)
                print(f"{participant.name} successfully completed the stage with an attack value of {attack_value}.")
            else:
                print(f"{participant.name} failed to complete the stage with an attack value of {attack_value}.")
        return remaining_participants

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_game(self):
        self.setup_adventure_deck()
        self.setup_event_deck()
        self.distribute_adventure_cards()
        while True:
            self.start_turn()
            self.end_turn()
            if self.check_for_winners():
                break

    def check_for_winners(self):
        winners = [player for player in self.players if player.shields >= 7]
        if winners:
            print("The game has ended! The winner(s):")
            for winner in winners:
                print(f"- {winner.name}")
            return True
        return False

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.shields = 0

    def add_card(self, card):
        if len(self.hand) < 12:
            self.hand.append(card)
        else:
            print(f"{self.name} cannot hold more than 12 cards.")

    def reduce_shields(self, count):
        self.shields = max(0, self.shields - count)

    def add_shields(self, count):
        self.shields += count

    def prepare_attack(self):
        print(f"{self.name}, prepare your attack. Your hand: {self.display_hand()}")
        attack_value = 0
        used_cards = []
        while True:
            card_index = input("Enter the index of the card to add to the attack or 'quit' to finish: ")
            if card_index.lower() == 'quit':
                break
            try:
                card_index = int(card_index)
                card = self.hand[card_index]
                if isinstance(card, WeaponCard) and card not in used_cards:
                    attack_value += card.value
                    used_cards.append(card)
                else:
                    print("Only weapon cards can be used for an attack, and each card can be used only once.")
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
        for card in used_cards:
            self.hand.remove(card)
        return attack_value

    def display_hand(self):
        foes = [card for card in self.hand if isinstance(card, FoeCard)]
        weapons = [card for card in self.hand if isinstance(card, WeaponCard)]
        foes.sort(key=lambda x: x.value)
        weapons.sort(key=lambda x: (x.value, x.name))
        return " | ".join([f"{card.name} ({card.value})" for card in foes + weapons])

class Card:
    def __init__(self, name):
        self.name = name

class FoeCard(Card):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

class WeaponCard(Card):
    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

class EventCard(Card):
    pass

class QuestCard(Card):
    def __init__(self, name, stages):
        super().__init__(name)
        self.stages = stages


if __name__ == "__main__":
    game = Game()
    game.play_game()
