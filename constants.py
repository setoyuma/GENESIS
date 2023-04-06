class Actions:
    UP = 119  # w
    DOWN = 115  # s
    BACK = 97  #  a
    FORWARD = 100  # d
    LP = 105  # i
    MP = 111  # o
    HP = 112  # p
    LK = 107  # k
    MK = 108  # l
    HK = 59  # ;

SONGS = [
    "main",
    "egypt",
    "science",
    "q",
    "credits",
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
            "2MK": 5,
            "2HK": 8,
            "JLP": 3,
            "JMP": 5,
        },
        "hitboxes": {
            "0": [0, (0,0,0,0)],
            "LP": [2, (-100, -80, 100, 50)],
            "MP": [2, (-70, -40, 100, 50)],
            "HP": [2, (-70, -40, 100, 50)],
            "LK": [4, (-60, 50, 100, 100)],
            "MK": [3, (-100, -60, 120, 80)],
            "HK": [3, (-100, -160, 80, 100)],
            "2LP": [3, (-60, 0, 100, 50)], 
            "2MP": [3, (-60, 0, 100, 50)], 
            "2HP": [4, (-10, 0, 100, 150)],
            "2LK": [3, (-100, 80, 120, 50)],
            "2MK": [3, (-100, 80, 120, 50)],
            "2HK": [7, (-100, 80, 120, 50)],
            "JLP": [1, (-100, -10, 120, 50)],
            "JMP": [1, (-100, -50, 120, 50)],
        },
        "combos": {
            "LFireball":(Actions.DOWN, Actions.FORWARD, Actions.LP),
            "MFireball":(Actions.DOWN, Actions.FORWARD, Actions.MP),
            "HFireball":(Actions.DOWN, Actions.FORWARD, Actions.HP),

            "LDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.LP),
            "MDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.MP),
            "HDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.HP),
            "EXDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.LP, Actions.MP),

            "FDASH" : (Actions.FORWARD, Actions.FORWARD),
            "BDASH" : (Actions.BACK, Actions.BACK),

            "AXEKICK": (Actions.FORWARD, Actions.MK), 
            "VIGNITION": (Actions.DOWN, Actions.HP),
            
            "SC1":(Actions.MP,Actions.HP),
            "SC2":(Actions.DOWN, Actions.LK, Actions.DOWN, Actions.MK),

            "TCLAW":(Actions.DOWN, Actions.FORWARD, Actions.LP),
            "MCLAW":(Actions.DOWN, Actions.FORWARD, Actions.MP),
            "HCLAW":(Actions.DOWN, Actions.FORWARD, Actions.HP),
            "EXCLAW":(Actions.DOWN, Actions.FORWARD, Actions.LP , Actions.MP),

            "COMETDROP":(Actions.DOWN, Actions.BACK, Actions.LK),
            "MDROP": (Actions.DOWN, Actions.BACK, Actions.MK),
            "HDROP": (Actions.DOWN, Actions.BACK, Actions.HK),
            "EXDROP": (Actions.DOWN, Actions.BACK, Actions.LK , Actions.MK),

            #hyper bomb
            "OGREDROP":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.LP),
            "MBOMB":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.MP),
            "HBOMB":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.HP),
            "EXBOMB":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.MP, Actions.HP),

            "TIGERPOUNCE":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.LK),
            "MPOUNCE":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.MK),
            "HPOUNCE":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.HK),
            "EXPOUNCE":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.MK, Actions.HK),

            "COLDONE":(Actions.DOWN, Actions.DOWN, Actions.LP or Actions.MP or Actions.HP),

            '''SUPERS'''
            "OO":(Actions.FORWARD, Actions.DOWN, Actions.BACK, Actions.UP, Actions.HP),
            "MSP":(Actions.DOWN, Actions.BACK, Actions.DOWN, Actions.BACK, Actions.MK),
            "HELLHAZE":(Actions.DOWN, Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.LP)
        }
    },
    # "Raijin": {

    # }
}

FRAME_DURATIONS = {
    'LP': 0.02,
    'MP': 0.02,
    'HP': 0.02,
    'LK': 0.04,
    'MK': 0.05,
    'HK': 0.06,
    '2LP': 0.03,
    '2MP': 0.04,
    '2HP': 0.06,
    '2LK': 0.04,
    '2MK': 0.05,
    '2HK': 0.03,
    'JLP': 0.03,
    'JMP': 0.03,
    'bg': 0.07,
    'idle': 0.07,
    'run': 0.07,
    'jump': 0.1,
    'crouch': 0.02,
    'hit': 0.08
}

UNUSED_INPUTS = {
    '''FIREBALLS'''
    "LFireball":(Actions.DOWN, Actions.FORWARD, Actions.LP),
    "MFireball":(Actions.DOWN, Actions.FORWARD, Actions.MP),
    "HFireball":(Actions.DOWN, Actions.FORWARD, Actions.HP),

    '''DP's'''
    "LDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.LP),
    "MDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.MP),
    "HDP":(Actions.FORWARD, Actions.DOWN, Actions.FORWARD, Actions.HP),

    '''TATSU'''
    "LTATSU":(Actions.DOWN, Actions.BACK, Actions.LK),
    "MTATSU":(Actions.DOWN, Actions.BACK, Actions.LK),
    "LTATSU":(Actions.DOWN, Actions.BACK, Actions.LK)
}

'''NON-COMBO ACTIONS'''
ATTACKS =  {
       "105" : "LP",
        "111" : "MP",
       "112" : "HP",
        "107" : "LK",
        "108" : "MK",
        "59" : "HK",
    }

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
    '2LK',
    '2MK',
    '2HK',
    'JLP',
    'JMP',
    ]

'''(UN-USED) CHARACTER INPUTS'''
RAIJIN_INPUTS = {
    "THUNDERHAMMER" : (),
    "TIDECRASHER " : (),
    "STORMRING" : (),
    "THUNDERBOLT" : (),
    "LTHUNDERBOLT" : (),
    "MTHUNDERBOLT" : (),
    "HTHUNDERBOLT" : (),
    "EXTHUNDERBOLT" : (),
    "WAVECHASER" : (),
    "LWAVECHASER" : (),
    "MWAVECHASER" : (),
    "HWAVECHASER" : (),
    "EXWAVECHASER" : (),
    "RISINGVOLT" : (),
    "LRISINGVOLT" : (),
    "MRISINGVOLT" : (),
    "HRISINGVOLT" : (),
    "EXRISINGVOLT" : (),
    "DANGEROUSDISCHARGE" : (),
}

INARI_INPUTS = {
    "SPIDERDROP" : (),
    "FOXTROT" : (),
    "LFOXTROT" : (),
    "MFOXTROT" : (),
    "HFOXTROT" : (),
    "EXFOXTROT" : (),
    "FLYINGSWALLOW" : (),
    "LSWALLOW" : (),
    "MSWALLOW" : (),
    "HSWALLOW" : (),
    "EXSWALLOW" : (),
    "SPIDERSCOUTING" : (),
    "KICKOFF" : (),
    "SPIDERDROP" : (),
    "EAGLEWALK" : (),
    "WALLDROP" : (),
    "RISINGKOI" : (),
    "LKOI" : (),
    "MKOI" : (),
    "HKOI" : (),
    "EXKOI" : (),
    "RABBITRETREAT" : (),
    "EAGLEWALK" : (),
    "WILDCATHUNT" : (),
    "LHUNT" : (),
    "MHUNT" : (),
    "HHUNT" : (),
    "EXHUNT" : (),
}