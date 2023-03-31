import pygame as pg
pg.font.init()

def load_settings(self):
    reader = open('settings.json', 'r')
    settings = json.loads(reader.read())
    return(settings)


'''FONT'''
FONT = pg.font.Font("assets/ui/font/minotaur.ttf", 30)

'''FIGHTER SCALES'''
FIGHTER_SCALES = {
    1: 1,
}

'''ATTACKS'''
ATTACKS = {

    "HIT_BOXES" : {
        "Homusubi": {
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
        }
    },

    "SUBI_INPUTS" : {
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
        "HELLHAZE":(DOWN, FORWARD, DOWN, FORWARD, LP),

    },

    "UNUSED_INPUTS" : {
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
        "LTATSU":(DOWN, BACK, LK),

    },


}

'''RESOLUTION'''
HALF_SCREENW = self.settings["screen_width"]//2
HALF_SCREENH = self.settings["screen_height"]//2
QUARTER_SCREENW = self.settings["screen_width"]//4
QUARTER_SCREENH = self.settings["screen_width"]//4

'''MOVEMENT'''
UP = pg.K_w
DOWN = pg.K_s
BACK = pg.K_a
FORWARD = pg.K_d

'''NORMAL ATTACKS'''
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

HOMUSUBI = {
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

}

CHAR_DAMAGE = {
    "Homusubi": HOMUSUBI,
}

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