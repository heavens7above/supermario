import asyncio
import sys
from .game import Game

def main():
    game = Game()
    # In a real async environment (like pyodide or robust event loops), 
    # we might strictly use asyncio.run. 
    # For compatibility, we'll stick to our async run pattern.
    try:
        asyncio.run(game.run())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Game crashed: {e}")

if __name__ == "__main__":
    main()
