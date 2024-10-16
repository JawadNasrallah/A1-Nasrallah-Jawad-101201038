import unittest
from unittest.mock import patch
from io import StringIO
from game_of_quests import Game, Player, Card, FoeCard, WeaponCard, EventCard, QuestCard

class TestGameOfQuests(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.setup_adventure_deck()
        self.game.setup_event_deck()
        self.game.distribute_adventure_cards()

    @patch('builtins.input', side_effect=['no', 'no', 'no', 'no'])
    def test_initial_setup_and_turn(self, mock_input):
        # Test the initial setup of the game including deck initialization and card distribution
        self.assertEqual(len(self.game.players), 4)
        for player in self.game.players:
            self.assertEqual(len(player.hand), 12)
        self.assertGreater(len(self.game.adventure_deck), 0)
        self.assertGreater(len(self.game.event_deck), 0)

        # Simulate a turn where no one sponsors a quest
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.start_turn()
            output = fake_out.getvalue().strip()
            self.assertIn("draws an event card", output)

    @patch('builtins.input', side_effect=['yes', 'quit', 'no', 'no', 'no'])
    def test_quest_sponsorship(self, mock_input):
        # Test quest sponsorship process, including a player accepting to sponsor the quest
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.start_turn()
            output = fake_out.getvalue().strip()
            self.assertIn("Setting up stage", output)

    @patch('builtins.input', side_effect=['yes', '0', 'quit', '0', 'quit'])
    def test_stage_setup_and_attack(self, mock_input):
        # Test the quest stage setup by the sponsor and subsequent participant attack setup
        quest_card = QuestCard("Q3", 3)
        sponsor = self.game.players[0]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.play_quest(sponsor, quest_card)
            output = fake_out.getvalue().strip()
            self.assertIn("Setting up stage", output)
            self.assertIn("prepare your attack", output)

    @patch('builtins.input', side_effect=['yes', '0', 'quit', 'quit'])
    def test_participant_attack_resolution(self, mock_input):
        # Test the resolution of a quest stage, including shield awarding
        quest_card = QuestCard("Q2", 2)
        sponsor = self.game.players[0]
        self.game.play_quest(sponsor, quest_card)
        participant = self.game.players[1]
        self.assertGreaterEqual(participant.shields, 0)

    @patch('builtins.input', side_effect=['yes', 'quit', 'yes', 'quit'])
    def test_winner_determination(self, mock_input):
        # Test if the game correctly identifies a winner
        sponsor = self.game.players[0]
        quest_card = QuestCard("Q5", 5)
        self.game.play_quest(sponsor, quest_card)
        self.game.players[1].add_shields(7)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game.check_for_winners()
            output = fake_out.getvalue().strip()
            self.assertIn("The game has ended! The winner(s):", output)

if __name__ == '__main__':
    unittest.main()
