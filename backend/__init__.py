import importlib, sys
# Expose backend.engines as top‑level 'engines' package for legacy imports
sys.modules['engines'] = importlib.import_module(__name__ + '.engines')
