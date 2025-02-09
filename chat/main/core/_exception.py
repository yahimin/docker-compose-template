r"""
    inlcude HTTP and backend server  exception    
"""


class BaseRPCException(Exception):
    r"""
        Base RPC exception.
    """    
    pass


class InternalServerErrorException(BaseRPCException):
    r"""
    InternalServerError Exception represent HTTP code 500.
    """
    
    pass
