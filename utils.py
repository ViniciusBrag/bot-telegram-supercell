def parse_order(text: str):
    """
    Recebe um texto no formato:
    '4 tela iphone xs max'
    
    Retorna:
    (quantidade, modelo)
    Exemplo:
    ('4', 'iphone xs max')
    """
    # divide o texto em no máximo 3 partes
    text_split = text.split(maxsplit=2)

    if len(text_split) < 3:
        logging.ERROR('Error format invalid')
        raise ValueError("Formato inválido. Use: '<quantidade> <item> <modelo>'")

    quantity = text_split[0]
    model = text_split[2]        
    return quantity, model