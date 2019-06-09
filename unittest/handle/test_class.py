from types import FunctionType


class ClassA:

    @staticmethod
    def func_a():
        print('a')

    @classmethod
    def func_b(cls, arg):
        print('b', arg)

    def func_c(self, arg):
        print('c', arg)


def func_d():
    print('d')


if __name__ == '__main__':
    class_a = ClassA()
    print('静态方法，实例调用验证')
    print("callable(class_a.func_a) result: {result}".format(result=callable(class_a.func_a)))
    print("type(class_a.func_a) is FunctionType result: {result}".format(result=type(class_a.func_a) is FunctionType))
    print("hasattr(class_a.func_a, '__call__') result: {result}".format(result=hasattr(class_a.func_a, '__call__')))

    print('静态方法，类调用验证')
    print("callable(ClassA.func_a) result: {result}".format(result=callable(ClassA.func_a)))
    print("type(ClassA.func_a) is FunctionType result: {result}".format(result=type(ClassA.func_a) is FunctionType))
    print("hasattr(ClassA.func_a, '__call__') result: {result}".format(result=hasattr(ClassA.func_a, '__call__')))

    print('类方法验证')
    print("callable(ClassA.func_b) result: {result}".format(result=callable(ClassA.func_b)))
    print("type(ClassA.func_b) is FunctionType result: {result}".format(result=type(ClassA.func_b) is FunctionType))
    print("hasattr(ClassA.func_b, '__call__') result: {result}".format(result=hasattr(ClassA.func_b, '__call__')))

    print('实例方法验证')
    print("callable(class_a.func_c) result: {result}".format(result=callable(class_a.func_c)))
    print("type(class_a.func_c) is FunctionType result: {result}".format(result=type(class_a.func_c) is FunctionType))
    print("hasattr(class_a.func_c, '__call__') result: {result}".format(result=hasattr(class_a.func_c, '__call__')))

    print('函数验证')
    print("callable(func_d) result: {result}".format(result=callable(func_d)))
    print("type(func_d) is FunctionType result: {result}".format(result=type(func_d) is FunctionType))
    print("hasattr(func_d, '__call__') result: {result}".format(result=hasattr(func_d, '__call__')))
