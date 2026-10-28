% rebase('layout', title='Item de Vida Útil')

% if item:
%   action_url = f"/vida-util/edit/{item['id']}"
%   page_title = "Editar Componente Monitorado"
% else:
%   action_url = f"/car/{car['id']}/vida-util/add"
%   page_title = f"Monitorar Peça: {car['marca']} {car['modelo']}"
% end

<div class="form-page-container">
    <div class="form-card">
        <div class="form-card-header">
            <h1><i class="fas fa-microchip"></i> {{page_title}}</h1>
            <p>O sistema calcula automaticamente o percentual de vida útil restante combinando o tempo de uso e a quilometragem rodada.</p>
        </div>

        % if not item and sugestoes:
        <div class="presets-box">
            <span class="presets-label"><i class="fas fa-wand-magic-sparkles"></i> Peças Comuns (Clique para preencher):</span>
            <div class="presets-chips">
                % for s in sugestoes:
                <button type="button" class="preset-chip"
                    onclick="preencherPresetVidaUtil('{{s['nome_item']}}', {{s['validade_anos']}}, {{s['validade_km']}})">
                    {{s['nome_item']}} ({{s['validade_anos']}}a / {{s['validade_km']//1000}}k km)
                </button>
                % end
            </div>
        </div>
        % end

        <form action="{{action_url}}" method="post" class="styled-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="nome_item">Nome do Componente / Peça *</label>
                    <input type="text" id="nome_item" name="nome_item" value="{{item.get('nome_item', '') if item else ''}}" placeholder="Ex: Bateria 60Ah, Pastilhas Dianteiras, Jogo de Pneus" required>
                </div>
                <div class="form-group">
                    <label for="marca_peca">Marca / Especificação da Peça</label>
                    <input type="text" id="marca_peca" name="marca_peca" value="{{item.get('marca_peca', '') if item else ''}}" placeholder="Ex: Moura, Michelin, Bosch, Motul">
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="data_instalacao">Data de Instalação *</label>
                    <input type="date" id="data_instalacao" name="data_instalacao" value="{{item.get('data_instalacao', '') if item else hoje}}" required>
                </div>
                <div class="form-group">
                    <label for="km_instalacao">KM na Instalação *</label>
                    <input type="number" id="km_instalacao" name="km_instalacao" value="{{item.get('km_instalacao', '') if item else car['km_atual']}}" min="0" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="validade_anos">Durabilidade Estimada (Anos) *</label>
                    <input type="number" step="0.1" min="0.1" max="20" id="validade_anos" name="validade_anos" value="{{item.get('validade_anos', 1.0) if item else 1.0}}" required>
                    <small class="form-hint">Ex: 0.5 (6 meses), 1.0 (1 ano), 3.0 (3 anos)</small>
                </div>
                <div class="form-group">
                    <label for="validade_km">Durabilidade Estimada (KM) *</label>
                    <input type="number" min="0" id="validade_km" name="validade_km" value="{{item.get('validade_km', 10000) if item else 10000}}" required>
                    <small class="form-hint">Ex: 10000 km para óleo, 50000 km para pneus</small>
                </div>
            </div>

            <div class="form-group">
                <label for="observacoes">Observações</label>
                <textarea id="observacoes" name="observacoes" rows="2" placeholder="Informações sobre garantia da peça ou medidas">{{item.get('observacoes', '') if item else ''}}</textarea>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-floppy-disk"></i> Salvar Componente
                </button>
                <a href="/carros/{{car['id']}}?tab=vida-util" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
