"""
Staged pipeline engine. Domain-agnostic.

Public API:
    from openwave.xperiments.m4_ewt.pipeline_engine import (
        Context, RunContext, SimContext, LogContext, Diagnostics,
        FeatureBag, Params,
        Stage, ErrorPolicy, IProcessor, BaseProcessor, Pipeline, PipelineError,
        ILogSink, JsonSessionSink, LiveJsonSink, InMemorySink,
        LogProcessor,
        IRunner, Runner,
    )

Design rules:
    Z1. Zero module-level state.
    Z2. Every mutation goes through a processor.
    Z3. Explicit requires/provides graph, validated at Pipeline.build().
    Z4. setup/teardown are lifecycle hooks; process() is per-step.
    Z5. The runner is an interface (IRunner). Runner is the default impl.
    Z6. Sinks are an interface (ILogSink). Several implementations.
    Z7. Measurement and logging are separate processors.
    Z8. Params are typed and grouped separately from run identity.
"""

from .contracts import ScatteringOperatorInterface, SourceTermInterface
from .experiments import ExperimentConfig, ExperimentRunner, ExperimentSummary
from .context import (
    Context,
    Diagnostics,
    FeatureBag,
    LogContext,
    Params,
    RunContext,
    SimContext,
)
from .pipeline import (
    BaseProcessor,
    ErrorPolicy,
    IProcessor,
    Pipeline,
    PipelineError,
    PipelineStopSignal,
    Stage,
)
from .sinks import ILogSink, InMemorySink, JsonSessionSink, LiveJsonSink
from .loggers import LogProcessor
from .runner import IRunner, Runner

__all__ = [
    # context
    "Context",
    "Diagnostics",
    "FeatureBag",
    "LogContext",
    "Params",
    "RunContext",
    "SimContext",
    # pipeline
    "BaseProcessor",
    "ErrorPolicy",
    "IProcessor",
    "Pipeline",
    "PipelineError",
    "PipelineStopSignal",
    "Stage",
    # sinks
    "ILogSink",
    "InMemorySink",
    "JsonSessionSink",
    "LiveJsonSink",
    # loggers
    "LogProcessor",
    # runner
    "IRunner",
    "Runner",
    "ScatteringOperatorInterface",
    "SourceTermInterface",
    "ExperimentConfig",
    "ExperimentRunner",
    "ExperimentSummary",
]
