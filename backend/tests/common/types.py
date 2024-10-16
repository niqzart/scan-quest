from typing import Any, Protocol


class Factory[Product](Protocol):
    async def __call__(self, **kwargs: Any) -> Product:  # noqa: U100  # bug
        pass


class PytestRequest[ParamType]:
    @property
    def param(self) -> ParamType:
        raise NotImplementedError


AnyJSON = dict[str, Any]
AnyKwargs = dict[str, Any]
