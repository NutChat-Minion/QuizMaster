import pytest

from quizmaster.player import Player


def test_player_creation():
    player = Player("Nut")

    assert player.name == "Nut"
    assert player.score == 0


def test_player_add_points():
    player = Player("Nut")

    player.add_points(3)
    player.add_points(2)

    assert player.score == 5


def test_player_reset_score():
    player = Player("Nut", 10)

    player.reset_score()

    assert player.score == 0


def test_empty_player_name():
    with pytest.raises(ValueError):
        Player("   ")


def test_negative_points():
    player = Player("Nut")

    with pytest.raises(ValueError):
        player.add_points(-1)