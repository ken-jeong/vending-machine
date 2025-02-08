class Cash:
    # constructor(생성자)
    def __init__(self, face_value, quantity):
        self.__face_value = face_value
        self.__quantity = quantity
    
    # getter(접근자) - face_value
    def get_face_value(self):
        return self.__face_value
    
    # getter(접근자) - quantity
    def get_quantity(self):
        return self.__quantity
    
    # setter(설정자) - quantity
    def set_quantity(self, value):
        self.__quantity = value
    
    def amount(self):
        return self.__face_value * self.__quantity