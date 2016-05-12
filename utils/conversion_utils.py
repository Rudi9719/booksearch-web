#!/usr/bin/env python

from api.base import BaseApi


class ConversionApi(BaseApi):

    CM_IN_IN = 2.54
    KG_IN_LB = 0.453592

    SYSTEM_UK = "uk"
    SYSTEM_USA = "usa"

    # TODO: Handle rounding
    def cm_to_in(self, cm):
        return cm / self.CM_IN_IN

    def in_to_cm(self, inches):
        return inches * self.CM_IN_IN

    def kg_to_lb(self, kg):
        return kg / self.KG_IN_LB

    def lb_to_kg(self, lb):
        return lb * self.KG_IN_LB

    def convert_dress_size(self, size, from_system, to_system):

        converted_size = None

        if from_system == self.SYSTEM_USA and to_system == self.SYSTEM_UK:
            converted_size = self.in_to_cm(size)
        elif from_system == self.SYSTEM_UK and to_system == self.SYSTEM_USA:
            converted_size = self.cm_to_in(size)

        return converted_size

    def convert_shoe_size(self, size, from_system, to_system):

        converted_size = None

        if from_system == self.SYSTEM_USA and to_system == self.SYSTEM_UK:
            converted_size = self.in_to_cm(size)
        elif from_system == self.SYSTEM_UK and to_system == self.SYSTEM_USA:
            converted_size = self.cm_to_in(size)

        return converted_size

    def convert_height(self, size, from_system, to_system):

        converted_size = None

        if from_system == self.SYSTEM_USA and to_system == self.SYSTEM_UK:
            converted_size = self.in_to_cm(size)
        elif from_system == self.SYSTEM_UK and to_system == self.SYSTEM_USA:
            converted_size = self.cm_to_in(size)

        return converted_size

    def convert_weight(self, size, from_system, to_system):

        converted_size = None

        if from_system == self.SYSTEM_USA and to_system == self.SYSTEM_UK:
            converted_size = self.lb_to_kg(size)
        elif from_system == self.SYSTEM_UK and to_system == self.SYSTEM_USA:
            converted_size = self.kg_to_lb(size)

        return converted_size
