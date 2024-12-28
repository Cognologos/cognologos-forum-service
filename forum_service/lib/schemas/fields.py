from logging import getLogger
from typing import Any, Self, no_type_check

from fastapi import Path, Query
from pydantic.fields import Field, FieldInfo

from .enums.filter import FilterType


logger = getLogger(__name__)


@no_type_check
def wrap_field(field_info: Any) -> Any:
    if not isinstance(field_info, FieldInfo):
        raise TypeError("field_info must be an instance of pydantic.FieldInfo (or a subclass)")
    if getattr(field_info, "__is_wrapped_field__", False):
        logger.warning(
            "Attempt to wrap a wrapped field. Ignoring and returning it back. This is probably a bug. Field: (%s) %s",
            field_info.__class__.__name__,
            field_info,
        )
        return field_info

    class WrappedField(field_info.__class__):  # type: ignore
        __is_wrapped_field__ = True

        def _get_kwargs(self) -> dict[str, Any]:
            return object.__getattribute__(self, "_inititial_kwargs").copy()

        def __call__(self, **new_kwargs: Any) -> Any:
            kwargs = self._get_kwargs()
            kwargs.update(new_kwargs)
            return self.__class__._init_wrapped(kwargs)

        @classmethod
        def _init_wrapped(cls, initial_kwargs: dict[str, Any]) -> Self:
            suffix = initial_kwargs.pop("suffix", None)
            if suffix is not None:
                initial_kwargs["description"] = initial_kwargs.get("description", "") + " " + suffix

            prefix = initial_kwargs.pop("prefix", None)
            if prefix is not None:
                initial_kwargs["description"] = prefix + " " + initial_kwargs.get("description", "")

            if initial_kwargs.get("description") is not None:
                initial_kwargs["description"] = initial_kwargs["description"].strip()

            c = cls(**initial_kwargs)
            object.__setattr__(c, "_inititial_kwargs", initial_kwargs)
            object.__setattr__(c, "__doc__", initial_kwargs.get("description"))  # replace docstring
            return c

        def to_class(self, _class: Any, **new_kwargs: Any) -> Any:
            kwargs = self._get_kwargs()
            kwargs.update(new_kwargs)
            return wrap_field(_class(**kwargs))

        def to_path(self) -> Any:
            if hasattr(self, "_path_cache"):
                return self._path_cache
            kwargs = self._get_kwargs()
            kwargs.pop("default")
            path = Path(**kwargs)
            setattr(self, "_path_cache", path)
            return path

        def to_query(self) -> Any:
            if hasattr(self, "_query_cache"):
                return self._query_cache
            kwargs = self._get_kwargs()
            kwargs.pop("default")
            query = Query(**kwargs)
            setattr(self, "_query_cache", query)
            return query

        @property
        def path(self) -> Any:
            return self.to_path()

        @property
        def query(self) -> Any:
            return self.to_query()

    WrappedField.__name__ = "Wrapped" + field_info.__class__.__name__
    dict_ = {}
    for attr in field_info.__slots__:
        dict_[attr] = getattr(field_info, attr)
    if "extra" in dict_:
        extra = dict_.pop("extra")
        if extra is not None:
            dict_.update(extra)
    return WrappedField._init_wrapped(dict_)


# Common fields.
# Regexes are taken from https://ihateregex.io/
BaseField = wrap_field(Field())

TIMESTAMP = BaseField(description="Timestamp in seconds since UNIX epoch.", examples=[1610000000], ge=0)
DATETIME = BaseField(description="Date and time in ISO 8601 format.", examples=["2021-01-07T12:00:00Z"])

UUID = BaseField(
    description="UUID version 4.",
    examples=["123e4567-e89b-12d3-a456-426614174000"],
)
ID = BaseField(
    description="Unique integer autoincrementing identifier.",
    examples=[1],
    ge=0,
)
ORDER_BY_FILTER = BaseField(
    description="Order by filter.",
    default=None,
    filter_type=FilterType.order_by,
)
