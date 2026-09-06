"""EN: Middleware package initialization. | ES: Inicializacion del paquete de middleware."""

from infrastructure.middleware.error_handler import register_error_handlers

__all__ = ["register_error_handlers"]
