from unittest.mock import patch, MagicMock
from services.user_service import UserService

@patch('services.user_service.UserRepository')
def test_list_users_returns_users(mock_repo):
    fake_user1 = MagicMock(login="younes")
    fake_user2 = MagicMock(login="admin")

    # mock get_all
    mock_repo.get_all.return_value = [fake_user1, fake_user2]

    users = UserService.list_users()

    assert len(users) == 2
    assert users[0].login == "younes"
    assert users[1].login == "admin"
    
    mock_repo.get_all.assert_called_once()
