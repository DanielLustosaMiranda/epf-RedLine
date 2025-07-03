from models.carro import CarroModel
from models.carro import Carro
from models.manutecao import Manutencao
from models.manutecao import ManutencaoModel
from models.user import UserModel
from models.user import User

user_model = UserModel()
carro_model = CarroModel()
manut_model = ManutencaoModel()

user = User(1, "Daniel", "dani1234@gmail.com", "18/01/18")
user2 = User(2, "João", "joao@gmai.com", "10/10/10")

user_model.add_user(user)
user_model.add_user(user2)

carro = Carro(1 , "Fiat", "Uno", 2010, "ABC1234", 120000)
carro_model.add_carro(carro)

manut1 = Manutencao("Troca de óleo", "2025-07-03", 250.0, "Preventiva", "ABC1234")
manut_model.add_manutencao(manut1)

manut2 = Manutencao("Revisão dos freios", "2025-07-10", 400.0, "Corretiva", "ABC1234")
manut_model.add_manutencao(manut2)

manutencoes = manut_model.get_by_veiculo("ABC1234")
print("Manutenções encontradas:")
for m in manutencoes:
    print(m.detalhar_servico())
