import data_manager

CARS_FILE = 'carros.json'

def get_cars_by_user_id(user_id):
    all_cars = data_manager.read_data(CARS_FILE)
    user_cars = [car for car in all_cars if car.get('user_id') == user_id]
    return user_cars

def get_car_by_id(car_id):
    all_cars = data_manager.read_data(CARS_FILE)
    for car in all_cars:
        if car.get('id') == car_id:
            return car
    return None

def create_car(marca, modelo, ano, placa, km_atual, user_id):
    all_cars = data_manager.read_data(CARS_FILE)

    last_id = all_cars[-1]['id'] if all_cars else 0
    new_id = last_id + 1

    new_car = {
        'id': new_id,
        'user_id': user_id,
        'marca': marca,
        'modelo': modelo,
        'ano': int(ano),
        'placa': placa.upper(),
        'km_atual': int(km_atual)
    }

    all_cars.append(new_car)
    data_manager.write_data(CARS_FILE, all_cars)
    return new_car

def update_car(car_id, marca, modelo, ano, placa, km_atual):
    all_cars = data_manager.read_data(CARS_FILE)
    car_to_update = None
    
    for car in all_cars:
        if car.get('id') == car_id:
            car['marca'] = marca
            car['modelo'] = modelo
            car['ano'] = int(ano)
            car['placa'] = placa.upper()
            car['km_atual'] = int(km_atual)
            car_to_update = car
            break

    if car_to_update:
        data_manager.write_data(CARS_FILE, all_cars)

    return car_to_update

def delete_car(car_id):
    all_cars = data_manager.read_data(CARS_FILE)
    original_count = len(all_cars)
    cars_to_keep = [car for car in all_cars if car.get('id') != car_id]

    if len(cars_to_keep) < original_count:
        data_manager.write_data(CARS_FILE, cars_to_keep)
        return True
        
    return False