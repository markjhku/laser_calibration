#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 16:34:20 2025

@author: markjhku
"""



class Mirror():
    def __init__(self, move_mirror_function = None):
       self._position = 0
  
       self._move_mirror_function = move_mirror_function

    def move_mirror_to_position(self,position: float | None = None):
        """
            moves mirror to position x
            x: float can be between -1 to 1  
        """

        if position is not None:
            if abs(position) > 1:
                m = "position must be between -1 and 1"
                raise ValueError(m)
                
            if self._move_mirror_function is not None:
                self._move_mirror_function(position)

            self._position = position
                
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value: float):
        self.move_mirror_to_position(position=value)
        self._position = value


    @property
    def move_mirror_function(self):
        
        return self._move_mirror_function
    
    @move_mirror_function.setter
    def move_mirror_function(self, move_mirror_function):
        self._move_mirror_function = move_mirror_function      
        
        if move_mirror_function is None:
            self.simulation = True
        
        