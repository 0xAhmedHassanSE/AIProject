"""
================================================================================
  gym_compat.py — Gymnasium Compatibility Shim
================================================================================
  This module provides a minimal stub of the `gymnasium` API so that the
  project can run in environments where the `gymnasium` package is not
  installed.  When `gymnasium` IS installed (the recommended case), this
  module is never imported — the real library takes precedence.

  Install the real library with:
      pip install gymnasium numpy matplotlib

  This shim is only used as a fallback for offline / sandboxed environments.
================================================================================
"""


class _Discrete:
    """Minimal stand-in for gymnasium.spaces.Discrete."""

    def __init__(self, n: int):
        self.n = n

    def contains(self, x) -> bool:
        return isinstance(x, int) and 0 <= x < self.n

    def __repr__(self):
        return f"Discrete({self.n})"


class _Spaces:
    """Namespace that exposes spaces.Discrete."""
    Discrete = _Discrete


class _Env:
    """
    Minimal stand-in for gymnasium.Env.

    Provides the same interface contract:
      • self.observation_space
      • self.action_space
      • self.np_random  (seeded numpy RNG)
      • reset(seed, options) → (obs, info)
      • step(action)         → (obs, reward, terminated, truncated, info)
      • render()
    """

    metadata = {}

    def __init__(self):
        self.observation_space = None
        self.action_space      = None
        import numpy as np
        self.np_random = np.random.default_rng(None)

    def reset(self, *, seed=None, options=None):
        if seed is not None:
            import numpy as np
            self.np_random = np.random.default_rng(seed)
        # Base class does nothing else; subclass handles the real reset logic.

    def step(self, action):
        raise NotImplementedError

    def render(self):
        pass

    def close(self):
        pass


# ---------------------------------------------------------------------------
# Build a fake `gymnasium` module that maze_env.py can import from
# ---------------------------------------------------------------------------
import sys
import types

def _install_shim():
    """Inject the shim as `gymnasium` in sys.modules."""
    mod = types.ModuleType("gymnasium")
    mod.Env    = _Env
    mod.spaces = _Spaces
    sys.modules["gymnasium"]        = mod
    sys.modules["gymnasium.spaces"] = _Spaces
    print(
        "[gym_compat] NOTE: 'gymnasium' not found — using built-in shim.\n"
        "             For full functionality, run: pip install gymnasium\n"
    )


# Auto-install shim if gymnasium is genuinely absent
try:
    import gymnasium  # noqa: F401
except ModuleNotFoundError:
    _install_shim()
