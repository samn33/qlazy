# -*- coding: utf-8 -*-

def get_lib_ext():
    
    import platform
    if platform.system() == 'Darwin':
        return 'dylib'
    else:
        return 'so'
