import json
import os
from typing import Optional
import argparse

# Classe para gerenciar uma lista de quests no formato CLI.


class QuestManager:

    def __init__(self, filename: str = "quests.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    # Adiciona uma quest à lista.
    def add_task(
            self, name: str, description: str, priority: str = "média"
    ) -> None:
        # Verificação de nome vazio.
        if not name.strip():
            raise ValueError("O nome da quest não pode ser vazio.")
        # Impede quests duplicadas.
        if any(task["name"] == name for task in self.tasks):
            raise ValueError(f"quest '{name}' já existe.")
        # Vereficação se prioridade está correta.
        if priority not in ["alta", "média", "baixa"]:
            raise ValueError("Prioridade deve ser 'alta', 'média' ou 'baixa'.")

        task = {
            "name": name, "description": description,
            "priority": priority, "done": False
        }

        self.tasks.append(task)
        self.save_tasks()

    # Retorna a lista de quests.
    def list_tasks(self) -> list[dict]:
        return self.tasks

    # Lista quests ordenadas por prioridade (alta > média > baixa).
    def list_tasks_by_priority(self) -> list[dict]:
        priority_order = {"alta": 1, "média": 2, "baixa": 3}
        sorted_tasks = sorted(
            self.tasks, key=lambda task: priority_order[task["priority"]]
        )
        return sorted_tasks

    # Marca uma quest como concluída pelo nome.
    def complete_task(self, name: str) -> None:
        for task in self.tasks:
            # Verificação se quest existe.
            if task["name"] == name:
                task["done"] = True
                self.save_tasks()
                return
        raise ValueError(f"quest '{name}' não encontrada.")

    # Remove uma quest pelo nome.
    def remove_task(self, name: str) -> None:
        original_count = len(self.tasks)
        # Cria uma nova lista pulando a quest que será removida.
        self.tasks = [task for task in self.tasks if task["name"] != name]
        # Verificação se quest foi removida.
        if len(self.tasks) < original_count:
            self.save_tasks()
        else:
            raise ValueError(f"quest '{name}' não encontrada.")

    # Filtra quests por prioridade (alta, média, baixa).
    def _filter_by_priority(
            self, tasks: list[dict], priority: str
    ) -> list[dict]:

        if priority not in ["alta", "média", "baixa"]:
            raise ValueError("Prioridade inválida.")
        return [task for task in tasks if task["priority"] == priority]

    # Filtra quests por status (pending, done).
    def _filter_by_status(self, tasks: list[dict], status: str) -> list[dict]:

        if status == "pending":
            return [task for task in tasks if not task["done"]]
        elif status == "done":
            return [task for task in tasks if task["done"]]
        raise ValueError("Status inválido. Use 'pending' ou 'done'.")

    def list_filtered_tasks(
            self, status: Optional[str] = None, priority: Optional[str] = None
    ) -> list[dict]:
        """
        Lista quests filtradas por status (pending/done) e/ou
        prioridade (alta/média/baixa).

        Args:
            status: 'pending' ou 'done' (opcional).
            priority: 'alta', 'média' ou 'baixa' (opcional).

        Returns:
            Lista de quests filtradas.
        """
        filtered_tasks = self.tasks
        if status:
            filtered_tasks = self._filter_by_status(filtered_tasks, status)
        if priority:
            filtered_tasks = self._filter_by_priority(filtered_tasks, priority)
        return filtered_tasks

    # Salva as quests em um arquivo JSON.
    def save_tasks(self) -> None:
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    # Carrega as quests de um arquivo JSON, se existir.
    def load_tasks(self) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Gerenciador de Missões Gamer CLI")
    parser.add_argument(
        "action", choices=["add", "list", "complete", "remove"],
        help="Ação a realizar"
    )
    parser.add_argument("--name", help="Nome da missão")
    parser.add_argument("--description", help="Descrição da missão")
    parser.add_argument(
        "--priority", choices=["alta", "média", "baixa"], default="média",
        help="Prioridade da missão"
    )
    parser.add_argument("--filter-status",
                        choices=["pending", "done"], help="Filtrar por status")
    parser.add_argument(
        "--filter-priority", choices=["alta", "média", "baixa"],
        help="Filtrar por prioridade"
    )
    args = parser.parse_args()

    todo = QuestManager()
    if args.action == "add":
        if not args.name or not args.description:
            parser.error("Ação 'add' requer --name e --description")
        todo.add_task(args.name, args.description, args.priority)
        print(f"Missão '{args.name}' adicionada com sucesso! 🎮")
    elif args.action == "list":
        tasks = todo.list_filtered_tasks(
            args.filter_status, args.filter_priority)
        if not tasks:
            print("Nenhuma missão encontrada. 🕹️")
        else:
            print("🎮 Lista de Missões:")
            for task in tasks:
                status = "Completa 🏆" if task["done"] else "Pendente ⚔️"
                print(
                    f"Missão: {task['name']} - {task['description']} "
                    f"({status}, Prioridade: {task['priority']})"
                )
    elif args.action == "complete":
        if not args.name:
            parser.error("Ação 'complete' requer --name")
        todo.complete_task(args.name)
        print(f"Missão '{args.name}' marcada como completa! 🏆")
    elif args.action == "remove":
        if not args.name:
            parser.error("Ação 'remove' requer --name")
        todo.remove_task(args.name)
        print(f"Missão '{args.name}' removida com sucesso! 🗑️")


if __name__ == "__main__":
    main()
