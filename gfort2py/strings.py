from __future__ import print_function
import ctypes
from .var import fVar


class fStr(fVar):

    def __init__(self, lib, obj,TEST_FLAG=False):
        self.__dict__.update(obj)
        self._lib = lib
        self._ctype = self.ctype_def()
       # self._ctype_f = self.ctype_def_func()
        self._pytype = str
        self.TEST_FLAG=TEST_FLAG

    def py_to_ctype(self, value):
        """
        Pass in a python value returns the ctype representation of it
        """
        return ctypes.c_char(value.encode())
        
    def py_to_ctype_f(self, value):
        """
        Pass in a python value returns the ctype representation of it, 
        suitable for a function
        
        Second return value is anythng that needs to go at the end of the
        arg list, like a string len
        """
        x,y=self.ctype_def_func()
        
        return x(value.encode()),y(len(value))

    def ctype_to_py(self, value):
        """
        Pass in a ctype value returns the python representation of it
        """
        return self._get_var_by_iter(value, self.char_len)
        
    def ctype_def(self):
        return ctypes.c_char

    def ctype_def_func(self):
        """
        The ctype type of a value suitable for use as an argument of a function

        May just call ctype_def
        
        Second return value is anythng that needs to go at the end of the
        arg list, like a string len
        """
        return ctypes.c_char_p,ctypes.c_int

    def set_mod(self, value):
        """
        Set a module level variable
        """
        r = self._get_from_lib()
        self._set_var_from_iter(r, value.encode(), self.char_len)

    def get(self):
        """
        Get a module level variable
        """
        r = self._get_from_lib()
        s = self.ctype_to_py(r)
        return ''.join([i.decode() for i in s])