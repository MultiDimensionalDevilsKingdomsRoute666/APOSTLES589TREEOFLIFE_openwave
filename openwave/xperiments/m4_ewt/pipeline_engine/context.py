"""
Context and shared containers for the pipeline engine.

Contains:
    FeatureBag   -- typed container, key = type, not string
    Params       -- typed read-only view over run parameters
    RunContext   -- immutable run identity (frozen)
    SimContext   -- mutable simulation clock
    LogContext   -- sinks by name
    Diagnostics  -- errors, warnings, timings
    Context      -- the only object a processor sees

Nothing in this module imports from other engine modules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, Mapping, TypeVar

T = TypeVar("T")


# ================================================================
# FeatureBag -- typed container
# ================================================================


class FeatureBag:
    """
    Typed container. Key is the class of the value, not a string.
    Adding a new feature never changes any processor signature.

    A value is registered under its concrete type and every base class in
    its MRO, excluding `object`. This lets a processor require an abstract
    type (ABC, Protocol with a base class, or a plain base class) and
    receive the concrete instance registered under a subclass.

    Usage:
        ctx.data.set(Counter())
        c = ctx.data.require(Counter)
    """

    __slots__ = ("_items",)

    def __init__(self) -> None:
        self._items: dict[type, object] = {}

    def set(self, value: object) -> None:
        """
        Register a value under its concrete type and every base class.

        `object` is excluded so that require(object) does not resolve to
        an arbitrary feature.
        """
        for cls in type(value).__mro__:
            if cls is object:
                continue
            self._items[cls] = value

    def try_get(self, key: type[T]) -> T | None:
        return self._items.get(key)  # type: ignore[return-value]

    def require(self, key: type[T]) -> T:
        if key not in self._items:
            raise KeyError(f"FeatureBag: '{key.__name__}' not present")
        return self._items[key]  # type: ignore[return-value]

    def __contains__(self, key: type) -> bool:
        return key in self._items

    def keys(self) -> Iterator[type]:
        return iter(self._items)


# ================================================================
# Params -- typed view over run parameters
# ================================================================


class Params:
    """
    Typed read-only view over a run's parameters.

    Processors read from ctx.params, never from a raw dict.
    Missing key with a default -> returns default.
    Missing key without a default -> KeyError.
    Wrong type -> TypeError.
    """

    __slots__ = ("_raw",)

    def __init__(self, raw: Mapping[str, Any] | None = None) -> None:
        self._raw: dict[str, Any] = dict(raw or {})

    def __contains__(self, key: str) -> bool:
        return key in self._raw

    def __getitem__(self, key: str) -> Any:
        return self._raw[key]

    def keys(self) -> Iterator[str]:
        return iter(self._raw)

    def get(self, key: str, default: Any = None) -> Any:
        return self._raw.get(key, default)

    def require(self, key: str) -> Any:
        if key not in self._raw:
            raise KeyError(f"Params: '{key}' is required but not provided")
        return self._raw[key]

    # --- typed accessors ---

    def _typed(self, key: str, tp: type | tuple[type, ...], default: Any) -> Any:
        if key not in self._raw:
            return default
        v = self._raw[key]
        if v is None:
            return default
        if not isinstance(v, tp):
            tname = tp.__name__ if isinstance(tp, type) else "/".join(t.__name__ for t in tp)
            raise TypeError(f"Params: '{key}' expected {tname}, got {type(v).__name__}")
        return v

    def get_int(self, key: str, default: int | None = None) -> int | None:
        return self._typed(key, int, default)

    def get_float(self, key: str, default: float | None = None) -> float | None:
        v = self._typed(key, (int, float), default)
        return float(v) if v is not None else None

    def get_str(self, key: str, default: str | None = None) -> str | None:
        return self._typed(key, str, default)

    def get_bool(self, key: str, default: bool | None = None) -> bool | None:
        return self._typed(key, bool, default)

    def get_list(self, key: str, default: list | None = None) -> list | None:
        return self._typed(key, list, default)

    def get_dict(self, key: str, default: dict | None = None) -> dict | None:
        return self._typed(key, dict, default)

    def get_path(self, key: str, default: Path | None = None) -> Path | None:
        v = self._raw.get(key, default)
        return Path(v) if v is not None else None

    # --- required, typed ---

    def require_int(self, key: str) -> int:
        v = self.get_int(key)
        if v is None:
            raise KeyError(f"Params: '{key}' (int) is required")
        return v

    def require_float(self, key: str) -> float:
        v = self.get_float(key)
        if v is None:
            raise KeyError(f"Params: '{key}' (float) is required")
        return v

    def require_str(self, key: str) -> str:
        v = self.get_str(key)
        if v is None:
            raise KeyError(f"Params: '{key}' (str) is required")
        return v


# ================================================================
# Context sub-objects
# ================================================================


@dataclass(frozen=True)
class RunContext:
    """Immutable run identity. Set once by the caller."""

    name: str
    output_dir: Path = Path("out")


@dataclass
class SimContext:
    """Mutable simulation clock."""

    dt: float = 1.0
    t: float = 0.0
    step: int = 0
    should_stop: bool = False


@dataclass
class LogContext:
    """
    Sinks by name. Processors look up by name, not by instance.

    The value type is Any to avoid an import cycle with sinks.py.
    In practice, values implement the ILogSink protocol.
    """

    sinks: dict[str, Any] = field(default_factory=dict)

    def get(self, name: str) -> Any:
        if name not in self.sinks:
            raise KeyError(f"LogContext: no sink named '{name}'")
        return self.sinks[name]


@dataclass
class Diagnostics:
    """Errors, warnings, timings. Populated by the pipeline."""

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    timings: dict[str, list[float]] = field(default_factory=dict)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def time(self, name: str, seconds: float) -> None:
        self.timings.setdefault(name, []).append(seconds)


# ================================================================
# Context -- the single object passed to every processor
# ================================================================


@dataclass
class Context:
    """Everything a processor sees in process()."""

    run: RunContext
    params: Params
    sim: SimContext
    data: FeatureBag
    log: LogContext
    diag: Diagnostics = field(default_factory=Diagnostics)
