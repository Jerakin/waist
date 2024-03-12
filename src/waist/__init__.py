from functools import wraps
from typing import TypeVar, Callable
from packaging.version import Version
from packaging.specifiers import Specifier
import logging


__all__ = ["API", "APIError"]


T = TypeVar("T")
logger = logging.getLogger(__name__)
logging.basicConfig()


class APIError(Exception):
    pass


def is_in_class(f: Callable) -> bool:
    """Check if a function is part of a class."""
    parts = f.__qualname__.split(".")
    return len(parts) >= 2 and parts[-2] != "<locals>"


def _split_parts(f: Callable):
    qualified_name = f.__module__ + "." + f.__qualname__
    return qualified_name.split(".")


def get_class(f: Callable) -> str:
    """Assuming that `f` is part of a class, get the fully qualified name of the
    class."""
    parts = _split_parts(f)
    return ".".join(parts[:-1])


class API:
    """Namespace for API functions.

    Create an instance of API with the version you want to dispatch too.

    Functions registered to this namespace will be called if their API version
     is the same as the registered.
    """
    def __init__(self, version: str | Version):
        self.version = self.__to_version(version)
        self.functions: dict[Version, Callable] = {}
        self.classes: dict[str, dict[Version, Callable]] = {}

    @staticmethod
    def __to_version(version):
        if isinstance(version, Version):
            return version
        if isinstance(version, str):
            return Version(version)
        if isinstance(version, tuple):
            return Version(".".join(version))
        raise TypeError("'%s' is not a Version")

    def _get_namespace(self, method: Callable) -> dict:
        if is_in_class(method):
            owner = get_class(method)
            if owner not in self.classes:
                self.classes[owner] = {}
            namespace = self.classes[owner]
        else:
            namespace = self.functions
        return namespace

    def _add_function(self, method: Callable, version_spec: None | Specifier | str):
        if version_spec is not None:
            version_spec = version_spec if isinstance(version_spec, Specifier) else Specifier(version_spec)

        namespace = self._get_namespace(method)
        name = method.__name__
        if name not in namespace:
            namespace[name] = {}
        if version_spec in namespace[name]:
            raise APIError("Can not register multiple functions to the same version.")
        namespace[name][version_spec] = method

    def _get_method(self, method, namespace):
        specifiers = []
        for s in namespace[method.__name__]:
            if s is None:
                continue
            if self.version in s:
                specifiers.append(s)
        if len(specifiers) > 1:
            logger.debug("Multiple overlapping specifiers, getting latest")
        if not specifiers:
            if None in namespace[method.__name__]:
                logger.debug("No matching version found, using default.")
                return namespace[method.__name__][None]

        specifiers.sort(key=lambda x: x.version)
        return None if not specifiers else namespace[method.__name__][specifiers[-1]]

    def __call__(self, version_spec: None | Specifier | str = None):
        def decorator(method):
            self._add_function(method, version_spec)

            @wraps(method)
            def wrapped(*args, **kwargs):
                namespace = self._get_namespace(method)
                selected = self._get_method(method, namespace)
                if not selected:
                    raise (APIError
                           (f"No function registered to '{self.version}'"))
                return selected(*args, **kwargs)
            return wrapped
        return decorator


# class StrictAPI:
#     """Namespace for API functions.
#
#     Create an instance of API with the version you want to dispatch too.
#
#     Functions registered to this namespace will be called if their API version
#      is the same as the registered.
#     """
#     def __init__(self, version: T):
#         self.version = version
#         self.functions: dict[T, Callable] = {}
#         self.classes: dict[str, dict[T, Callable]] = {}
#
#     def _get_namespace(self, method: Callable) -> dict:
#         if is_in_class(method):
#             owner = get_class(method)
#             if owner not in self.classes:
#                 self.classes[owner] = {}
#             namespace = self.classes[owner]
#         else:
#             namespace = self.functions
#         return namespace
#
#     def _add_function(self, method: Callable, version: T):
#         namespace = self._get_namespace(method)
#         name = method.__name__
#         if name not in namespace:
#             namespace[name] = {}
#         if version in namespace[name]:
#             raise APIError("Can not register multiple functions to the same version.")
#         namespace[name][version] = method
#
#     def __call__(self, version: T):
#         def decorator(method):
#             self._add_function(method, version)
#
#             @wraps(method)
#             def wrapped(*args, **kwargs):
#                 namespace = self._get_namespace(method)
#                 name = method.__name__
#                 if self.version not in namespace[name]:
#                     raise (APIError
#                            (f"No function registered to '{self.version}'"))
#                 return namespace[name][self.version](*args, **kwargs)
#             return wrapped
#         return decorator
#
