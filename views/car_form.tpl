% rebase('layout', title='Editar Veículo' if car else 'Novo Veículo')

<div class="form-page-container">
    <div class="form-card">
        <div class="form-card-header">
            <h1>
                <i class="fas fa-car"></i>
                {{f"Editar Veículo: {car['marca']} {car['modelo']}" if car else "Cadastrar Novo Veículo"}}
            </h1>
            <p>Preencha as informações do veículo para controle completo de manutenções e peças.</p>
        </div>

        <form action="{{action_url}}" method="post" class="styled-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="marca">Marca *</label>
                    <input type="text" id="marca" name="marca" value="{{car['marca'] if car else ''}}" placeholder="Ex: Honda, Volkswagen, Toyota" required>
                </div>
                <div class="form-group">
                    <label for="modelo">Modelo / Versão *</label>
                    <input type="text" id="modelo" name="modelo" value="{{car['modelo'] if car else ''}}" placeholder="Ex: Civic Touring 1.5 Turbo" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="ano">Ano *</label>
                    <input type="number" id="ano" name="ano" value="{{car['ano'] if car else '2024'}}" min="1950" max="2030" required>
                </div>
                <div class="form-group">
                    <label for="placa">Placa *</label>
                    <input type="text" id="placa" name="placa" value="{{car['placa'] if car else ''}}" placeholder="ABC-1D23" maxlength="10" required>
                </div>
                <div class="form-group">
                    <label for="km_atual">Quilometragem Atual (km) *</label>
                    <input type="number" id="km_atual" name="km_atual" value="{{car['km_atual'] if car else '0'}}" min="0" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="combustivel">Combustível</label>
                    <select id="combustivel" name="combustivel">
                        % for tc in tipos_combustivel:
                            <option value="{{tc}}" {{'selected' if car and car.get('combustivel') == tc else ''}}>{{tc}}</option>
                        % end
                    </select>
                </div>
                <div class="form-group">
                    <label for="cor">Cor</label>
                    <input type="text" id="cor" name="cor" value="{{car.get('cor', '') if car else ''}}" placeholder="Ex: Prata, Preto, Branco">
                </div>
                <div class="form-group">
                    <label for="apelido">Apelido (Opcional)</label>
                    <input type="text" id="apelido" name="apelido" value="{{car.get('apelido', '') if car else ''}}" placeholder="Ex: Carro de Viagem">
                </div>
            </div>

            <div class="form-group">
                <label for="observacoes">Observações / Especificações Técnicas (ex: viscosidade do óleo, calibragem)</label>
                <textarea id="observacoes" name="observacoes" rows="3" placeholder="Ex: Usar óleo sintético 5W30 API SP; Pneus 32 PSI">{{car.get('observacoes', '') if car else ''}}</textarea>
            </div>

            % if not car:
            <div class="checkbox-card">
                <label class="checkbox-label">
                    <input type="checkbox" name="criar_kit_padrao" checked>
                    <span>
                        <strong>Gerar automaticamente o Kit Essencial de Vida Útil (Recomendado)</strong>
                        <small>Cria automaticamente o monitoramento de Óleo, Filtros, Pastilhas de Freio, Pneus, Bateria, Correia e Velas.</small>
                    </span>
                </label>
            </div>
            % end

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-floppy-disk"></i> Salvar Veículo
                </button>
                % cancel_url = f"/carros/{car['id']}" if car else "/carros"
                <a href="{{cancel_url}}" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
