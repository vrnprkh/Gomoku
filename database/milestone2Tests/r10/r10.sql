
/*

User creates lobby
    -> add new row in Games (gid, uid1)
    -> [TRIGGER] add new row in Lobbies (gid, uid1, open = true)

User joins lobby
    -> update Lobbies (update uid2)
    -> [TRIGGER] update Games (update uid2) and update Lobby (update open = false)

Game Ends
    -> Update Games (update final_game_state, result, start_time)
    -> Add to Detailed_Moves (insert row for each move in game)
    -> Update User Stats
    -> 

*/

