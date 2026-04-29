class KernelError(Exception):
    pass

class ContractViolation(KernelError):
    pass

class InvalidTransition(KernelError):
    pass
