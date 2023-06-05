import inspect


def validate_arguments(func_args, task_args):
    for param_name, param_obj in func_args:
        if param_name not in task_args:
            if param_obj.default is inspect.Parameter.empty and param_obj.kind != inspect.Parameter.VAR_KEYWORD:
                raise TypeError(f"{param_name} is a required parameter")
        else:
            arg_value = task_args[param_name]

            if param_obj.kind == inspect.Parameter.VAR_KEYWORD:
                continue
            elif param_obj.kind == inspect.Parameter.VAR_POSITIONAL:
                continue
            elif param_obj.annotation is not inspect.Parameter.empty:
                if not isinstance(arg_value, param_obj.annotation):
                    raise TypeError(f"{param_name} must be of type {param_obj.annotation.__name__}")

    unexpected_args = set(task_args.keys()) - {param_name for param_name, _ in func_args}

    if unexpected_args and not any(p.kind == inspect.Parameter.VAR_KEYWORD for _, p in func_args):
        raise TypeError(f"Unexpected argument{'' if len(unexpected_args) == 1 else 's'}: {', '.join(unexpected_args)}")

    return True
