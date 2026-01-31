import argparse
from task_manager.storage import load_task, save_task, StorageError

def build_parser():
    parser = argparse.ArgumentParser(prog="CLI", description="CLI Task Manager")

    subparser = parser.add_subparsers(dest="command", required=True)
    
    # List
    list_parser = subparser.add_parser("list")

    # Add
    add_parser = subparser.add_parser("add")
    add_parser.add_argument("title")    

    # Delete
    delete_parser = subparser.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    # Done
    done_parser = subparser.add_parser("done")
    done_parser.add_argument("id", type=int)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        tasks = load_task("storage.json")
    except StorageError as e:
        print(f"Błąd danych: {e}")
        raise SystemExit(1)
    
    if args.command == "list":
        if not tasks:
            print("Brak zadań")
            return 
        
        for t in tasks:
            done = "x" if t.get("done") else " "
            print(f"[#{t.get('id','?')}] [{done}] {t.get('title','')}")

    elif args.command == "add":
        title = args.title.strip()

        if not title:
            print("Nie podana tytułu")
            exit(1)
        
        new_id = max([t["id"] for t in tasks], default=0) + 1
        tasks.append({"id": new_id, "title": title, "done":False})

        save_task("storage.json", tasks)

    elif args.command == "delete":
        selected_id = args.id
        
        for i, t in enumerate(tasks):
            if t.get("id") == selected_id:
                del tasks[i]
                save_task("storage.json", tasks)
                print("Usunięto zadanie")
                return
            
        print(f"Nie znaleziono podanego ID: {selected_id}")
        raise SystemExit(1)

    elif args.command == "done":
        selected_id = args.id

        for t in tasks:
            if t.get("id") == selected_id:
                t["done"] = True
                save_task("storage.json", tasks)
                print("Zadanie wykonane")
                return
            
        print(f"Nie znaleziono podanego ID: {selected_id}")
        raise SystemExit(1)
            
        




