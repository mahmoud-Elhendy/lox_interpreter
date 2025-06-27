from typing import Any


class Env():
    def __init__(self) -> None:
        self.env: dict[str, Any] = dict()

    def put(self, k: str, v: Any) -> None:
        self.env[k] = v

    def get(self, k: str) -> Any:
        if k in self.env:
            return self.env[k]
        else:
            raise RuntimeError(f'Undefined variable {k} .')
