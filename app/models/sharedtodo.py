from beanie import Document, Link

from .user import UserModel
from .todo import TodoModel

class SharedTodoModel(Document):
    todo: Link[TodoModel]
    owner: Link[UserModel]
    shared_with: Link[UserModel]

    def __repr__(self) -> str:
        return f"<SharedTodo todo={self.todo}, owner={self.owner}, shared_with={self.shared_with}>"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(str(self.owner) + str(self.shared_with))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SharedTodoModel):
            return self.todo == other.todo \
                   and self.owner == other.owner \
                   and self.shared_with == other.shared_with
        return False

    class Settings:
        name = "sharedtodos"
