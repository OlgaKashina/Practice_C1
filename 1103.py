class Client:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def data_client(self):
        return f'Клиент «{self.name}». Баланс: {self.balance} руб.'

client_1 = Client("Иван Петров", 50)
client_2 = Client("Максим Сидоров", 100)
client_3 = Client("Андрей Кумаров", 77)

clients = [client_1, client_2, client_3]
for client in clients:
    print(client.data_client())
