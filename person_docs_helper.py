import re

from validate_docbr import CPF


def remove_mask(string: str) -> str:
    return re.sub("[^0-9]", "", string)


def mask_cpf(cpf: str) -> str:
    _cpf: str = remove_mask(cpf)
    if len(_cpf) == 11:
        return CPF().mask(_cpf)
    else:
        return _cpf


def validate_cpf(cpf: str) -> bool:
    _cpf: str = remove_mask(cpf)
    if len(_cpf) == 11:
        return CPF().validate(_cpf)
    return False
