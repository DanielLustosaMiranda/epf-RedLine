from services import (
    car_service,
    manutencao_service,
    programada_service,
    vida_util_service,
    abastecimento_service,
)


def enriquecer_carro(car: dict) -> dict:
    """Adiciona indicadores de saúde, custos, alertas e contadores a um dicionário de veículo."""
    car_id = car['id']
    km_atual = car['km_atual']

    manutencoes = manutencao_service.get_manutencoes_by_car_id(car_id)
    programadas = programada_service.get_programadas_by_car_id(car_id, km_atual)
    itens_vida = vida_util_service.get_itens_by_car_id(car_id, km_atual)
    combustivel_stats = abastecimento_service.calcular_estatisticas_combustivel(car_id)

    custo_manutencoes = round(sum(m['custo'] for m in manutencoes), 2)
    custo_combustivel = combustivel_stats['total_gasto']
    custo_total = round(custo_manutencoes + custo_combustivel, 2)

    atrasadas = [p for p in programadas if p['status'] == 'atrasada']
    proximas = [p for p in programadas if p['status'] == 'proxima']
    criticos = [i for i in itens_vida if i['status'] == 'critico']
    atencao = [i for i in itens_vida if i['status'] == 'atencao']

    # Cálculo do índice de saúde do veículo (0 a 100)
    if itens_vida:
        media_pecas = sum(i['saude_percentual'] for i in itens_vida) / len(itens_vida)
    else:
        media_pecas = 100.0

    penalidade_programadas = (len(atrasadas) * 18) + (len(proximas) * 6)
    saude = int(round(max(5, min(100, media_pecas - penalidade_programadas))))

    if saude >= 75:
        saude_cor = "success"
        saude_label = "Excelente"
    elif saude >= 45:
        saude_cor = "warning"
        saude_label = "Atenção"
    else:
        saude_cor = "danger"
        saude_label = "Crítico"

    ultima_manutencao = manutencoes[0] if manutencoes else None

    return {
        **car,
        'saude': saude,
        'saude_cor': saude_cor,
        'saude_label': saude_label,
        'qtd_manutencoes': len(manutencoes),
        'qtd_programadas': len(programadas),
        'qtd_itens_vida': len(itens_vida),
        'custo_manutencoes': custo_manutencoes,
        'custo_combustivel': custo_combustivel,
        'custo_total': custo_total,
        'consumo_medio_kml': combustivel_stats['consumo_medio_kml'],
        'alertas_criticos': len(atrasadas) + len(criticos),
        'alertas_aviso': len(proximas) + len(atencao),
        'ultima_manutencao': ultima_manutencao,
        'programadas': programadas,
        'itens_vida': itens_vida,
        'manutencoes': manutencoes,
    }


def obter_dados_dashboard(user_id: int) -> dict:
    """Agrega todos os indicadores da garagem do usuário para o Dashboard e Relatórios."""
    raw_cars = car_service.get_cars_by_user_id(user_id)
    cars = [enriquecer_carro(c) for c in raw_cars]

    total_carros = len(cars)
    total_manutencoes = sum(c['qtd_manutencoes'] for c in cars)
    custo_total_manutencoes = round(sum(c['custo_manutencoes'] for c in cars), 2)
    custo_total_combustivel = round(sum(c['custo_combustivel'] for c in cars), 2)
    custo_geral = round(custo_total_manutencoes + custo_total_combustivel, 2)
    saude_media = int(round(sum(c['saude'] for c in cars) / total_carros)) if total_carros > 0 else 100

    # Central de Alertas (Programadas atrasadas/próximas + Peças críticas/atenção)
    alertas = []
    for c in cars:
        nome_carro = f"{c['marca']} {c['modelo']} ({c['placa']})"
        for p in c['programadas']:
            if p['status'] in ('atrasada', 'proxima'):
                alertas.append({
                    'tipo_origem': 'programada',
                    'nivel': 'danger' if p['status'] == 'atrasada' else 'warning',
                    'titulo': p['descricao'],
                    'subtitulo': nome_carro,
                    'detalhe': p['resumo_status'],
                    'car_id': c['id'],
                    'item_id': p['id'],
                    'acao_url': f"/programada/concluir/{p['id']}",
                    'acao_label': "Concluir",
                })
        for iv in c['itens_vida']:
            if iv['status'] in ('critico', 'atencao'):
                alertas.append({
                    'tipo_origem': 'vida_util',
                    'nivel': 'danger' if iv['status'] == 'critico' else 'warning',
                    'titulo': f"Peça: {iv['nome_item']} ({iv['saude_percentual']}% vida útil)",
                    'subtitulo': nome_carro,
                    'detalhe': iv['status_label'],
                    'car_id': c['id'],
                    'item_id': iv['id'],
                    'acao_url': f"/vida-util/renovar/{iv['id']}",
                    'acao_label': "Substituir",
                })

    # Ordena alertas: danger primeiro
    alertas.sort(key=lambda a: 0 if a['nivel'] == 'danger' else 1)

    todas_manutencoes = manutencao_service.get_manutencoes_by_user(user_id)

    # Gastos por tipo de manutenção
    gastos_por_tipo = {}
    for m in todas_manutencoes:
        t = m['tipo'] or 'Outros'
        gastos_por_tipo[t] = round(gastos_por_tipo.get(t, 0.0) + m['custo'], 2)

    distribuicao_tipos = []
    for t, valor in sorted(gastos_por_tipo.items(), key=lambda x: x[1], reverse=True):
        pct = int(round((valor / custo_total_manutencoes) * 100)) if custo_total_manutencoes > 0 else 0
        distribuicao_tipos.append({'tipo': t, 'valor': valor, 'percentual': pct})

    return {
        'cars': cars,
        'total_carros': total_carros,
        'total_manutencoes': total_manutencoes,
        'custo_total_manutencoes': custo_total_manutencoes,
        'custo_total_combustivel': custo_total_combustivel,
        'custo_geral': custo_geral,
        'saude_media': saude_media,
        'alertas': alertas,
        'ultimas_manutencoes': todas_manutencoes[:6],
        'todas_manutencoes': todas_manutencoes,
        'distribuicao_tipos': distribuicao_tipos,
    }
