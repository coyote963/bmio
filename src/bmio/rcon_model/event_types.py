from dataclasses import dataclass, asdict
from typing import Optional

from .rcon_events import RconEvent
from .enemy_types import Enemy, EnemyRank
from .weapon_types import Weapon
from .hat_types import Hat
from .powerup_types import PowerUp
from .vice_types import Vice
from .mission_types import Mission
from .taunt_types import Taunt


@dataclass
class BaseClass:
    Time: str
    EventID: RconEvent

    def asdict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class PlayerProfile:
    ProfileID: str
    StoreID: str

@dataclass
class server_shutdown(BaseClass):
    """Triggers when the server is shutdown."""

@dataclass
class server_startup(BaseClass):
    """"Triggers when the server is started up"""

@dataclass
class lobby_connect(BaseClass):
    """Triggers when the server connects to the server list."""


@dataclass
class lobby_disconnect(BaseClass):
    """Triggers when the server loses connection to the server list."""


@dataclass
class player_connect(BaseClass):
    """Triggers when a new player connects to the server."""
    IP: str
    PlayerName: str
    PlayerID: int
    Profile: PlayerProfile
    IsAdmin: str


@dataclass
class player_spawn(BaseClass):
    """Triggers when a player or NPC respawns. The weapons returned are not always what the player picks in the loadout, depending on when they finish selecting their loadout. You should use player_loadout for handling any loadout weapons."""
    PlayerID: int
    Profile: PlayerProfile
    X: float
    Y: float
    Hat: Hat
    Hat2: Hat
    Name: str
    Color: str
    Team: str
    Weap1: Weapon
    Weap2: Weapon
    Equip: Weapon
    OffWeap: Weapon
    OffWeap2: Weapon
    EnemyType: Optional[Enemy] = None
    EnemyRank: Optional[EnemyRank] = None


@dataclass
class player_death(BaseClass):	
    """Triggers when a player dies."""
    VictimID: str
    KillerID: str
    AssisterID: str
    VictimProfile: PlayerProfile
    AssisterProfile: PlayerProfile
    KillerWeapon: Weapon
    Headshot: bool
    DeathType: str
    Drone: bool
    Teamkill: str
    VictimX: float
    VictimY: float
    KillerX: Optional[float] = None
    KillerY: Optional[float] = None
    KillerProfile: Optional[PlayerProfile] = None
    AssistX: Optional[float] = None
    AssistY: Optional[float] = None


@dataclass
class player_disconnect(BaseClass):
    """Triggers when a player disconnects from the server."""
    IP: str
    PlayerID: int
    Profile: PlayerProfile
    IsAdmin: bool
    Kicked: bool
    KickReason: str


@dataclass
class player_team_change(BaseClass):
    """Triggers when a player changes team."""
    PlayerID: int
    Profile: PlayerProfile
    OldTeam: str
    NewTeam: str
    Autobalanced: bool


@dataclass
class player_level_up(BaseClass):
    """Triggers when a player levels up."""
    PlayerID: int
    Profile: PlayerProfile
    Level: int
    NewWeapon: Weapon
    SkinWeapon: Weapon
    SkinType: str


@dataclass
class player_get_powerup(BaseClass):
    """Triggers when a player gets a power up"""
    PlayerID: int
    Profile: PlayerProfile
    PowerUp: PowerUp
    X: float
    Y: float


@dataclass
class player_damage(BaseClass):
    """Triggers when a player takes damage. DISABLED FOR NOW"""
    AttackerID: int
    VictimID: int
    AttackerProfile: PlayerProfile
    VictimProfile: PlayerProfile
    Headshot: bool
    Damage: int


@dataclass
class player_loaded(BaseClass):
    """Triggers when a player is finished loading their map."""
    PlayerID: int
    Profile: PlayerProfile


@dataclass
class tdm_round_start(BaseClass):
    """Triggers when a Team Deathmatch round starts."""
    Alive1: int
    Alive2: int
    Players1: int
    Players2: int


@dataclass
class tdm_round_end(BaseClass):
    """Triggers when a Team Deathmatch round ends."""
    Players1: int
    Players2: int
    Winner: str
    Score1: int
    Score2: int
    RoundEndType: str
    Flawless: bool


@dataclass
class tdm_flag_unlocked(BaseClass):
    """Triggers when the Team Deathmatch flag unlocks for capture."""
    Alive1: int
    Alive2: int
    Players1: int
    Players2: int
    FlagX: float
    FlagY: float


@dataclass
class tdm_switch_sides(BaseClass):
    """Triggers when the server switches team sides in Team Deathmatch."""
    Score1: int
    Score2: int


@dataclass
class ctf_taken(BaseClass):
    """Triggers when a flag in CTF is stolen."""
    CarrierID: int
    CarrierProfile: PlayerProfile
    FlagTeam: str
    WasHome: bool
    FlagX: float
    FlagY: float


@dataclass
class ctf_dropped(BaseClass):
    """Triggers when a flag in CTF is dropped by a flag carrier."""
    CarrierID: int
    CarrierProfile: PlayerProfile
    FlagTeam: str
    Thrown: bool
    FlagX: float
    FlagY: float


@dataclass
class ctf_returned(BaseClass):
    """Triggers when a flag is returned to home base."""
    ReturnPlayerID: int
    ReturnProfile: PlayerProfile
    ReturnType: str
    FlagX: float
    FlagY: float


@dataclass
class ctf_scored(BaseClass):
    """Triggers when a team scores a point in CTF."""
    CarrierID: int
    CarrierProfile: PlayerProfile
    ScoringTeam: str
    Score1: str
    Score2: str


@dataclass
class ctf_generator_repaired(BaseClass):
    """Triggers when a generator is repaired."""
    ID: str
    Team: str
    RepairerID: str
    RepairerProfile: PlayerProfile


@dataclass
class ctf_generator_destroyed(BaseClass):
    """Triggers when a generator is destroyed."""
    ID: str
    Team: str
    KillerID: str
    KillerProfile: PlayerProfile


@dataclass
class ctf_turret_repaired(BaseClass):
    """Triggers when a turret is repaired."""
    ID: str
    Team: str
    RepairerID: str
    RepairerProfile: PlayerProfile


@dataclass
class ctf_turret_destroyed(BaseClass):
    """Triggers when a turret is destroyed."""
    ID: str
    Team: str
    KillerID: str
    KillerProfile: PlayerProfile


@dataclass
class ctf_resupply_repaired(BaseClass):
    """Triggers when a resupply station is repaired."""
    ID: str
    Team: str
    RepairerID: str
    RepairerProfile: PlayerProfile


@dataclass
class ctf_resupply_destroyed(BaseClass):
    """Triggers when a resupply station is destroyed."""
    ID: str
    Team: str
    KillerID: str
    KillerProfile: PlayerProfile


@dataclass
class match_end(BaseClass):
    """Triggers when the current match ends."""
    WinnerText: str
    WinnerColor: str
    WinnerID: str
    WinnerTeam: str
    GameModeID: str
    NextMapFile: str
    NextMap: str
    PlayerData: str


@dataclass
class match_overtime(BaseClass):
    """Triggers when the match enters over time."""



@dataclass
class match_start(BaseClass):
    """Triggers when a new match starts, does not trigger until warm up phase ends (if there is one)."""
    MapName: str
    MapFile: str
    GameModeID: str
    WorkshopID: str
    MD5: str


@dataclass
class survival_new_wave(BaseClass):
    """Triggers at the start of a new wave in Survival mode."""
    WaveNumber: str
    Enemies: str
    Chests: str
    ChestPrice: str
    ChestCrash: str


@dataclass
class survival_wave_begins(BaseClass):
    """Triggers when the control point flag unlocks for enemies to capture. Turns out this still triggers during Survival Classic or when the prep time is set to 0, will probably changed to save bandwidth."""
    WaveObjective: str
    WaveNumber: str


@dataclass
class survival_buy_chest(BaseClass):
    """Triggers when a player opens a chest."""
    PlayerID: int
    Profile: PlayerProfile
    ChestID: str
    ChestCost: int
    PlayerMoney: int


@dataclass
class log_message(BaseClass):
    """Triggers when a message is logged into the server console."""
    Message: str
    Color: str

@dataclass
class RequestDataBase(BaseClass):
    CaseID: str
    RequestID: str


@dataclass
class request_data_match(RequestDataBase):
    """Triggered when an RCON client makes a request. See below for more documentation on this RCON event."""
    GamemodeName: str
    Team1Score: int
    MaxPlayers: int 
    MaxScore: int
    TimeLeft: int
    TimeStr: str
    Version: str
    Map: str
    MaxTime: int
    ServerName: int
    Team2Score: int
    Players: int
    Overtime: int
    # TODO: make a gamemode enum
    GamemodeID: int
    

@dataclass
class request_data_player(RequestDataBase):
    """Triggered when an RCON client makes a request. See below for more documentation on this RCON event."""
    ID: str
    Name: str
    Color: str
    Team: str
    Kills: int
    Deaths: int
    Assists: int
    Score: int
    Profile: str
    Store: str
    Alive: str
    Bot: str
    Hat: Hat
    Hat2: Hat
    Money: int
    RespawnCost: int
    Premium: str
    
    GamemodeID: str
    X: Optional[int] = None
    Y: Optional[int] = None
    WeaponsDealRank: Optional[str] = None
    ClanID: Optional[str] = None
    ClanTag: Optional[str] = None

    


@dataclass
class command_entered(BaseClass):
    """Triggered when a command is entered into the console."""
    Command: str
    Source: str
    ReturnText: Optional[str] = None


@dataclass
class rcon_logged_in(BaseClass):
    """Triggers when an RCON client successfully logs in."""
    RconIP: str
    RconPort: str
    RconSocket: str
    GameModeID: str
    MapName: str


@dataclass
class match_paused(BaseClass):
    """Triggered when the server is paused."""


@dataclass
class match_unpaused(BaseClass):
    """Triggered when the server is unpaused."""


@dataclass
class warmup_start(BaseClass):
    """Triggered when the warm up phase has begun."""
    WarmupTime: str


@dataclass
class rcon_disconnect(BaseClass):
    """Triggers when an RCON client disconencts."""
    RconIP: str
    RconPort: str
    RconSocket: str


@dataclass
class rcon_ping(BaseClass):
    """Triggers every 5 seconds for each connected RCON client."""


@dataclass
class chat_message(BaseClass):
    """Triggers when a player sends a chat message in the Server tab."""
    PlayerID: int
    Name: str
    Profile: PlayerProfile
    Message: str
    Team: str
    NameColor: str


@dataclass
class survival_get_vice(BaseClass):
    """Triggers when a player collects a vice in Survival mode."""
    PlayerID: int
    Profile: PlayerProfile
    ViceID: Vice
    Amount: int
    X: float
    Y: float


@dataclass
class survival_use_vice(BaseClass):
    """Triggers when a player uses a consumable vice. (Rubbing Alcohol, Smokes, Hot Wings, etc)"""
    PlayerID: int
    Profile: PlayerProfile
    ViceID: Vice


@dataclass
class survival_player_revive(BaseClass):
    """Triggers when a player is revived outside of a new wave starting."""
    RevivingPlayerID: int
    SaviorPlayerID: int
    RevivingProfile: PlayerProfile
    SaviorProfile: PlayerProfile
    Antacids: str
    Cost: int


@dataclass
class player_taunt(BaseClass):
    """Triggers when a player uses a emote, such as /drink or /smoke"""
    PlayerID: int
    Profile: PlayerProfile
    TauntID: Taunt


@dataclass
class survival_complete_mission(BaseClass):
    """Triggered when a player completes a mission from the bar in Survival."""
    PlayerID: int
    Profile: PlayerProfile
    Amount: int
    Vice: Vice
    Type: Mission


@dataclass
class survival_take_mission(BaseClass):
    """Triggered when a player accepts a mission from the bar in Survival."""
    PlayerID: int
    Profile: PlayerProfile
    Amount: int
    Vice: Vice
    Type: Mission


@dataclass
class survival_fail_mission(BaseClass):
    """Triggered when a player fails or abandons a mission from the bar in Survival."""
    PlayerID: int
    Profile: PlayerProfile
    Amount: int
    Vice: Vice
    Type: Mission


@dataclass
class zombrains_revive(BaseClass):
    """"""

@dataclass
class Triggered(BaseClass):
    """zombie player revives from killing players (or through console command)"""
    PlayerID: int
    Profile: PlayerProfile


@dataclass
class zombrains_buy_weapon(BaseClass):
    """Triggered when a player buys a weapon from a weapon printer."""
    PlayerID: int
    Profile: PlayerProfile
    Weapon: Weapon
    Cost: int


@dataclass
class zombrains_begin(BaseClass):
    """Triggered when the match starts in Zombrains."""


@dataclass
class zombrains_helicopter_arriving(BaseClass):
    """Triggered when the helicopter spawns to pick up the surviving humans in Zombrains."""
    LandingX: float
    LandingY: float


@dataclass
class zombrains_helicopter_boarding(BaseClass):
    """Triggered when the helicopter reaches the landing zone and is accepting human players to board in Zombrains/
    The helicopter doesn't always stop exactly at the coordinates reported in the zombrains_helicopter_arriving event, 
    so thats why its position is recorded here as well."""
    X: float
    Y: float


@dataclass
class zombrains_helicopter_player_boarded(BaseClass):
    """Triggered when a human player boards the helicopter in Zombrains."""
    PlayerID: int
    Profile: PlayerProfile


@dataclass
class zombrains_end(BaseClass):
    """Triggered when the Zombrains match ends.
    The zombies win if "Alive" returns as "0", the humans win if "Alive" is anything higher then "0"."""
    Alive: int
    Dead: int


@dataclass
class game_over(BaseClass):
    """Triggered the very same frame the game has ended. More precise then the match_end RCON event, but does not include PlayerData."""
    WinnerText: str
    WinnerColor: str
    WinnerID: int
    WinnerTeam: str
    GameModeID: str
    CurrentMapName: str
    CurrentMapFile: str


@dataclass
class server_empty(BaseClass):
    """Triggered when the last human player (except the host player) has quit. You can check if the server is literally empty by checking that the 'Bots' and 'Host' key both return '0'."""
    Bots: int
    Host: bool


@dataclass
class weaponsdeal_rankchange(BaseClass):
    """Triggered when a player ranks up or down in Weapons Deal and gets a new weapon. I guess I should add the weapon ID too at some point."""
    PlayerID: int
    Profile: PlayerProfile
    WeaponsDealRank: str


@dataclass
class takeover_flagcapture(BaseClass):
    """Triggered when a team caps a flag in Take Over."""
    FlagID: str
    FlagX: float
    FlagY: float
    NewOwner: str
    LastOwner: str
    FlagsTeamOne: str
    FlagsTeamTwo: str


@dataclass
class takeover_flagscreated(BaseClass):
    """Triggered when the match starts in Take Over, or when the flags are randomly cycled."""
    FlagAmount: int
    Team1Score: str
    Team2Score: str
    FlagData: str
    FlagID: str
    FlagX: float
    FlagY: float


@dataclass
class player_loadout(BaseClass):
    """Triggered when a player finishes using the load out menu. This is similar to player_spawn, but sometimes players do not select their loadout until after they spawn."""
    PlayerID: int
    Profile: PlayerProfile
    Weap1: Weapon
    Weap2: Weapon
    Dualwield: str
    Equip: Weapon
    OffWeap: Weapon
    OffWeap2: Weapon


@dataclass
class survival_bomb_defused(BaseClass):
    """Triggered when a bomb is defused in Survival."""
    TimeLeft: str
    Defuser: str


@dataclass
class survival_bomb_exploded(BaseClass):
    """Triggered when a bomb explodes in Survival and ends the match. This event will trigger before any of the match ending RCON events are triggered."""


@dataclass
class survival_bomb_rearmed(BaseClass):
    """Triggered when Bomb Dude, Demolitions Guy, Operator or EXPLODEBOT 5000 re-arm a defused bomb."""
    TimeLeft: str


@dataclass
class sleep(BaseClass): 
    """the dedicated server falls sleep to save power."""

