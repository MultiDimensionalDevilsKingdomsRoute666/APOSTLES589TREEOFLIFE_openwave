"""Core package for the OpenWave project.

Open-source subatomic physics simulator using classical field methods with topology
to study particle and force emergence. GPU-accelerated.

"""

# Calendar versioning, YY.N: the release year, then the release count in that year (26.1,
# 26.2, ...), restarting at 27.1 in January. No zero padding, because PEP 440 strips it and
# "26.011" would install as "26.11", silently unmatching its tag. No letter suffix: PEP 440 reads
# "26.11b" as a beta, which sorts BEFORE 26.11 and is skipped by a default pip install. Keep this
# in sync with pyproject.toml. See dev_docs/VERSION_MANAGEMENT.md.
__version__ = "26.12"
