SONGS = [
    "main"
    "egypt"
    "science"
    "q"
    "credits"
]

BACKGROUNDS = {
    "carnival" : "bay-side-carnival",
    "ogre" : "ogre-gate"
}

FIGHTER_DATA = {
    "Homusubi": {
        "max hp": 200,
        "size": 350,
        "scale": 1,
        "damage": {
            "LP": 3,
            "MP": 6,
            "HP": 10,
            "LK": 4,
            "MK": 8,
            "HK": 15,
            "2LP": 4,
            "2MP": 8,
            "2HP": 15,
            "2LK": 5,
        },
        "hitboxes": {
            "0": [0, (0,0,0,0)],
            "1": [2, (-40, -80, 100, 50)],  #LP
            "2": [2, (-10, -40, 100, 50)],  #MP
            "3": [2, (-10, -40, 100, 50)],  #HP
            "4": [4, (0, 50, 100, 100)],  #LK
            "5": [3, (-40, -60, 120, 80)],  #MK
            "6": [3, (-40, -160, 80, 100)],  #HK
            "7": [2, (0, 0, 100, 50)],  #2LP
            "8": [2, (0, 0, 100, 50)],  #2MP
            "9": [2, (50, 0, 100, 150)],  #2HP
            "10": [2, (50, 0, 100, 150)],  #2HP
        },
        "combos": {
            "LFireball":(DOWN, FORWARD, LP),
            "MFireball":(DOWN, FORWARD, MP),
            "HFireball":(DOWN, FORWARD, HP),

            "LDP":(FORWARD, DOWN, FORWARD, LP),
            "MDP":(FORWARD, DOWN, FORWARD, MP),
            "HDP":(FORWARD, DOWN, FORWARD, HP),
            "EXDP":(FORWARD, DOWN, FORWARD, LP, MP),

            "FDASH" : (FORWARD, FORWARD),
            "BDASH" : (BACK, BACK),

            "AXEKICK": (FORWARD, MK), 
            "VIGNITION": (DOWN, HP),
            
            "SC1":(MP,HP),
            "SC2":(DOWN,LK, DOWN,MK),

            "TCLAW":(DOWN, FORWARD, LP),
            "MCLAW":(DOWN, FORWARD, MP),
            "HCLAW":(DOWN, FORWARD, HP),
            "EXCLAW":(DOWN, FORWARD, LP , MP),

            "COMETDROP":(DOWN, BACK, LK),
            "MDROP": (DOWN, BACK, MK),
            "HDROP": (DOWN, BACK, HK),
            "EXDROP": (DOWN, BACK, LK ,MK),

            #hyper bomb
            "OGREDROP":(FORWARD, DOWN, BACK, LP),
            "MBOMB":(FORWARD, DOWN, BACK, MP),
            "HBOMB":(FORWARD, DOWN, BACK, HP),
            "EXBOMB":(FORWARD, DOWN, BACK, MP, HP),

            "TIGERPOUNCE":(FORWARD, DOWN, BACK, LK),
            "MPOUNCE":(FORWARD, DOWN, BACK, MK),
            "HPOUNCE":(FORWARD, DOWN, BACK, HK),
            "EXPOUNCE":(FORWARD, DOWN, BACK, MK, HK),

            "COLDONE":(DOWN, DOWN, LP or MP or HP),

            '''SUPERS'''
            "OO":(FORWARD, DOWN, BACK, UP, HP),
            "MSP":(DOWN, BACK, DOWN, BACK, MK),
            "HELLHAZE":(DOWN, FORWARD, DOWN, FORWARD, LP)
        }
    },
    "Raijin": {

    }
}

ANIMATION_SPEEDS = {
    'LP': 0.2,
    'MP': 0.1,
    'HP': 0.2,
    'LK': 0.2,
    'MK': 0.2,
    'HK': 0.2,
    '2LP': 0.4,
    '2MP': 0.1,
    '2HP': 0.1,
    '2LK': 0.2,
    'bg': 0.2,
    'idle': 0.2
}

UNUSED_INPUTS = {
    '''FIREBALLS'''
    "LFireball":(DOWN, FORWARD, LP),
    "MFireball":(DOWN, FORWARD, MP),
    "HFireball":(DOWN, FORWARD, HP),

    '''DP's'''
    "LDP":(FORWARD, DOWN, FORWARD, LP),
    "MDP":(FORWARD, DOWN, FORWARD, MP),
    "HDP":(FORWARD, DOWN, FORWARD, HP),

    '''TATSU'''
    "LTATSU":(DOWN, BACK, LK),
    "MTATSU":(DOWN, BACK, LK),
    "LTATSU":(DOWN, BACK, LK)
}

'''ACTIONS'''
UP = pg.K_w
DOWN = pg.K_s
BACK = pg.K_a
FORWARD = pg.K_d
LP = pg.K_i
MP = pg.K_o
HP = pg.K_p
LK = pg.K_k
MK = pg.K_l
HK = pg.K_SEMICOLON

'''NON-COMBO ACTIONS'''
ACTIONS = [
    'LP',
    'MP',
    'HP',
    'LK',
    'MK',
    'HK',
    '2LP',
    '2MP',
    '2HP',
    '2LK'
    'FDASH'
    'BDASH'
    ]

'''(UN-USED) CHARACTER INPUTS'''
RAIJIN_INPUTS = {
   (): "THUNDERHAMMER",
   (): "TIDECRASHER ",
   (): "STORMRING",
   (): "THUNDERBOLT",
   (): "LTHUNDERBOLT",
   (): "MTHUNDERBOLT",
   (): "HTHUNDERBOLT",
   (): "EXTHUNDERBOLT",
   (): "WAVECHASER",
   (): "LWAVECHASER",
   (): "MWAVECHASER",
   (): "HWAVECHASER",
   (): "EXWAVECHASER",
   (): "RISINGVOLT",
   (): "LRISINGVOLT",
   (): "MRISINGVOLT",
   (): "HRISINGVOLT",
   (): "EXRISINGVOLT",
   (): "DANGEROUSDISCHARGE",


   (): "SPIDERDROP",
   (): "FOXTROT",
   (): "LFOXTROT",
   (): "MFOXTROT",
   (): "HFOXTROT",
   (): "EXFOXTROT",
   (): "FLYINGSWALLOW",
   (): "LSWALLOW",
   (): "MSWALLOW",
   (): "HSWALLOW",
   (): "EXSWALLOW",
   (): "SPIDERSCOUTING",
   (): "KICKOFF",
   (): "SPIDERDROP",
   (): "EAGLEWALK",
   (): "WALLDROP",
   (): "RISINGKOI",
   (): "LKOI",
   (): "MKOI",
   (): "HKOI",
   (): "EXKOI",
   (): "RABBITRETREAT",
   (): "EAGLEWALK",
   (): "WILDCATHUNT",
   (): "LHUNT",
   (): "MHUNT",
   (): "HHUNT",
   (): "EXHUNT",
}