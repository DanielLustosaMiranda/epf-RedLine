% rebase('layout', title='Registrar Abastecimento')

<div class="form-page-container">
    <div class="form-card">
        <div class="form-card-header">
            <h1><i class="fas fa-gas-pump"></i> Registrar Abastecimento: {{car['marca']}} {{car['modelo']}}</h1>
            <p>Registre seus abastecimentos para calcular o consumo médio (km/L) e acompanhar os gastos com combustível.</p>
        </div>

        <form action="/car/{{car['id']}}/abastecimentos/add" method="post" class="styled-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="data">Data *</label>
                    <input type="date" id="data" name="data" value="{{hoje}}" required>
                </div>
                <div class="form-group">
                    <label for="km">Quilometragem no Hodômetro (km) *</label>
                    <input type="number" id="km" name="km" value="{{car['km_atual']}}" min="0" required>
                </div>
                <div class="form-group">
                    <label for="combustivel">Combustível *</label>
                    <select id="combustivel" name="combustivel">
                        <option value="Gasolina Comum">Gasolina Comum</option>
                        <option value="Gasolina Aditivada">Gasolina Aditivada</option>
                        <option value="Etanol">Etanol</option>
                        <option value="Diesel S10">Diesel S10</option>
                        <option value="GNV">GNV</option>
                        <option value="Recarga Elétrica">Recarga Elétrica</option>
                    </select>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="litros">Quantidade (Litros) *</label>
                    <input type="number" step="0.01" min="0.1" id="litros" name="litros" placeholder="Ex: 42.50" required oninput="calcularPrecoLitro()">
                </div>
                <div class="form-group">
                    <label for="valor_total">Valor Total Pago (R$) *</label>
                    <input type="number" step="0.01" min="0.01" id="valor_total" name="valor_total" placeholder="Ex: 250.00" required oninput="calcularPrecoLitro()">
                </div>
                <div class="form-group">
                    <label for="preco_litro_preview">Preço por Litro Calculado</label>
                    <input type="text" id="preco_litro_preview" value="R$ 0,00 / L" readonly class="readonly-input">
                </div>
            </div>

            <div class="form-group">
                <label for="posto">Posto de Combustível (Opcional)</label>
                <input type="text" id="posto" name="posto" placeholder="Ex: Posto Shell / Ipiranga / Petrobras">
            </div>

            <div class="checkbox-card">
                <label class="checkbox-label">
                    <input type="checkbox" name="tanque_cheio" checked>
                    <span>
                        <strong>Tanque Completo (Cheio)</strong>
                        <small>Permite o cálculo preciso de consumo (km/L) em relação ao abastecimento anterior.</small>
                    </span>
                </label>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-floppy-disk"></i> Salvar Abastecimento
                </button>
                <a href="/carros/{{car['id']}}?tab=abastecimentos" class="btn btn-secondary">Cancelar</a>
            </div>
        </form>
    </div>
</div>
