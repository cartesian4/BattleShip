import pytest
from BattleshipsFolder import *

# def test_get_username_with_empty_input():
#     with pytest.raises(StopIteration):
#         def mock_input(s): return ""
#         __builtins__['input'] = mock_input
#         assert get_username() == "Alice"

def test_get_username_with_valid_input():
    def mock_input(s): return "Bob"
    __builtins__['input'] = mock_input
    assert get_username() == "Bob" 

def test_get_mapsize_when_user_enters_valid_input():
    def mock_input(s): return "10"
    __builtins__['input'] = mock_input
    assert int(input("\nChoose a map size between 5 and 100: ")) == 10

def test_get_mapsize_when_user_enters_invalid_input():
    def mock_input(s): return "abc"
    __builtins__['input'] = mock_input
    with pytest.raises(ValueError):
        int(input("\nChoose a map size between 5 and 100: "))

def test_pick_battleship_placement_off_grid():
    # It will tell you the spot is invalid
    assert(False)

def test_pick_battleshsip_placement_already_occupied():
    # It will tell the user that the spot is occupied
    assert(False)


