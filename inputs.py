from settings import *

UnusedInputs = {
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

}

Subi_Inputs = {
        "LFireball":(DOWN, FORWARD, LP),
        "MFireball":(DOWN, FORWARD, MP),
        "HFireball":(DOWN, FORWARD, HP),

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

    }

Raijin_Inputs = {
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


# Inputs = {
#             "Homusubi" : Subi_Inputs,
#             "Raijin" : Raijin_Inputs,
            
#         }


