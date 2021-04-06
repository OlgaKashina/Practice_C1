class Client:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def get_name(self):
        return self.name

    def get_balance(self):
        return self.balance


class Guest(Client):
    def __init__(self, name, city, status):
        self.name = name
        self.city = city
        self.status = status

    def get_status(self):
        return self.status

    def get_city(self):
        return self.city


list_volunteer = [
    {'Имя': 'Иван Петров', 'Город': 'Москва', 'Статус': 'Наставник'},
    {'Имя': 'Маргарита Сидорова', 'Город': 'Санкт-Петербург', 'Статус': 'Врач'},
    {'Имя': 'Анна Иванова', 'Город': 'Астрахань', 'Статус': 'Профессор'},
           ]

corporate_guests = [Guest(d['Имя'], d['Город'], d['Статус']) for d in list_volunteer]
for guest in corporate_guests:
    print(f'"{guest.get_name()}", г.{guest.get_city()}, статус "{guest.get_status()}"')
