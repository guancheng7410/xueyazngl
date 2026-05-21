#!/usr/bin/env python3
"""
Python 3.14 compatibility patch for SQLAlchemy 2.0.x
"""
import sys
if sys.version_info >= (3, 14):
    import typing
    _orig_generic_init_subclass = typing._generic_init_subclass
    
    def _patched_generic_init_subclass(cls, *args, **kwargs):
        if hasattr(cls, '__orig_bases__'):
            for base in cls.__orig_bases__:
                if getattr(base, '__origin__', None) is typing.Generic:
                    break
            else:
                if hasattr(cls, '__mro__'):
                    for base in cls.__mro__:
                        if base.__module__ == 'typing' and 'TypingOnly' in base.__name__:
                            return
        return _orig_generic_init_subclass(cls, *args, **kwargs)
    
    typing._generic_init_subclass = _patched_generic_init_subclass
