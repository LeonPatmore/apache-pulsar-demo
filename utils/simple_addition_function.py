from pulsar import Function


class AdditionFunction(Function):

    def process(self, input, context):
        print(input)
        context.publish("output", input + "hi")
