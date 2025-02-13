r"""
    inlcude HTTP and backend server and client exception   
    => http backend , client excpetion 에러 모음 
"""


class BaseRPCException(Exception):
    r"""
    Base RPC exception.
    """    
    pass

class BadRequestException(BaseRPCException):
    r"""
    BadRequestException reporesent HTTP code 400.
    """
    pass

class InternalServerErrorException(BaseRPCException):
    r"""
    InternalServerError Exception represent HTTP code 500.
    """
    pass

class NotFoundException(BaseRPCException):
    r"""
    NotFoundException HTTP code 404.
    """
    pass

class HTTPConnectionException(BaseRPCException):
    r"""
    HTTPConnectionException represent HTTP connection error.
    """
    pass

class ForbiddenException(BaseRPCException):
    r"""
    ForbiddenException reporesent HTTP code 403.
    """
    pass