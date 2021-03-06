## GAME DISPLAY

from blaseball_mike.models import Game
from display.general import *

def display_game_results(game):
    """
    Display a game overview similarly to the Blaseball website

    :param game: Game
    :return: ipython Display
    """
    if isinstance(game, list):
        if len(game) > 1:
            raise ValueError("Can only display one game at a time")
        game = game[0]

    if isinstance(game, dict):
        if len(game) > 1:
            raise ValueError("Can only display one game at a time")
        game = list(game.values())[0]

    if not isinstance(game, Game):
        raise ValueError("Game is not a game")

    away_emoji = parse_emoji(game.away_team_emoji)
    home_emoji = parse_emoji(game.home_team_emoji)

    weather_style = ""

    home_back_color = game.home_team_color + "80"
    away_back_color = game.away_team_color + "80"

    if game.shame:
        game_status = "SHAME"
        game_status_style = "background:#800878;"
    elif not game.game_start:
        game_status = "UPCOMING"
        game_status_style = "background:#9a9531;"
    elif game.game_complete:
        game_status = "FINAL"
        if game.inning > 9:
            game_status += f" ({game.inning})"
        game_status_style = "background:red;"
    else:
        top_mark = "▲" if game.top_of_inning else "▼"
        game_status = f"LIVE - {game.inning} {top_mark}"
        game_status_style = "background:green;"

    if len(game.outcomes) > 1:
        outcomes = "</br>".join(game.outcomes)
    elif len(game.outcomes) > 0:
        outcomes = game.outcomes[0]
    else:
        outcomes = ""

    if game.game_complete:
        if game.home_score > game.away_score:
            home_win = "border: 2px solid;"
            away_win = ""
        else:
            away_win = "border: 2px solid;"
            home_win = ""
    else:
        home_win = ""
        away_win = ""

    try:
        away_font_color = game.away_team_secondary_color
        home_font_color = game.home_team_secondary_color
    except AttributeError:
        away_font_color = game.away_team_color
        home_font_color = game.home_team_color


    html = f"""
    <div style="display:flex;flex-direction:column;border-radius:5px;background-color:#111;width:390px;font-size:1rem;font-weight:400;line-height:1.5;color:#fff;box-sizing:border-box;">
        <div style="height:32px;display:flex;justify-content:space-between;flex-direction:row;align-items:center;font-size:14px;background:rgba(30,30,30,.64);border-radius:5px 5px 0 0;">
            <div style=" display:flex;flex-direction:row;height:32px">
                <div style="{game_status_style}display:flex;padding:0 8px;height:100%;border-radius:5px;align-items:center">
                    {game_status}
                </div>
                <div style="{weather_style}display:flex;padding-left:10px;padding-right:10px;height:32px;border-radius:5px;align-items:center;font-size:14px;justify-content:center">
                    {game.weather.text}
                </div>
            </div>
        </div>
        <div style="display:flex;flex:1 0 auto;flex-direction:column;justify-content:space-around;padding:10px 0 10px 10px;">
            <div style="display:grid;grid-template-columns:60px auto 15%;grid-gap:10px;gap:10px;width:100%;align-items:center;padding-bottom:10px;">
                <div style="background:{game.away_team_color};display:flex;width:50px;height:50px;margin-left:8px;border-radius:50%;font-size:29px;justify-content:center;align-items:center;">
                    {away_emoji}
                </div>
                <div style="color:{away_font_color};font-size:24px; font-family:"Lora","Courier New",monospace,serif;">
                    {game.away_team_nickname}
                </div>
                <div style="{away_win}display:flex;font-size:24px;align-items:center;justify-content:center;width:46px;height:46px;margin:0 auto;border-radius:50%;margin:0 8px 0 0;">
                    {game.away_score}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:60px auto 15%;grid-gap:10px;gap:10px;width:100%;align-items:center">
                <div style="background:{game.home_team_color};display:flex;width:50px;height:50px;margin-left:8px;border-radius:50%;font-size:29px;justify-content:center;align-items:center;">
                    {home_emoji}
                </div>
                <div style="color:{home_font_color};font-size:24px; font-family:"Lora","Courier New",monospace,serif;">
                    {game.home_team_nickname}
                </div>
                <div style="{home_win}display:flex;font-size:24px;align-items:center;justify-content:center;width:46px;height:46px;margin:0 auto;border-radius:50%;margin:0 8px 0 0;">
                    {game.home_score}
                </div>
            </div>
            <div style="display:flex;flex-direction:row;align-items:center;justify-content:space-evenly;padding-top:20px;">
                <div style="background:{away_back_color};font-size:14px;align-items:center;line-height:20px;padding:0 8px;margin:5px 0;border-radius:5px;">
                    {game.away_pitcher_name}
                </div>
                <div style="background:{home_back_color};font-size:14px;align-items:center;line-height:20px;padding:0 8px;margin:5px 0;border-radius:5px;">
                    {game.home_pitcher_name}
                </div>
            </div>
            <div style="font-size:12px;line-height:24px;height:100%;text-align:center;padding:5px 0;">
                {outcomes}
            </div>
        </div>
    </div>
    """
    return HTMLWrapper(html)