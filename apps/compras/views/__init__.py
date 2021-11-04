from .solicitacoes import (
    SolicitacaoCompraNova, SolicitacaoCompraList, SolicitacaoCompraDetail,
    SolicitacaoCompraEdit, SCListProcesso, vinculasc, consulta_saldo_dl,
)

from .pesquisas import (
    nova_pesquisa_processo, edita_pesquisa
)

from .autocomplete_views import (
    AreaAutocomplete, ResponsavelAutocomplete, CentroCustoAutocomplete,
    ContaContabilAutocomplete, ProdutoAutocomplete
)
