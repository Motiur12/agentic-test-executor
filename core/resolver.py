from settings.variables import VARIABLES


class Resolver:

    @staticmethod
    def resolve(value):

        if not isinstance(value, str):
            return value

        if value.startswith("${") and value.endswith("}"):

            key = value[2:-1]

            return VARIABLES.get(key, value)

        return value