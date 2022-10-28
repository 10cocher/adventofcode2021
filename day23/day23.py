from typing import Dict, List, Tuple, Union

TYPE_LIST_INSTR = List[Tuple[Union[int, str], Union[int, str]]]

list_chars: List[str] = ["A", "B", "C", "D"]
char_to_weight: Dict[str, int] = {"A": 1, "B": 10, "C": 100, "D": 1000}

room_init_toy = {
    "aup": "B",
    "adown": "A",
    "bup": "C",
    "bdown": "D",
    "cup": "B",
    "cdown": "C",
    "dup": "D",
    "ddown": "A",
}
list_instr_toy: TYPE_LIST_INSTR = [
    ("cup", 3),
    ("bup", "cup"),
    ("bdown", 5),
    (3, "bdown"),
    ("aup", "bup"),
    ("dup", 7),
    ("ddown", 9),
    (7, "ddown"),
    (5, "dup"),
    (9, "aup"),
]
room_init_puz = {
    "aup": "A",
    "adown": "D",
    "bup": "C",
    "bdown": "D",
    "cup": "B",
    "cdown": "A",
    "dup": "B",
    "ddown": "C",
}
list_instr_puz_try1: TYPE_LIST_INSTR = [
    ("bup", 3),
    ("bdown", 10),
    ("cup", "bdown"),
    ("dup", "bup"),
    ("cdown", 9),
    (3, "cdown"),
    ("ddown", "cup"),
    ("aup", 1),
    ("adown", "ddown"),
    (1, "adown"),
    (9, "aup"),
    (10, "dup")

]

list_instr_puz_try2: TYPE_LIST_INSTR = [
    ("cup", 1),
    ("cdown", 9),
    ("bup", "cdown"),
    ("dup", 3),
    ("ddown", "cup"),
    ("bdown", "ddown"),
    (3, "bdown"),
    (1, "bup"),
    ("aup", 1),
    ("adown", "dup"),
    (1, "adown"),
    (9, "aup")
]

list_instr_puz_try3: TYPE_LIST_INSTR = [
    ("cup", 9),
    ("cdown", 0),
    ("bup", "cdown"),
    ("dup", 3),
    ("ddown", "cup"),
    ("bdown", "ddown"),
    (3, "bdown"),
    (9, "bup"),
    ("aup", 1),
    ("adown", "dup"),
    (1, "adown"),
    (0, "aup")
]

list_instr_puz: TYPE_LIST_INSTR = [
    ("aup", 1),
    ("adown", 3),
    (1, "adown"),
    #("cup", 9),
    #("cdown", 1),
    #("bup", "cdown"),
    #("dup", 3),
    #("ddown", "cup"),
    #("bdown", "ddown"),
    #(3, "bdown"),
    #(9, "bup"),
    #("aup", 3),
    #("adown", "dup"),
    #(3, "adown"),
    #(1, "aup")
]


class Game:
    def __init__(self, room: Dict[str, str]) -> None:
        self.score: int = 0
        #
        self.hallway: List[str] = ["." for i in range(11)]
        #
        self.room: Dict[str, str] = {}
        self.room["aup"] = room["aup"]
        self.room["adown"] = room["adown"]
        self.room["bup"] = room["bup"]
        self.room["bdown"] = room["bdown"]
        self.room["cup"] = room["cup"]
        self.room["cdown"] = room["cdown"]
        self.room["dup"] = room["dup"]
        self.room["ddown"] = room["ddown"]

    def dist_room_room(self, pos_room_1: str, pos_room_2: str) -> int:
        tot = 0
        ud1 = pos_room_1[1]
        ud2 = pos_room_2[1]
        #
        for char in [ud1, ud2]:
            if char == "u":
                tot += 1
            elif char == "d":
                tot += 2
        #
        char_to_col = {"a": 2, "b": 4, "c": 6, "d": 8}
        #
        col1 = pos_room_1[0]
        col2 = pos_room_2[0]
        tot += abs(char_to_col[col1] - char_to_col[col2])
        return tot

    def dist_room_hallway(self, pos_room: str, pos_hallway: int) -> int:
        if pos_room == "aup":
            return 1 + abs(pos_hallway - 2)
        elif pos_room == "adown":
            return 2 + abs(pos_hallway - 2)
        elif pos_room == "bup":
            return 1 + abs(pos_hallway - 4)
        elif pos_room == "bdown":
            return 2 + abs(pos_hallway - 4)
        elif pos_room == "cup":
            return 1 + abs(pos_hallway - 6)
        elif pos_room == "cdown":
            return 2 + abs(pos_hallway - 6)
        elif pos_room == "dup":
            return 1 + abs(pos_hallway - 8)
        elif pos_room == "ddown":
            return 2 + abs(pos_hallway - 8)
        else:
            raise ValueError(f"unknown value {pos_room}")

    def to_hallway(self, pos_room: str, pos_hallway: int) -> None:
        if self.room[pos_room] not in list_chars:
            raise ValueError(f"empty room {pos_room}")
        if self.hallway[pos_hallway] in list_chars:
            raise ValueError("already occupied")
        char = self.room[pos_room]
        self.hallway[pos_hallway] = char
        self.room[pos_room] = "."
        self.score += char_to_weight[char] * self.dist_room_hallway(
            pos_room, pos_hallway
        )
        return

    def to_room(self, pos_room: str, pos_hallway: int) -> None:
        if self.room[pos_room] in list_chars:
            raise ValueError("already occupied")
        if self.hallway[pos_hallway] not in list_chars:
            raise ValueError("empty hallway pos {pos_room}")
        char = self.hallway[pos_hallway]
        self.room[pos_room] = char
        self.hallway[pos_hallway] = "."
        self.score += char_to_weight[char] * self.dist_room_hallway(
            pos_room, pos_hallway
        )
        return

    def room_to_room(self, pos_from: str, pos_to: str) -> None:
        if self.room[pos_to] in list_chars:
            raise ValueError("already occupied")
        if self.room[pos_from] not in list_chars:
            raise ValueError("empty")
        char = self.room[pos_from]
        self.room[pos_to] = char
        self.room[pos_from] = "."
        self.score += char_to_weight[char] * self.dist_room_room(pos_from, pos_to)
        return

    def apply_instr(self, pos_from: Union[int, str], pos_to: Union[int, str]) -> None:
        if isinstance(pos_from, int) and isinstance(pos_to, str):
            self.to_room(pos_to, pos_from)
        elif isinstance(pos_from, str) and isinstance(pos_to, int):
            self.to_hallway(pos_from, pos_to)
        elif isinstance(pos_from, str) and isinstance(pos_to, str):
            self.room_to_room(pos_from, pos_to)
        else:
            raise ValueError("non valid")
        return

    def print_board(self) -> None:
        print(" ")
        print("#############")
        print("#" + "".join(list(self.hallway)) + "#")
        line = "###"
        for col in ["a", "b", "c", "d"]:
            line += self.room[f"{col}up"]
            line += "#"
        line += "##"
        print(line)
        line = "  #"
        for col in ["a", "b", "c", "d"]:
            line += self.room[f"{col}down"]
            line += "#"
        print(line)
        print("  #########")
        print(" ")
        return

    def print_score(self) -> None:
        print(f"score = {self.score}")


if __name__ == "__main__":
    list_instr: TYPE_LIST_INSTR
    room_init: Dict[str, str]

    if True:
        list_instr = list_instr_puz_try3
        room_init = room_init_puz
    else:
        list_instr = list_instr_toy
        room_init = room_init_toy
    #

    g = Game(room_init)
    #
    g.print_board()
    #
    for pos_from, pos_to in list_instr:
        g.apply_instr(pos_from, pos_to)
        g.print_board()
        g.print_score()
