% rebase('layout', title='Manutenção Programada')

% if programada:
%   action_url = f"/programada/edit/{programada['id']}"
%   page_title = "Editar Manutenção Programada"
% else:
%   action_url = f"/car/{car['id']}/programadas/add"
%   page_title = f"Agendar Manutenção: {car['marca']} {car['modelo']}"
% end

<div class="form-page-container">
    <div class="form-card">
        <div class="form-card-header">
            <h1><i class="fas fa-calendar-plus"></i> {{page_title}}</h1>
            <p>Defina o intervalo em dias e/ou quilômetros para receber alertas automáticos antes do vencimento.</p>
        </div>

        % if not programada and presets:
        <div class="presets-box">
            <span class="presets-label"><i class="fas fa-wand-magic-sparkles"></i> Preenchimento Rápido (Clique para usar):</span>
            <div class="presets-chips">
                % for pr in presets:
                <button type="button" class="preset-chip"
                    onclick="preencherPresetProgramada('{{pr['descricao']}}', {{pr['frequencia_dias']}}, {{pr['frequencia_km']}}, {{pr['custo_estimado']}})">
                    {{pr['descricao']}} ({{pr['frequencia_km']//1000}}k km / {{pr['frequencia_dias']}}d)
                </button>
                % end
            </div>
        </div>
        % end

        <form action="{{action_url}}" method="post" class="styled-form">
            <div class="form-group">
                <label for="descricao">Descrição da Revisão / Serviço *</label>
                <input type="text" id="descricao" name="descricao" value="{{programada.get('descricao', '') if programada else ''}}" placeholder="Ex: Troca de Óleo do Motor e Filtro" required>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="ultima_data">Data da Última Realização *</label>
                    <input type="date" id="ultima_data" name="ultima_data" value="{{programada.get('ultima_data', '') if programada else hoje}}" required>
                </div>
                <div class="form-group">
                    <label for="ultimo_km">KM da Última Realização *</label>
                    <input type="number" id="ultimo_km" name="ultimo_km" value="{{programada.get('ultimo_km', '') if programada else car['km_atual']}}" min="0" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="frequencia_dias">Repetir a cada quantos dias? *</label>
                    <input type="number" id="frequencia_dias" name="frequencia_dias" value="{{programada.get('frequencia_dias', 180) if programada else 180}}" min="1" required>
                    <small class="form-hint">Ex: 180 dias (6 meses), 365 dias (1 ano)</small>
                </div>
                <div class="form-group">
                    <label for="frequencia_km">Repetir a cada quantos KM?</label>
                    <input type="number" id="frequencia_km" name="frequencia_km" value="{{programada.get('frequencia_km', 10000) if programada else 10000}}" min="0">
                    <small class="form-hint">Ex: 10000 km (use 0 se controlar apenas por data)</small>
                </div>
                <div class="form-group">
                    <label for="custo_estimado">Custo Estimado (R$)</label>
                    <input type="number" step="0.01" min="0" id="custo_estimado" name="custo_estimado" value="{{programada.get('custo_estimado', 0.0) if programada else 250.0}}">
                </div>
            </div>

            <div class="form-group">
                <label for="observacoes">Observações / Recomendações do Manual</label>
                <textarea id="observacoes" name="observacoes" rows="2" placeholder="Ex: Verificar também anel de vedação do bujão do cárter">{{programada.get('observacoes', '') if programada else ''}}</textarea>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-calendar-check"></i> Salvar Agendamento
                </button>
                <a href="/carros/{{car['id']}}?tab=programadas" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
