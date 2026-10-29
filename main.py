from cli import FETCli

def main():
    print("Select execution mode:")
    print("1 => CLI (Command Line Interface)")
    # Future modes can be added here (e.g., Web, GUI)
    
    mode = input("Write mode (default is cli): \n").strip().lower()
    
    # Accept empty input (Enter) or 'cli' or 'lol' as CLI mode
    if mode in ("", "cli", "lol"):
        cli = FETCli()
        cli.run()
    else:
        print(f"Unknown mode: '{mode}'. Defaulting to CLI...")
        cli = FETCli()
        cli.run()

if __name__ == "__main__":
    main()