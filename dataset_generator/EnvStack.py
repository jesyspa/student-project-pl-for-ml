class EnvStack:
    def __init__(self):
        self.env_stack = [set()]
        self.funcs = set()

    def current_env(self):
        return self.env_stack[-1]

    def set_var(self, name):
        self.current_env().add(name)

    def is_available(self, name):
        return any(name in env for env in reversed(self.env_stack))

    def all_vars(self):
        return list(set().union(*self.env_stack))

    def push(self):
        self.env_stack.append(set())

    def pop(self):
        self.env_stack.pop()

    def reset(self):
        self.env_stack = [set()]
        self.funcs = set()

    def define_func(self, name):
        self.funcs.add(name)

    def all_funcs(self):
        return list(self.funcs)