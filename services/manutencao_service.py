import data_manager

MAINTENANCES_FILE = 'manutencoes.json'

def get_manutencoes_by_car_id(car_id):
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    car_maintenances = [m for m in all_maintenances if m.get('car_id') == car_id]
    return car_maintenances

def create_manutencao(descricao, data, custo, tipo, km, car_id):
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)

    last_id = all_maintenances[-1]['id'] if all_maintenances else 0
    new_id = last_id + 1

    new_maintenance = {
        'id': new_id,
        'car_id': car_id,
        'descricao': descricao,
        'data': data,
        'custo': float(custo),
        'tipo': tipo,
        'km': int(km)
    }

    all_maintenances.append(new_maintenance)
    data_manager.write_data(MAINTENANCES_FILE, all_maintenances)
    return new_maintenance

def delete_manutencao(maintenance_id):
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    original_count = len(all_maintenances)
    
    to_keep = [m for m in all_maintenances if m.get('id') != maintenance_id]

    if len(to_keep) < original_count:
        data_manager.write_data(MAINTENANCES_FILE, to_keep)
        return True
        
    return False

def get_manutencao_by_id(maintenance_id):
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    for m in all_maintenances:
        if m.get('id') == maintenance_id:
            return m
    return None

def update_manutencao(maintenance_id, descricao, data, custo, tipo, km):
    all_maintenances = data_manager.read_data(MAINTENANCES_FILE)
    maintenance_to_update = None
    
    for m in all_maintenances:
        if m.get('id') == maintenance_id:
            m['descricao'] = descricao
            m['data'] = data
            m['custo'] = float(custo)
            m['tipo'] = tipo
            m['km'] = int(km)
            maintenance_to_update = m
            break
            
    if maintenance_to_update:
        data_manager.write_data(MAINTENANCES_FILE, all_maintenances)
        
    return maintenance_to_update