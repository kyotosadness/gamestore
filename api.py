from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Game(BaseModel):
    id: int
    title: str
    price: float
    genre: str


games_db = [
    {"id": 1, "title": "The Witcher 3", "price": 29.99, "genre": "RPG"},
    {"id": 2, "title": "Cyberpunk 2077", "price": 49.99, "genre": "RPG"},
    {"id": 3, "title": "FIFA 23", "price": 59.99, "genre": "Sports"},
    {"id": 4, "title": "Call of Duty: Warzone", "price": 0.00, "genre": "FPS"},
]


@app.get("/games", response_model=List[Game])
async def get_games():
    return games_db


@app.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: int):
    for game in games_db:
        if game["id"] == game_id:
            return game
    raise HTTPException(status_code=404, detail="Game not found")


@app.post("/games", response_model=Game)
async def add_game(game: Game):
    games_db.append(game.dict())
    return game

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)