from pulsar import Function


class AdditionFunction(Function):

    def process(self, input, context):
        print(input)
        return input + 1
