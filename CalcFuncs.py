# Class to encapsulate functions for calculator

class CalcFuncs:

    @staticmethod
    def add(operands):
        return operands[0]+operands[1]
    
    @staticmethod
    def subtract(operands):
        return operands[0]-operands[1]

    @staticmethod
    def multiply(operands):
        return operands[0]*operands[1]

    @staticmethod
    def divide(operands):
        return operands[0]/operands[1]

    @staticmethod
    def exp(operands):
        return operands[0]**operands[1]

    @staticmethod
    def sqareRoot(operands):
        # Easy approach:
        # return operands[0]**.5
        # More involved approach:
        x = operands[0]
        last_guess= x/2.0
        while True:
          # Apply Babylonian Squre Root Algorithm
          guess = (last_guess + x/last_guess)/2
          if abs(guess - last_guess) < .000001: # example threshold
               return guess
          last_guess= guess

   