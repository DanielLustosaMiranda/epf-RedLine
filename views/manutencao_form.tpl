% rebase('layout', title='Editar Manutenção' if manutencao else 'Nova Manutenção')

% if manutencao:
%   action_url = f"/manutencao/edit/{manutencao['id']}"
%   page_title = "Editar Registro de Manutenção"
% else:
%   action_url = f"/car/{car['id']}/manutencoes/add"
%   page_title = f"Registrar Manutenção: {car['marca']} {car['modelo']} ({car['placa']})"
% end

<div class="form-page-container">
    <div class="form-card">
        <div class="form-card-header">
            <h1><i class="fas fa-screwdriver-wrench"></i> {{page_title}}</h1>
            <p>Se a quilometragem informada for maior que a atual do veículo ({{format_km(car['km_atual'])}}), o hodômetro será atualizado automaticamente.</p>
        </div>

        <form action="{{action_url}}" method="post" class="styled-form">
            <div class="form-group">
                <label for="descricao">Descrição do Serviço / Peças Trocadas *</label>
                <input type="text" id="descricao" name="descricao" value="{{manutencao.get('descricao', '') if manutencao else ''}}" placeholder="Ex: Troca de óleo sintético 5W30, filtro de óleo e filtro de ar" required>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="data">Data do Serviço *</label>
                    <input type="date" id="data" name="data" value="{{manutencao.get('data', '') if manutencao else hoje}}" required>
                </div>
                <div class="form-group">
                    <label for="km">Quilometragem no Momento (km) *</label>
                    <input type="number" id="km" name="km" value="{{manutencao.get('km', '') if manutencao else car['km_atual']}}" min="0" required>
                </div>
                <div class="form-group">
                    <label for="custo">Custo Total (R$) *</label>
                    <input type="number" step="0.01" min="0" id="custo" name="custo" value="{{manutencao.get('custo', '') if manutencao else ''}}" placeholder="0.00" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="tipo">Categoria de Manutenção *</label>
                    <select id="tipo" name="tipo">
                        % for tm in tipos_manutencao:
                            <option value="{{tm}}" {{'selected' if manutencao and manutencao.get('tipo') == tm else ''}}>{{tm}}</option>
                        % end
                    </select>
                </div>
                <div class="form-group">
                    <label for="oficina">Oficina / Prestador</label>
                    <input type="text" id="oficina" name="oficina" value="{{manutencao.get('oficina', '') if manutencao else ''}}" placeholder="Ex: Oficina Bosch Service / Concessionária">
                </div>
                <div class="form-group">
                    <label for="garantia_meses">Garantia (Meses)</label>
                    <input type="number" id="garantia_meses" name="garantia_meses" value="{{manutencao.get('garantia_meses', 0) if manutencao else 6}}" min="0" max="120">
                </div>
            </div>

            <div class="form-group">
                <label for="observacoes">Observações / Código das Peças / Nota Fiscal</label>
                <textarea id="observacoes" name="observacoes" rows="3" placeholder="Detalhes adicionais, marca das peças utilizadas ou número da OS">{{manutencao.get('observacoes', '') if manutencao else ''}}</textarea>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-floppy-disk"></i> Salvar Manutenção
                </button>
                <a href="/carros/{{car['id']}}?tab=historico" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
