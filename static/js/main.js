/**
 * RedLine — Scripts de Interatividade e Facilidades de Uso
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Controle de Abas no Painel 360º do Veículo
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach((btn) => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-tab-target');
            tabButtons.forEach((b) => b.classList.remove('active'));
            tabPanes.forEach((p) => p.classList.remove('active'));

            btn.classList.add('active');
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // 2. Auto-dismiss opcional da mensagem flash após 6 segundos
    const flashBanner = document.getElementById('flash-banner');
    if (flashBanner) {
        setTimeout(() => {
            flashBanner.style.transition = 'opacity 0.4s ease';
            flashBanner.style.opacity = '0';
            setTimeout(() => flashBanner.remove(), 400);
        }, 6000);
    }

    // 3. Formatação automática de placa em maiúsculas
    const placaInput = document.getElementById('placa');
    if (placaInput) {
        placaInput.addEventListener('input', function () {
            this.value = this.value.toUpperCase();
        });
    }
});

/**
 * Preenche rapidamente o formulário de Manutenção Programada a partir de um preset
 */
function preencherPresetProgramada(descricao, freqDias, freqKm, custoEstimado) {
    const descEl = document.getElementById('descricao');
    const diasEl = document.getElementById('frequencia_dias');
    const kmEl = document.getElementById('frequencia_km');
    const custoEl = document.getElementById('custo_estimado');

    if (descEl) descEl.value = descricao;
    if (diasEl) diasEl.value = freqDias;
    if (kmEl) kmEl.value = freqKm;
    if (custoEl) custoEl.value = custoEstimado;
}

/**
 * Preenche rapidamente o formulário de Item de Vida Útil a partir de uma sugestão
 */
function preencherPresetVidaUtil(nomeItem, validadeAnos, validadeKm) {
    const nomeEl = document.getElementById('nome_item');
    const anosEl = document.getElementById('validade_anos');
    const kmEl = document.getElementById('validade_km');

    if (nomeEl) nomeEl.value = nomeItem;
    if (anosEl) anosEl.value = validadeAnos;
    if (kmEl) kmEl.value = validadeKm;
}

/**
 * Calcula automaticamente o preço por litro no formulário de Abastecimento
 */
function calcularPrecoLitro() {
    const litrosEl = document.getElementById('litros');
    const valorEl = document.getElementById('valor_total');
    const previewEl = document.getElementById('preco_litro_preview');

    if (!litrosEl || !valorEl || !previewEl) return;

    const litros = parseFloat(litrosEl.value) || 0;
    const valor = parseFloat(valorEl.value) || 0;

    if (litros > 0 && valor > 0) {
        const preco = (valor / litros).toFixed(2).replace('.', ',');
        previewEl.value = `R$ ${preco} / L`;
    } else {
        previewEl.value = 'R$ 0,00 / L';
    }
}
