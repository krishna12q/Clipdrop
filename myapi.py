from fastapi import FastAPI, Path, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import json
from fastapi.staticfiles import StaticFiles
import psycopg2
import time
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

with open("commands.json", "r") as f:
    commands = json.load(f)

templates = Jinja2Templates(directory="templates")


# FASTAPI by default runs on json data structure

players = {

    "kraken": {
        "coins": 1200,
        "firewall": 2,
        "miner_level": 2
    },

    "cipher": {
        "coins": 2500,
        "firewall": 4,
        "miner_level": 3
    },

    "wraith": {
        "coins": 800,
        "firewall": 1,
        "miner_level": 1
    },

    "nullbyte": {
        "coins": 4000,
        "firewall": 7,
        "miner_level": 5
    }
}

students = {
    1: {
        "name": "jhon cena",
        "age": 67,
        "grade": "Year 12"
    }
}

gamestate = {
    "player": {
        "alias": "Ghost",
        "coins": 500,
        "miner_level": 1,
        "firewall": 1,
        "cps": 20,
        "last_collect": time.time(),
        "defencelvl":1,
        "nuke":False,
        "atklvl":1
    },
    "pending_action":False
}

class Command(BaseModel):
    command: str

def upgraded_miner():

    upg_cost = gamestate["player"]["cps"] * 6 + 70

    if gamestate["player"]["coins"] < upg_cost:
        return {
            "action": "print",
            "output":
            f"\nNext Upgrade Costs {upg_cost} B$,You Dont Have Enough\n"
        }

    gamestate["player"]["coins"] -= upg_cost

    gamestate["player"]["miner_level"] += 1

    gamestate["player"]["cps"] = int(
        gamestate["player"]["cps"] * 1.8
    )

    return {
        "action": "print",
        "output":
        f"\nMiner Upgraded\n"
        f"Level: {gamestate['player']['miner_level']}\n"
        f"CPS: {gamestate['player']['cps']}\n"
    }


def use_nuke():

    if gamestate["player"]["nuke"] == True:
        gamestate["pending_action"] = {
            "type":"nuke"
        }  

        return {
            "action":"print",
            "output":"\nLaunch Cyber-Incinerator Mk V\nTHIS ACTION CANNOT BE UNDONE\nConfirm [Y/N]\n"
        }
    else:
        return {
            "action":"print",
            "output":"\nYou Don't Own A Nuke, Buy One First\n"
        }

def attack(port, target):

    target = target.lower()

    if target not in players:
        return {
            "action": "error",
            "output": f"Target '{target}' not found"
        }

    defence = 35 + (5 * players[target]["firewall"])
    atk = random.randint(0, 100) + gamestate["player"]["atklvl"] * 5

    if atk >= defence:

        reward = random.randint(100, 512)

        reward = min(reward, players[target]["coins"])

        players[target]["coins"] -= reward
        gamestate["player"]["coins"] += reward

        return {
            "action": "print",
            "show_progress": True,
            "output": f"Successfully cooked {target} at port {port}, and stole {reward} Bitcoins with level {gamestate['player']['atklvl']} attacker"
        }

    return {
        "action": "print",
        "show_progress": True,
        "output": "Attack Failed"
    }

def cls():
    return {
    "action": "clear_screen"
}

def help_cmd():

    output = (
        "NETBREACH COMMAND DATABASE\n"
        "==========================\n\n"
    )

    for name, info in commands.items():

        output += (
            f"[{name.upper()}]\n"
            f"  Args  : {info['args']}\n"
            f"  Usage : {info['usage']}\n\n"
        )

    return {
        "action": "print",
        "output": output
    }

def wallet():
    return {
        "action": "print",
        "output": f"Total {gamestate['player']['coins']} BCoins\nNuke Owned : {gamestate['player']['nuke']}"
    }

def miner():

    collectable = get_collectable_coins()
    next_upgrade = gamestate["player"]["cps"] * 6 + 70

    return {
        "action": "print",
        "output":
        f"""
Bitcoin Miner
-------------
Level              : {gamestate['player']['miner_level']}
Coins Per Second   : {gamestate['player']['cps']}
Coins To Collect   : {collectable}
Next Upgrade Cost  : {next_upgrade}
"""
    }

def get_collectable_coins():

    now = time.time()

    elapsed = now - gamestate["player"]["last_collect"]

    return int(
    elapsed *
    gamestate["player"]["cps"]
)

def collect():

    collectable = get_collectable_coins()

    gamestate["player"]["coins"] += collectable

    gamestate["player"]["last_collect"] = time.time()

    return {
        "action": "print",
        "output":
        f"Collected {collectable} BCoins"
    }

def leaderboard():

    output = "\n     LEADERBOARD\n"
    output += "======================\n"

    for player in players:
        output += f"\n{player} : {players[player]['coins']} BCoins"

    return {
        "action": "print",
        "output": output+"\n"
    }

def win():
    return ""

def nuke_used():
    
    gamestate["player"]['nuke'] = False

    win()

    return {
            "action": "print",
            "output": "\nNETWORK NUKE LAUNCHED 💀\n"
        }

def confirm_action():

    action =  gamestate["pending_action"]

    gamestate['pending_action'] = None

    if action["type"] == "buy_nuke":

        return bought_nuke()

    if action["type"] == "nuke":

        return nuke_used()
    
    if action["type"] == "buy_next_atk":

        return upgraded_atk()
    
    if action["type"] == "buy_next_miner":

        return upgraded_miner()
    
    
def parse_command(command,arg1,arg2):
    if command.lower() == "atk":
        port = arg2
        target = arg1
        return attack(port,target)

    elif command.lower() == "cls":
        return cls()
    
    elif command.lower() == "help":
        return help_cmd()
    
    elif command.lower() == "miner":
        return miner()
    
    elif command.lower() == "wallet":
        return wallet()

    elif command.lower() == "leaderboard":
        return leaderboard()
    
    elif command.lower() == "collect":
        return collect()
    
    elif command.lower() == "use_nuke":
        return use_nuke()
    
    elif command.lower() == "buy_nuke":
        return buy_nuke()
        
    elif command.lower() == "upgrade_miner":
        return miner_prompt()

    elif command.lower() == "upgrade_firewall":
        return firewall_prompt()
    
    elif command.lower() == "shop":
        return shop()
    
    elif command.lower() == "upgrade_attacker":
        return upgrade_attack_prompt()

def buy_nuke():

    if gamestate["player"]["coins"] >= 5000:
        gamestate["pending_action"] = {
            "type":"buy_nuke"
        }

        return {
            "action":"print",
            "output":"\nBuy Nuke\nCost: 5000 B$\nConfirm [Y/N]\n"
        }
    
    else:
        return {
            "action":"print",
            "output":"\nYou Require Atleast 5k B$ to buy a nuke\n"
        }

def bought_nuke():
    gamestate["player"]["nuke"] = True
    gamestate["player"]['coins'] -= 5000
    return {
        "action":"print",
        "output":"\nBought Nuke\n"
    }
   
def upgrade_attack_prompt():

    upgcost = gamestate["player"]["atklvl"] * 20 * 6 + 70


    gamestate["pending_action"] = {
            "type":"buy_next_atk"
        }

    return {
            "action":"print",
            "output":f"\nNext Upgrade\nCost: {upgcost} B$\nDo you want to buy [Y/N]\n"
        }
    
    
def upgraded_atk():

    cost = gamestate["player"]["atklvl"] * 20 * 6 + 70

    gamestate['player']['coins'] -= cost

    gamestate['player']['atklvl'] += 1

    return {
        "action": "print",
        "output":
            f"\nAttacker Upgraded\n"
            f"Level : {gamestate['player']['atklvl']}\n"
    }

def shop():
    return {
        "action": "print",
        "output":
            f"\nBLACK MARKET\n\n1. Upgrade Miner - {gamestate["player"]["cps"] * 6 + 70} B$\n2. Upgrade Defence - {gamestate["player"]["defencelvl"] * 20 * 6 + 70} B$\n3. Upgrade Attacker - {gamestate["player"]["atklvl"] * 20 * 6 + 70} B$\n4. Buy Nuke - 5000 B$\n"
    }

def firewall_prompt():
    upgcost = gamestate["player"]["defencelvl"] * 20 * 6 + 70

    gamestate["pending_action"] = {
            "type":"buy_next_firewall"
        }

    return {
            "action":"print",
            "output":f"\nNext Upgrade\nCost: {upgcost} B$\nDo you want to buy [Y/N]\n"
        }


def miner_prompt():
    upgcost = gamestate["player"]["miner_level"] * 20 * 6 + 70

    gamestate["pending_action"] = {
            "type":"buy_next_miner"
        }

    return {
            "action":"print",
            "output":f"\nNext Upgrade\nCost: {upgcost} B$\nDo you want to buy [Y/N]\n"
        }


def upg_frwl():
    cost = gamestate["player"]["firewall"] * 20 * 6 + 70

    gamestate['player']['coins'] -= cost

    gamestate['player']['firewall'] += 1

    return {
        "action": "print",
        "output":
            f"\nFirewall Upgraded\n"
            f"Level : {gamestate['player']['firewall']}\n"
    }

@app.post("/parse")
async def parse(cmd: Command):
    wordbyword = cmd.command.strip().split()

    if not wordbyword:
        return {
            "action":"print",
            "output":"ERR : No command entered"
        }

    command = wordbyword[0].lower()
    args = wordbyword[1:]

    if gamestate["pending_action"]:
         
        answer = command.lower()

        if answer == "y":
            return confirm_action()
        elif answer == "n":
            gamestate["pending_action"] = None

            return {
                "action": "print",
                "output": "Cancelled"
            }
        else:
            return {
                "action": "print",
                "output": "Unidentified Option"
            }

    if command not in commands:
        return {
            "action":"print",
            "output":"ERR : No such command found in netbreach --db"
        }

    expected_args = commands[command]["args"]

    if len(args) != expected_args:
        return {
            "Error": f"Usage: {commands[command]['usage']}"
        }

    arg1 = args[0] if len(args) > 0 else None
    arg2 = args[1] if len(args) > 1 else None

    return parse_command(command, arg1, arg2)


























































class student(BaseModel):
    name: str
    age: int
    grade: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "name": "Krishna"
        }
    )



# GET

# @app.get("/")
# def index():
#    return {"name": "First Data"}


# PATH PARAMETER

@app.get("/get-student/{student_id}")
def find_student(
    student_id: int = Path(
        ...,
        description="The ID Student To Be Viewed",
        gt=0,
        lt=30
    )
):
    # ... means required parameter
    # gt = greater than
    # lt = lesser than
    # le = lesser or equal
    # ge = greater or equal
    # PATH IS USED WHENEVER WE NEED TO PROCESS SMTG DYNAMICALLY

    if student_id not in students:
        return {"Error": "Student Not Found"}

    return students[student_id]


# QUERY PARAMETER

# EG - google.com/results?search=Python
# Basically like PATH PARAMETER

@app.get("/get-by-name")
def get_student(
    *,
    name: Optional[str] = None,
    test: int
):
    # None only works sometimes but its used to show not required
    # Optional always before required

    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]

    return {"Data": "Not Found"}


# Request Body And Post Method

@app.post("/create-student/{student_id}")
def create(student_id: int, student: student):
    if student_id in students:
        return {"Error": "ID is taken"}

    students[student_id] = student.model_dump()

    return students[student_id]


# PUT

@app.put("/update_student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):

    if student_id not in students:
        return {"Error": "No Student Found"}

    if student.name is not None:
        students[student_id]["name"] = student.name

    if student.age is not None:
        students[student_id]["age"] = student.age

    if student.grade is not None:
        students[student_id]["grade"] = student.grade

    return students[student_id]

# DELETE

@app.delete("/delete-student/{student_id}")
def del_student(student_id:int , student: student):
    if students[student_id] not in students:
        return {"Error":"Item Not Found"}
    
    del students[student_id]
    return {"Message":"Student Deleted Succsessfully"}