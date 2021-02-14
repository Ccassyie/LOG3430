from crud import CRUD
import unittest
from unittest.mock import patch


class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596855166.0,
                "Date_of_last_seen_message": 1596855166.0,
                "Groups": ["default"],
            },
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass


    @patch("crud.CRUD.read_users_file")    
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        mock_modify_users_file.return_value= True

        crud=CRUD()
        email="test@email.com"
        date="2003-09-13"

        crud.add_new_user(email,date)
        mock_modify_users_file.assert_called_once_with(self.users_data)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Returns_false_to_invalid_email_to_modify_users_file(
            self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        crud=CRUD()
        email="test"
        date="2003-09-13"

        self.assertFalse(crud.add_new_user(email,date))


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data


        crud=CRUD()

        name="roommates"
        Trust=100
        List_of_members= []


        crud.add_new_group(name,Trust, List_of_members)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)


    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        mock_read_users_file.return_value=self.users_data
        user_id="3"
        field="Trust"


        crud=CRUD()
        self.assertEqual(crud.get_user_data(user_id,field),False)


    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        mock_read_users_file.return_value=self.users_data
        user_id=3
        field="Test"

        crud=CRUD()
        self.assertEqual(crud.get_user_data(user_id,field),False)


    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        crud=CRUD()
        user_id="2"
        field="SpamN"
        self.assertEqual(crud.get_user_data(user_id,field),171)


    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        group_id="3"
        field="Trust"
        self.assertEqual(crud.get_groups_data(group_id,field),False)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        group_id="2"
        field="Test"
        self.assertEqual(crud.get_groups_data(group_id,field),False)


    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        group_id="2"
        field="Trust"
        self.assertEqual(crud.get_groups_data(group_id,field),90)



    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        crud=CRUD()
        name="test@gmail.com"
        self.assertEqual(crud.get_user_id(name), False)


    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        mock_read_users_file.return_value=self.users_data
        crud=CRUD()
        name="mark@mail.com"
        self.assertEqual(crud.get_user_id(name),"2")


    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
        self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        name="Test"
        self.assertEqual(crud.get_group_id(name),False)

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):
        mock_read_groups_file.return_value=self.groups_data
        crud=CRUD()
        name="friends"
        self.assertEqual(crud.get_group_id(name),"2")


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        mock_modify_users_file.return_value= True
        crud=CRUD()
        user_id="3"
        field="Trust"
        self.assertEqual(crud.update_users(user_id,field,60), False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Returns_false_for_invalid_field(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        mock_modify_users_file.return_value= True
        crud=CRUD()
        user_id="2"
        field="Test"
        self.assertEqual(crud.update_users(user_id,field,60), False)


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        mock_modify_users_file.return_value=True

        crud=CRUD()
        user_id="1"
        field="SpamN"
        data=80

        crud.update_users(user_id,field,data)
        mock_modify_users_file.assert_called_once_with(self.users_data)


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value=self.groups_data
        mock_modify_groups_file.return_value=True

        crud=CRUD()
        group_id="3"
        field="name"
        data="Test"

        self.assertEqual(crud.update_groups(group_id,field,data),False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value=self.groups_data
        mock_modify_groups_file.return_value=True

        crud=CRUD()
        group_id="1"
        field="Test"
        data=80

        self.assertEqual(crud.update_groups(group_id,field,data),False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value=self.groups_data
        mock_modify_groups_file.return_value=True

        crud=CRUD()
        group_id="1"
        field="Trust"
        data=60

        crud.update_groups(group_id,field,data)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value=self.users_data
        mock_modify_users_file.return_value=True

        crud=CRUD()
        user_id="3"

        self.assertEqual(crud.remove_user(user_id),False)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):

        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True

        crud=CRUD()
        user_id="2"

        crud.remove_user(user_id)
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True

        crud = CRUD()
        user_id ="3"
        group_name = "default"

        self.assertEqual(crud.remove_user_group(user_id, group_name),False);


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")    
    def test_remove_user_group_Returns_false_for_invalid_group(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        user_id ="1"
        group_name = "Test"

        self.assertFalse(crud.remove_user_group(user_id, group_name));

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True

        crud=CRUD()
        user_id="2"
        group_name="default"

        crud.remove_user_group(user_id,group_name)
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value=True

        crud = CRUD()
        group_id ="4"

        self.assertFalse(crud.remove_group(group_id));

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True

        crud=CRUD()
        group_id="2"

        crud.remove_group(group_id)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_read_groups_file, mock_modify_groups_file
    ):

        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value=True

        crud = CRUD()
        group_id ="4"
        member="alex@gmail.com"

        self.assertFalse(crud.remove_group_member(group_id,member));

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value=True

        crud = CRUD()
        group_id ="2"
        member="Test@gmail.com"

        self.assertFalse(crud.remove_group_member(group_id,member));

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")    
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True

        crud=CRUD()
        group_id="2"
        member="alex@gmail.com"

        crud.remove_group_member(group_id,member)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)


    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_value_of_Trust_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud=CRUD()
        user_id="2"
        field="Trust"
        data=60

        crud.update_users(user_id,field,data)
        mock_modify_users_file.assert_called_once_with(self.users_data)
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_value_of_name_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
):
        mock_read_users_file.return_value = self.users_data

        crud=CRUD()
        user_id="2"
        field="name"
        data="Test@gmail.com"

        crud.update_users(user_id,field,data)
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_value_of_groups_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
):
        mock_read_users_file.return_value = self.users_data

        crud=CRUD()
        user_id="2"
        field="Groups"
        data=[]

        crud.update_users(user_id,field,data)
        mock_modify_users_file.assert_called_once_with(self.users_data)



    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_value_of_date_first_seen_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud=CRUD()
        user_id="1"
        field="Date_of_first_seen_message"
        data="2000-09-01"

        crud.update_users(user_id,field,data)
        mock_modify_users_file.assert_called_once_with(self.users_data)

    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_value_of_date_last_seen_to_modify_users_file(
        self, mock_read_users_file, mock_modify_users_file
):
        mock_read_users_file.return_value = self.users_data

        crud=CRUD()
        user_id="2"
        field="Date_of_last_seen_message"
        data="2022-09-01"

        crud.update_users(user_id,field,data)
        mock_modify_users_file.assert_called_once_with(self.users_data)


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_value_to_modify_groups_file(
    self, mock_read_groups_file, mock_modify_groups_file
):
        mock_read_groups_file.return_value = self.groups_data

        crud=CRUD()
        group_id=2
        field="Trust"
        data=60

        crud.update_groups(group_id,field,data)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_value_of_name_to_modify_users_file(
        self, mock_read_groups_file, mock_modify_groups_file
):
        mock_read_groups_file.return_value = self.groups_data

        crud=CRUD()
        group_id=2
        field="name"
        data="Test"

        crud.update_groups(group_id,field,data)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_value_of_list_of_members_to_modify_users_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud=CRUD()
        group_id=2
        field="List_of_members"
        data=[]

        crud.update_groups(group_id,field,data)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)









#if __name__ == "__main__":

    #unittest.main()
