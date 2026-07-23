from settings.variables import VARIABLES


class Resolver:

    @staticmethod
    def resolve(value):

        if not isinstance(value, str):
            return value

        if value.startswith("${") and value.endswith("}"):

            key = value[2:-1]
            resolved = VARIABLES.get(key)

            if not resolved:
                raise ValueError(
                    f"Missing required secret for ${{{key}}}. "
                    f"Set the corresponding CARTUP_{key} environment variable."
                )

            return resolved

        return value
