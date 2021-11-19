from api import PetFriends
from settings import valid_email, valid_pswd
import os

pf = PetFriends()


def test_get_api_key_for_invalid_mail(email='', password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_invalid_pswd(email=valid_email, password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_valid_user(email=valid_email, password=valid_pswd):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)  # ключ
    # запрашиваем список питомцев -> возвращается статус и результат
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200  # проверяем код 200
    assert len(result['pets']) > 0  # проверяем, что список в json формате не равен 0


def test_post_new_pet_with_valid_data(name='Mars', animal_type='Cat', age='4', pet_photo='images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)  # ключ
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_pet_delete():
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_new_pet(auth_key, 'Vasily', 'Cat', '5', 'images/cat1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_change_pet_data(name='Nale', animal_type='Cat', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)  # ключ
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # список своих питомцев
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_data(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_change_pet_photo(pet_photo='images/cat2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)  # получили ключ
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # получили список своих питомцев
    if len(my_pets['pets']) > 0:
        status, result = pf.set_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != 0
    else:
        raise Exception("There is no my pets")


def test_successful_change_pet_name(name='Rale', animal_type='', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)  # получили ключ
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # получили список своих питомцев
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_data(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_change_pet_type(name='', animal_type='Kitty', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)  # получили ключ
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # получили список своих питомцев
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_data(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['animal_type'] == animal_type
    else:
        raise Exception("There is no my pets")


def test_successful_change_pet_age(name='', animal_type='', age='7'):
    _, auth_key = pf.get_api_key(valid_email, valid_pswd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_data(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)
        assert status == 200
        assert result['age'] == age
    else:
        raise Exception("There is no my pets")
