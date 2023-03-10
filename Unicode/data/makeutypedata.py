import enum


class Pose(enum.IntFlag):
    ABOVE = 0x100
    BELOW = 0x200
    OVERSTRIKE = 0x400
    LEFT = 0x800
    RIGHT = 0x1000
    JOINS2 = 0x2000
    CENTERLEFT = 0x4000
    CENTERRIGHT = 0x8000
    CENTEREDOUTSIDE = 0x10000
    OUTSIDE = 0x20000
    RIGHTEDGE = 0x40000
    LEFTEDGE = 0x80000
    TOUCHING = 0x100000


def map_canonical_combining_class(ccc: int) -> Pose:
    if ccc == 1:  # Overlay
        return Pose.OVERSTRIKE
    elif ccc == 200:  # Attached_Below_Left
        return Pose.BELOW | Pose.LEFT | Pose.TOUCHING
    elif ccc == 202:  # Attached_Below
        return Pose.BELOW | Pose.TOUCHING
    elif ccc == 204:  # Attached_Below_Right
        return Pose.BELOW | Pose.RIGHT | Pose.TOUCHING
    elif ccc == 208:  # Attached_Left
        return Pose.LEFT | Pose.TOUCHING
    elif ccc == 210:  # Attached_Right
        return Pose.RIGHT | Pose.TOUCHING
    elif ccc == 212:  # Attached_Above_Left
        return Pose.ABOVE | Pose.LEFT | Pose.TOUCHING
    elif ccc == 214:  # Attached_Above
        return Pose.ABOVE | Pose.TOUCHING
    elif ccc == 216:  # Attached_Above_Right
        return Pose.ABOVE | Pose.RIGHT | Pose.TOUCHING
    elif ccc == 218:  # Below_Left
        return Pose.BELOW | Pose.LEFT
    elif ccc == 220:  # Below
        return Pose.BELOW
    elif ccc == 222:  # Below_Right
        return Pose.BELOW | Pose.RIGHT
    elif ccc == 224:  # Left
        return Pose.LEFT
    elif ccc == 226:  # Right
        return Pose.RIGHT
    elif ccc == 228:  # Above_Left
        return Pose.ABOVE | Pose.LEFT
    elif ccc == 230:  # Above
        return Pose.ABOVE
    elif ccc == 232:  # Above_Right
        return Pose.ABOVE | Pose.RIGHT
    elif ccc == 233:  # Double_Below
        return Pose.BELOW | Pose.JOINS2
    elif ccc == 234:  # Double_Above
        return Pose.ABOVE | Pose.JOINS2

    # Leave it up to the overrides
    return Pose(0)


def get_pose(char: int, ccc: int, with_ccc: bool = False) -> Pose:
    pose = MANUAL_POSES.get(char, map_canonical_combining_class(ccc))
    if with_ccc:
        return pose | (ccc & 0xFF)
    return pose


# These non-normative decompositions allow display algorithms to
# pick something that looks right, even if the character doesn't mean
# what it should. For example Alpha LOOKS LIKE A so if we don't have
# an Alpha character available we can draw it with an A. But this decomp
# is not normative and should not be used for ordering purposes
VISUAL_ALTS = {
    #  ligatures
    #  I don't bother with AE, ae because they are in latin1 and so common
    0x152: [0x4F, 0x45],  # ?? -> OE
    0x153: [0x6F, 0x65],  # ?? -> oe
    #  Things which look alike to my eyes
    0x110: [0xD0],  # ?? -> ??
    0x138: [0x3BA],  # ?? -> ??
    0x182: [0x402],  # ?? -> ??
    0x189: [0xD0],  # ?? -> ??
    0x19E: [0x3B7],  # ?? -> ??
    0x19F: [0x398],  # ?? -> ??
    0x1A9: [0x3A3],  # ?? -> ??
    0x1C0: [0x7C],  # ?? -> |
    0x1C1: [0x7C, 0x7C],  # ?? -> ||
    0x269: [0x3B9],  # ?? -> ??
    #  IPA
    0x278: [0x3A6],  # ?? -> ??
    0x299: [0x432],  # ?? -> ??
    0x292: [0x1B7],  # ?? -> ??
    0x29C: [0x43D],  # ?? -> ??
    0x2B9: [0x27],  # ?? -> '
    0x2BA: [0x22],  # ?? -> "
    0x2BC: [0x27],  # ?? -> '
    0x2C4: [0x5E],  # ?? -> ^
    0x2C6: [0x5E],  # ?? -> ^
    0x2C8: [0x27],  # ?? -> '
    # 0x2DC: [0x7E],  # ?? -> ~
    # 0x2E0: [0x263],  # ?? -> ??
    # 0x2E1: [0x6C],  # ?? -> l
    # 0x2E2: [0x73],  # ?? -> s
    # 0x2E3: [0x78],  # ?? -> x
    # 0x2E4: [0x2E4],  # ?? -> ??
    0x301: [0xB4],  # ?? -> ??
    0x302: [0x5E],  # ?? -> ^
    0x303: [0x7E],  # ?? -> ~
    0x308: [0xA8],  # ?? -> ??
    0x30A: [0xB0],  # ?? -> ??
    0x30B: [0x22],  # ?? -> "
    0x30E: [0x22],  # ?? -> "
    0x327: [0xB8],  # ?? -> ??
    #  Greek
    # 0x374: [0x27],  # ?? -> '
    0x375: [0x2CF],  # ?? -> ??
    # 0x37A: [0x345],  # ?? -> ??
    # 0x37E: [0x3B],  # ?? -> ;
    0x391: [0x41],  # ?? -> A
    0x392: [0x42],  # ?? -> B
    0x393: [0x413],  # ?? -> ??
    0x395: [0x45],  # ?? -> E
    0x396: [0x5A],  # ?? -> Z
    0x397: [0x48],  # ?? -> H
    0x399: [0x49],  # ?? -> I
    0x39A: [0x4B],  # ?? -> K
    0x39C: [0x4D],  # ?? -> M
    0x39D: [0x4E],  # ?? -> N
    0x39F: [0x4F],  # ?? -> O
    0x3A1: [0x50],  # ?? -> P
    0x3A4: [0x54],  # ?? -> T
    0x3A5: [0x59],  # ?? -> Y
    0x3A7: [0x58],  # ?? -> X
    0x3BA: [0x138],  # ?? -> ??
    0x3BF: [0x6F],  # ?? -> o
    0x3C1: [0x70],  # ?? -> p
    0x3C7: [0x78],  # ?? -> x
    #  Cyrillic
    0x405: [0x53],  # ?? -> S
    0x406: [0x49],  # ?? -> I
    0x408: [0x4A],  # ?? -> J
    0x410: [0x41],  # ?? -> A
    0x412: [0x42],  # ?? -> B
    0x413: [0x393],  # ?? -> ??
    0x415: [0x45],  # ?? -> E
    0x41A: [0x4B],  # ?? -> K
    0x41C: [0x4D],  # ?? -> M
    0x41D: [0x48],  # ?? -> H
    0x41E: [0x4F],  # ?? -> O
    0x41F: [0x3A0],  # ?? -> ??
    0x420: [0x50],  # ?? -> P
    0x421: [0x43],  # ?? -> C
    0x422: [0x54],  # ?? -> T
    0x424: [0x3A6],  # ?? -> ??
    0x425: [0x58],  # ?? -> X
    0x430: [0x61],  # ?? -> a
    0x435: [0x65],  # ?? -> e
    0x43A: [0x3BA],  # ?? -> ??
    0x43E: [0x6F],  # ?? -> o
    0x43F: [0x3C0],  #  Not quite right, but close # ?? -> ??
    0x440: [0x70],  # ?? -> p
    0x441: [0x63],  # ?? -> c
    0x443: [0x79],  # ?? -> y
    0x445: [0x78],  # ?? -> x
    0x455: [0x73],  # ?? -> s
    0x456: [0x69],  # ?? -> i
    0x458: [0x6A],  # ?? -> j
    #  extended Cyrillic
    0x470: [0x3A8],  # ?? -> ??
    0x471: [0x3C8],  # ?? -> ??
    0x4AE: [0x59],  # ?? -> Y
    0x4C0: [0x49],  # ?? -> I
    0x4D4: [0xC6],  # ?? -> ??
    0x4D5: [0xE6],  # ?? -> ??
    0x4E0: [0x1B7],  # ?? -> ??
    0x4E1: [0x292],  # ?? -> ??
    0x4E8: [0x398],  # ?? -> ??
    0x4E9: [0x3B8],  # ?? -> ??
    #  Armenian
    0x54F: [0x53],  # ?? -> S
    0x555: [0x4F],  # ?? -> O
    0x570: [0x68],  # ?? -> h
    0x578: [0x6E],  # ?? -> n
    0x57A: [0x270],  # ?? -> ??
    0x57D: [0x75],  # ?? -> u
    0x581: [0x261],  # ?? -> ??
    0x582: [0x269],  # ?? -> ??
    0x584: [0x66],  # ?? -> f
    0x585: [0x6F],  # ?? -> o
    0x589: [0x3A],  # ?? -> :
    #  Yiddish ligs
    0x5F0: [0x5D5, 0x5D5],  # ?? -> ????
    0x5F1: [0x5D5, 0x5D9],  #  0x5d9 should be drawn first [r to l] # ?? -> ????
    0x5F2: [0x5D9, 0x5D9],  # ?? -> ????
    #  Arabic
    0x60C: [0x2018],  # ?? -> ???
    0x66A: [0x25],  # ?? -> %
    0x66C: [0x2C],  # ?? -> ,
    0x66D: [0x22C6],  # ?? -> ???
    0x6D4: [0xB7],  # ?? -> ??
    #  Arabic isolated forms are alternates for the standard forms
    0x621: [0xFE80],  # ?? -> ???
    0x627: [0xFE8D],  # ?? -> ???
    0x628: [0xFE8F],  # ?? -> ???
    0x629: [0xFE93],  # ?? -> ???
    0x62A: [0xFE95],  # ?? -> ???
    0x62B: [0xFE99],  # ?? -> ???
    0x62C: [0xFE9D],  # ?? -> ???
    0x62D: [0xFEA1],  # ?? -> ???
    0x62E: [0xFEA5],  # ?? -> ???
    0x62F: [0xFEA9],  # ?? -> ???
    0x630: [0xFEAB],  # ?? -> ???
    0x631: [0xFEAD],  # ?? -> ???
    0x632: [0xFEAF],  # ?? -> ???
    0x633: [0xFEB1],  # ?? -> ???
    0x634: [0xFEB5],  # ?? -> ???
    0x635: [0xFEB9],  # ?? -> ???
    0x636: [0xFEBD],  # ?? -> ???
    0x637: [0xFEC1],  # ?? -> ???
    0x638: [0xFEC5],  # ?? -> ???
    0x639: [0xFEC9],  # ?? -> ???
    0x63A: [0xFECD],  # ?? -> ???
    0x641: [0xFED1],  # ?? -> ???
    0x642: [0xFED5],  # ?? -> ???
    0x643: [0xFED9],  # ?? -> ???
    0x644: [0xFEDD],  # ?? -> ???
    0x645: [0xFEE1],  # ?? -> ???
    0x646: [0xFEE5],  # ?? -> ???
    0x647: [0xFEE9],  # ?? -> ???
    0x648: [0xFEED],  # ?? -> ???
    0x649: [0xFEEF],  # ?? -> ???
    0x64A: [0xFEF1],  # ?? -> ???
    0x671: [0xFB50],  # ?? -> ???
    0x679: [0xFB66],  # ?? -> ???
    0x67A: [0xFB5E],  # ?? -> ???
    0x67B: [0xFB52],  # ?? -> ???
    0x67E: [0xFB56],  # ?? -> ???
    0x67F: [0xFB62],  # ?? -> ???
    0x680: [0xFB5A],  # ?? -> ???
    0x683: [0xFB76],  # ?? -> ???
    0x684: [0xFB72],  # ?? -> ???
    0x686: [0xFB7A],  # ?? -> ???
    0x687: [0xFB7E],  # ?? -> ???
    0x688: [0xFB88],  # ?? -> ???
    0x68C: [0xFB84],  # ?? -> ???
    0x68D: [0xFB82],  # ?? -> ???
    0x68E: [0xFB86],  # ?? -> ???
    0x691: [0xFB8C],  # ?? -> ???
    0x698: [0xFB8A],  # ?? -> ???
    0x6A4: [0xFB6A],  # ?? -> ???
    0x6A6: [0xFB6E],  # ?? -> ???
    0x6A9: [0xFB8E],  # ?? -> ???
    0x6AD: [0xFBD3],  # ?? -> ???
    0x6AF: [0xFB92],  # ?? -> ???
    0x6B1: [0xFB9A],  # ?? -> ???
    0x6B3: [0xFB96],  # ?? -> ???
    0x6BA: [0xFB9E],  # ?? -> ???
    0x6BB: [0xFBA0],  # ?? -> ???
    0x6BE: [0xFBAA],  # ?? -> ???
    0x6C1: [0xFBA6],  # ?? -> ???
    0x6C5: [0xFBE0],  # ?? -> ???
    0x6C6: [0xFBD9],  # ?? -> ???
    0x6C7: [0xFBD7],  # ?? -> ???
    0x6C8: [0xFBDB],  # ?? -> ???
    0x6C9: [0xFBE2],  # ?? -> ???
    0x6CB: [0xFBDE],  # ?? -> ???
    0x6CC: [0xFBFC],  # ?? -> ???
    0x6D0: [0xFBE4],  # ?? -> ???
    0x6D2: [0xFBAE],  # ?? -> ???
    #  Many of the Korean Jamo are ligatures of other Jamo
    #  0x110b often, but not always, rides underneath [0x1135 it's left]
    #  Chosung
    0x1101: [0x1100, 0x1100],  # ??? -> ??????
    0x1104: [0x1103, 0x1103],  # ??? -> ??????
    0x1108: [0x1107, 0x1107],  # ??? -> ??????
    0x110A: [0x1109, 0x1109],  # ??? -> ??????
    0x110D: [0x110C, 0x110C],  # ??? -> ??????
    0x1113: [0x1102, 0x1100],  # ??? -> ??????
    0x1114: [0x1102, 0x1102],  # ??? -> ??????
    0x1115: [0x1102, 0x1103],  # ??? -> ??????
    0x1116: [0x1102, 0x1107],  # ??? -> ??????
    0x1117: [0x1103, 0x1100],  # ??? -> ??????
    0x1118: [0x1105, 0x1102],  # ??? -> ??????
    0x1119: [0x1105, 0x1105],  # ??? -> ??????
    0x111A: [0x1105, 0x1112],  # ??? -> ??????
    0x111B: [0x1105, 0x110B],  # ??? -> ??????
    0x111C: [0x1106, 0x1107],  # ??? -> ??????
    0x111D: [0x1106, 0x110B],  # ??? -> ??????
    0x111E: [0x1107, 0x1100],  # ??? -> ??????
    0x111F: [0x1107, 0x1102],  # ??? -> ??????
    0x1120: [0x1107, 0x1103],  # ??? -> ??????
    0x1121: [0x1107, 0x1109],  # ??? -> ??????
    0x1122: [0x1107, 0x1109, 0x1100],  # ??? -> ?????????
    0x1123: [0x1107, 0x1109, 0x1103],  # ??? -> ?????????
    0x1124: [0x1107, 0x1109, 0x1107],  # ??? -> ?????????
    0x1125: [0x1107, 0x1109, 0x1109],  # ??? -> ?????????
    0x1126: [0x1107, 0x1109, 0x110C],  # ??? -> ?????????
    0x1127: [0x1107, 0x110C],  # ??? -> ??????
    0x1128: [0x1107, 0x110E],  # ??? -> ??????
    0x1129: [0x1107, 0x1110],  # ??? -> ??????
    0x112A: [0x1107, 0x1111],  # ??? -> ??????
    0x112B: [0x1107, 0x110B],  # ??? -> ??????
    0x112C: [0x1107, 0x1107, 0x110B],  # ??? -> ?????????
    0x112D: [0x1109, 0x1100],  # ??? -> ??????
    0x112E: [0x1109, 0x1102],  # ??? -> ??????
    0x112F: [0x1109, 0x1103],  # ??? -> ??????
    0x1130: [0x1109, 0x1105],  # ??? -> ??????
    0x1131: [0x1109, 0x1106],  # ??? -> ??????
    0x1132: [0x1109, 0x1107],  # ??? -> ??????
    0x1133: [0x1109, 0x1107, 0x1100],  # ??? -> ?????????
    0x1134: [0x1109, 0x1109, 0x1109],  # ??? -> ?????????
    0x1135: [0x1109, 0x110B],  # ??? -> ??????
    0x1136: [0x1109, 0x110C],  # ??? -> ??????
    0x1137: [0x1109, 0x110E],  # ??? -> ??????
    0x1138: [0x1109, 0x110F],  # ??? -> ??????
    0x1139: [0x1109, 0x1110],  # ??? -> ??????
    0x113A: [0x1109, 0x1111],  # ??? -> ??????
    0x113B: [0x1109, 0x1112],  # ??? -> ??????
    0x113D: [0x113C, 0x113C],  # ??? -> ??????
    0x113F: [0x113E, 0x113E],  # ??? -> ??????
    0x1141: [0x110B, 0x1100],  # ??? -> ??????
    0x1142: [0x110B, 0x1103],  # ??? -> ??????
    0x1143: [0x110B, 0x1106],  # ??? -> ??????
    0x1144: [0x110B, 0x1107],  # ??? -> ??????
    0x1145: [0x110B, 0x1109],  # ??? -> ??????
    0x1146: [0x110B, 0x1140],  # ??? -> ??????
    0x1147: [0x110B, 0x110B],  # ??? -> ??????
    0x1148: [0x110B, 0x110C],  # ??? -> ??????
    0x1149: [0x110B, 0x110E],  # ??? -> ??????
    0x114A: [0x110B, 0x1110],  # ??? -> ??????
    0x114B: [0x110B, 0x1111],  # ??? -> ??????
    0x114D: [0x110C, 0x110B],  # ??? -> ??????
    0x114F: [0x114E, 0x114E],  # ??? -> ??????
    0x1151: [0x1150, 0x1150],  # ??? -> ??????
    0x1152: [0x110E, 0x110F],  # ??? -> ??????
    0x1153: [0x110E, 0x1112],  # ??? -> ??????
    0x1156: [0x1111, 0x1107],  # ??? -> ??????
    0x1157: [0x1111, 0x110B],  # ??? -> ??????
    0x1158: [0x1112, 0x1112],  # ??? -> ??????
    #  Jungsung
    0x1162: [0x1161, 0x1175],  # ??? -> ??????
    0x1164: [0x1163, 0x1175],  # ??? -> ??????
    0x1166: [0x1165, 0x1175],  # ??? -> ??????
    0x1168: [0x1167, 0x1175],  # ??? -> ??????
    0x116A: [0x1169, 0x1161],  # ??? -> ??????
    0x116B: [0x1169, 0x1162],  # ??? -> ??????
    0x116C: [0x1169, 0x1175],  # ??? -> ??????
    0x116F: [0x116E, 0x1165],  # ??? -> ??????
    0x1170: [0x116E, 0x1166],  # ??? -> ??????
    0x1171: [0x116E, 0x1175],  # ??? -> ??????
    0x1174: [0x1173, 0x1175],  # ??? -> ??????
    0x1176: [0x1161, 0x1169],  # ??? -> ??????
    0x1177: [0x1161, 0x116E],  # ??? -> ??????
    0x1178: [0x1163, 0x1169],  # ??? -> ??????
    0x1179: [0x1163, 0x116D],  # ??? -> ??????
    0x117A: [0x1165, 0x1169],  # ??? -> ??????
    0x117B: [0x1165, 0x116E],  # ??? -> ??????
    0x117C: [0x1165, 0x1173],  # ??? -> ??????
    0x117D: [0x1167, 0x1169],  # ??? -> ??????
    0x117E: [0x1167, 0x116E],  # ??? -> ??????
    0x117F: [0x1169, 0x1165],  # ??? -> ??????
    0x1180: [0x1169, 0x1166],  # ??? -> ??????
    0x1181: [0x1169, 0x1168],  # ??? -> ??????
    0x1182: [0x1169, 0x1169],  # ??? -> ??????
    0x1183: [0x1169, 0x116E],  # ??? -> ??????
    0x1184: [0x116D, 0x1163],  # ??? -> ??????
    0x1185: [0x116D, 0x1164],  # ??? -> ??????
    0x1186: [0x116D, 0x1167],  # ??? -> ??????
    0x1187: [0x116D, 0x1169],  # ??? -> ??????
    0x1188: [0x116D, 0x1175],  # ??? -> ??????
    0x1189: [0x116E, 0x1161],  # ??? -> ??????
    0x118A: [0x116E, 0x1162],  # ??? -> ??????
    0x118B: [0x116E, 0x1165, 0x1173],  # ??? -> ?????????
    0x118C: [0x116E, 0x1168],  # ??? -> ??????
    0x118D: [0x116E, 0x116E],  # ??? -> ??????
    0x118E: [0x1172, 0x1161],  # ??? -> ??????
    0x118F: [0x1172, 0x1165],  # ??? -> ??????
    0x1190: [0x1172, 0x1166],  # ??? -> ??????
    0x1191: [0x1172, 0x1167],  # ??? -> ??????
    0x1192: [0x1172, 0x1168],  # ??? -> ??????
    0x1193: [0x1172, 0x116E],  # ??? -> ??????
    0x1194: [0x1172, 0x1175],  # ??? -> ??????
    0x1195: [0x1173, 0x116E],  # ??? -> ??????
    0x1196: [0x1173, 0x1173],  # ??? -> ??????
    0x1197: [0x1174, 0x116E],  # ??? -> ??????
    0x1198: [0x1175, 0x1161],  # ??? -> ??????
    0x1199: [0x1175, 0x1163],  # ??? -> ??????
    0x119A: [0x1175, 0x1169],  # ??? -> ??????
    0x119B: [0x1175, 0x116E],  # ??? -> ??????
    0x119C: [0x1175, 0x1173],  # ??? -> ??????
    0x119D: [0x1175, 0x119E],  # ??? -> ??????
    0x119F: [0x119E, 0x1165],  # ??? -> ??????
    0x11A0: [0x119E, 0x116E],  # ??? -> ??????
    0x11A1: [0x119E, 0x1175],  # ??? -> ??????
    0x11A2: [0x119E, 0x119E],  # ??? -> ??????
    #  Jongsung
    0x11A8: [0x1100],  # ??? -> ???
    0x11A9: [0x11A8, 0x11A8],  # ??? -> ??????
    0x11AA: [0x11A8, 0x11BA],  # ??? -> ??????
    0x11AB: [0x1102],  # ??? -> ???
    0x11AC: [0x11AB, 0x11BD],  # ??? -> ??????
    0x11AD: [0x11AB, 0x11C2],  # ??? -> ??????
    0x11AE: [0x1103],  # ??? -> ???
    0x11AF: [0x1105],  # ??? -> ???
    0x11B0: [0x11AF, 0x11A8],  # ??? -> ??????
    0x11B1: [0x11AF, 0x11B7],  # ??? -> ??????
    0x11B2: [0x11AF, 0x11B8],  # ??? -> ??????
    0x11B3: [0x11AF, 0x11BA],  # ??? -> ??????
    0x11B4: [0x11AF, 0x11C0],  # ??? -> ??????
    0x11B5: [0x11AF, 0x11C1],  # ??? -> ??????
    0x11B6: [0x11AF, 0x11C2],  # ??? -> ??????
    0x11B7: [0x1106],  # ??? -> ???
    0x11B8: [0x1107],  # ??? -> ???
    0x11B9: [0x11B8, 0x11BA],  # ??? -> ??????
    0x11BA: [0x1109],  # ??? -> ???
    0x11BB: [0x11BA, 0x11BA],  # ??? -> ??????
    0x11BC: [0x110B],  # ??? -> ???
    0x11BD: [0x110C],  # ??? -> ???
    0x11BE: [0x110E],  # ??? -> ???
    0x11BF: [0x110F],  # ??? -> ???
    0x11C0: [0x1110],  # ??? -> ???
    0x11C1: [0x1111],  # ??? -> ???
    0x11C2: [0x1112],  # ??? -> ???
    0x11C3: [0x11A8, 0x11AF],  # ??? -> ??????
    0x11C4: [0x11A8, 0x11BA, 0x11A8],  # ??? -> ?????????
    0x11C5: [0x11AB, 0x11A8],  # ??? -> ??????
    0x11C6: [0x11AB, 0x11AE],  # ??? -> ??????
    0x11C7: [0x11AB, 0x11BA],  # ??? -> ??????
    0x11C8: [0x11AB, 0x11EB],  # ??? -> ??????
    0x11C9: [0x11AB, 0x11C0],  # ??? -> ??????
    0x11CA: [0x11AE, 0x11A8],  # ??? -> ??????
    0x11CB: [0x11AE, 0x11AF],  # ??? -> ??????
    0x11CC: [0x11AF, 0x11A8, 0x11BA],  # ??? -> ?????????
    0x11CD: [0x11AF, 0x11AB],  # ??? -> ??????
    0x11CE: [0x11AF, 0x11AE],  # ??? -> ??????
    0x11CF: [0x11AF, 0x11AE, 0x11C2],  # ??? -> ?????????
    0x11D0: [0x11AF, 0x11AF],  # ??? -> ??????
    0x11D1: [0x11AF, 0x11B7, 0x11A8],  # ??? -> ?????????
    0x11D2: [0x11AF, 0x11B7, 0x11BA],  # ??? -> ?????????
    0x11D3: [0x11AF, 0x11B8, 0x11BA],  # ??? -> ?????????
    0x11D4: [0x11AF, 0x11B8, 0x11C2],  # ??? -> ?????????
    # 0x11d5: [0x11af , 0x11b8 , 0x11bc], # ??? -> ?????????
    0x11D5: [0x11AF, 0x11E6],  # ??? -> ??????
    0x11D6: [0x11AF, 0x11BA, 0x11BA],  # ??? -> ?????????
    0x11D7: [0x11AF, 0x11EB],  # ??? -> ??????
    0x11D8: [0x11AF, 0x11BF],  # ??? -> ??????
    0x11D9: [0x11AF, 0x11F9],  # ??? -> ??????
    0x11DA: [0x11B7, 0x11A8],  # ??? -> ??????
    0x11DB: [0x11B7, 0x11AF],  # ??? -> ??????
    0x11DC: [0x11B7, 0x11B8],  # ??? -> ??????
    0x11DD: [0x11B7, 0x11BA],  # ??? -> ??????
    0x11DE: [0x11B7, 0x11BA, 0x11BA],  # ??? -> ?????????
    0x11DF: [0x11B7, 0x11EB],  # ??? -> ??????
    0x11E0: [0x11B7, 0x11BE],  # ??? -> ??????
    0x11E1: [0x11B7, 0x11C2],  # ??? -> ??????
    0x11E2: [0x11B7, 0x11BC],  # ??? -> ??????
    0x11E3: [0x11B8, 0x11AF],  # ??? -> ??????
    0x11E4: [0x11B8, 0x11C1],  # ??? -> ??????
    0x11E5: [0x11B8, 0x11C2],  # ??? -> ??????
    0x11E6: [0x11B8, 0x11BC],  # ??? -> ??????
    0x11E7: [0x11BA, 0x11A8],  # ??? -> ??????
    0x11E8: [0x11BA, 0x11AE],  # ??? -> ??????
    0x11E9: [0x11BA, 0x11AF],  # ??? -> ??????
    0x11EA: [0x11BA, 0x11B8],  # ??? -> ??????
    0x11EB: [0x1140],  # ??? -> ???
    0x11EC: [0x11BC, 0x11A8],  # ??? -> ??????
    0x11ED: [0x11BC, 0x11A8, 0x11A8],  # ??? -> ?????????
    0x11EE: [0x11BC, 0x11BC],  # ??? -> ??????
    0x11EF: [0x11BC, 0x11BF],  # ??? -> ??????
    0x11F0: [0x114C],  # ??? -> ???
    0x11F1: [0x11F0, 0x11BA],  # ??? -> ??????
    0x11F2: [0x11F0, 0x11EB],  # ??? -> ??????
    0x11F3: [0x11C1, 0x11B8],  # ??? -> ??????
    0x11F4: [0x11C1, 0x11BC],  # ??? -> ??????
    0x11F5: [0x11C2, 0x11AB],  # ??? -> ??????
    0x11F6: [0x11C2, 0x11AF],  # ??? -> ??????
    0x11F7: [0x11C2, 0x11B7],  # ??? -> ??????
    0x11F8: [0x11C2, 0x11B8],  # ??? -> ??????
    0x11F9: [0x1159],  # ??? -> ???
    #  Cherokee
    0x13A0: [0x44],  # ??? -> D
    0x13A1: [0x52],  # ??? -> R
    0x13A2: [0x54],  # ??? -> T
    0x13A9: [0x423],  # ??? -> ??
    0x13AA: [0x41],  # ??? -> A
    0x13AB: [0x4A],  # ??? -> J
    0x13AC: [0x45],  # ??? -> E
    0x13B1: [0x393],  # ??? -> ??
    0x13B3: [0x57],  # ??? -> W
    0x13B7: [0x4D],  # ??? -> M
    0x13BB: [0x48],  # ??? -> H
    0x13BE: [0x398],  # ??? -> ??
    0x13C0: [0x47],  # ??? -> G
    0x13C2: [0x68],  # ??? -> h
    0x13C3: [0x5A],  # ??? -> Z
    0x13CF: [0x42C],  # ??? -> ??
    0x13D9: [0x56],  # ??? -> V
    0x13DA: [0x53],  # ??? -> S
    0x13DE: [0x4C],  # ??? -> L
    0x13DF: [0x43],  # ??? -> C
    0x13E2: [0x50],  # ??? -> P
    0x13E6: [0x4B],  # ??? -> K
    0x13F4: [0x42],  # ??? -> B
    #  punctuation
    # 0x2000: [0x20],  # ??? ->
    # 0x2001: [0x20],  # ??? ->
    0x2010: [0x2D],  # ??? -> -
    # 0x2011: [0x2D],  # ??? -> -
    0x2012: [0x2D],  # ??? -> -
    0x2013: [0x2D],  # ??? -> -
    0x2014: [0x2D],  # ??? -> -
    0x2015: [0x2D],  # ??? -> -
    0x2016: [0x7C, 0x7C],  # ??? -> ||
    0x2018: [0x60],  # ??? -> `
    0x2019: [0x27],  # ??? -> '
    0x201C: [0x22],  # ??? -> "
    0x201D: [0x22],  # ??? -> "
    # 0x2024: [0x2E],  # ??? -> .
    # 0x2025: [0x2E, 0x2E],  # ??? -> ..
    # 0x2026: [0x2E, 0x2E, 0x2E],  # ??? -> ...
    0x2032: [0x27],  # ??? -> '
    # 0x2033: [0x22],  # ??? -> "
    0x2035: [0x60],  # ??? -> `
    # 0x2036: [0x22],  # ??? -> "
    0x2039: [0x3C],  # ??? -> <
    0x203A: [0x3E],  # ??? -> >
    # 0x203C: [0x21, 0x21],  # ??? -> !!
    # 0x2048: [0x3F, 0x21],  # ??? -> ?!
    # 0x2049: [0x21, 0x3F],  # ??? -> !?
    # 0x2126: [0x3A9],  # ??? -> ??
    #  Mathematical operators
    0x2205: [0xD8],  # ??? -> ??
    0x2206: [0x394],  # ??? -> ??
    0x220F: [0x3A0],  # ??? -> ??
    0x2211: [0x3A3],  # ??? -> ??
    0x2212: [0x2D],  # ??? -> -
    0x2215: [0x2F],  # ??? -> /
    0x2216: [0x5C],  # ??? -> \
    0x2217: [0x2A],  # ??? -> *
    0x2218: [0xB0],  # ??? -> ??
    0x2219: [0xB7],  # ??? -> ??
    0x2223: [0x7C],  # ??? -> |
    0x2225: [0x7C, 0x7C],  # ??? -> ||
    0x2236: [0x3A],  # ??? -> :
    0x223C: [0x7E],  # ??? -> ~
    0x226A: [0xAB],  # ??? -> ??
    0x226B: [0xBB],  # ??? -> ??
    0x2299: [0x298],  # ??? -> ??
    0x22C4: [0x25CA],  # ??? -> ???
    0x22C5: [0xB7],  # ??? -> ??
    0x22EF: [0xB7, 0xB7, 0xB7],  # ??? -> ??????
    #  Misc Technical
    0x2303: [0x5E],  # ??? -> ^
    #  APL greek
    0x2373: [0x3B9],  # ??? -> ??
    0x2374: [0x3C1],  # ??? -> ??
    0x2375: [0x3C9],  # ??? -> ??
    0x237A: [0x3B1],  # ??? -> ??
    #  names of control chars
    0x2400: [0x4E, 0x55, 0x4C],  # ??? -> NUL
    0x2401: [0x53, 0x4F, 0x48],  # ??? -> SOH
    0x2402: [0x53, 0x54, 0x58],  # ??? -> STX
    0x2403: [0x45, 0x54, 0x58],  # ??? -> ETX
    0x2404: [0x45, 0x4F, 0x54],  # ??? -> EOT
    0x2405: [0x45, 0x4E, 0x41],  # ??? -> ENA
    0x2406: [0x41, 0x43, 0x4B],  # ??? -> ACK
    0x2407: [0x42, 0x45, 0x4C],  # ??? -> BEL
    0x2408: [0x42, 0x53],  # ??? -> BS
    0x2409: [0x48, 0x54],  # ??? -> HT
    0x240A: [0x4C, 0x46],  # ??? -> LF
    0x240B: [0x56, 0x54],  # ??? -> VT
    0x240C: [0x46, 0x46],  # ??? -> FF
    0x240D: [0x43, 0x52],  # ??? -> CR
    0x240E: [0x53, 0x4F],  # ??? -> SO
    0x240F: [0x53, 0x49],  # ??? -> SI
    0x2410: [0x44, 0x4C, 0x45],  # ??? -> DLE
    0x2411: [0x44, 0x43, 0x31],  # ??? -> DC1
    0x2412: [0x44, 0x43, 0x32],  # ??? -> DC2
    0x2413: [0x44, 0x43, 0x33],  # ??? -> DC3
    0x2414: [0x44, 0x43, 0x34],  # ??? -> DC4
    0x2415: [0x4E, 0x41, 0x4B],  # ??? -> NAK
    0x2416: [0x53, 0x59, 0x4E],  # ??? -> SYN
    0x2417: [0x45, 0x54, 0x42],  # ??? -> ETB
    0x2418: [0x43, 0x41, 0x4E],  # ??? -> CAN
    0x2419: [0x45, 0x4D],  # ??? -> EM
    0x241A: [0x53, 0x55, 0x42],  # ??? -> SUB
    0x241B: [0x45, 0x53, 0x43],  # ??? -> ESC
    0x241C: [0x46, 0x53],  # ??? -> FS
    0x241D: [0x47, 0x53],  # ??? -> GS
    0x241E: [0x52, 0x53],  # ??? -> RS
    0x241F: [0x55, 0x53],  # ??? -> US
    0x2420: [0x53, 0x50],  # ??? -> SP
    0x2421: [0x44, 0x45, 0x4C],  # ??? -> DEL
    0x2422: [0x180],  # ??? -> ??
    0x2500: [0x2014],  # ??? -> ???
    0x2502: [0x7C],  # ??? -> |
    0x25B3: [0x2206],  # ??? -> ???
    0x25B8: [0x2023],  # ??? -> ???
    0x25BD: [0x2207],  # ??? -> ???
    0x25C7: [0x25CA],  # ??? -> ???
    0x25E6: [0xB0],  # ??? -> ??
    0x2662: [0x25CA],  # ??? -> ???
    0x2731: [0x2A],  # ??? -> *
    0x2758: [0x7C],  # ??? -> |
    0x2762: [0x21],  # ??? -> !
    #  Idiographic symbols
    0x3001: [0x2C],  # ??? -> ,
    0x3008: [0x3C],  # ??? -> <
    0x3009: [0x3E],  # ??? -> >
    0x300A: [0xAB],  # ??? -> ??
    0x300B: [0xBB],  # ??? -> ??
    #  The Hangul Compatibility Jamo are just copies of the real Jamo
    #   [different spacing semantics though]. These already have NFKD forms
    # 0x3131: [0x1100],  # ??? -> ???
    # 0x3132: [0x1101],  # ??? -> ???
    # 0x3133: [0x11AA],  # ??? -> ???
    # 0x3134: [0x1102],  # ??? -> ???
    # 0x3135: [0x11AC],  # ??? -> ???
    # 0x3136: [0x11AD],  # ??? -> ???
    # 0x3137: [0x1103],  # ??? -> ???
    # 0x3138: [0x1104],  # ??? -> ???
    # 0x3139: [0x1105],  # ??? -> ???
    # 0x313A: [0x11B0],  # ??? -> ???
    # 0x313B: [0x11B1],  # ??? -> ???
    # 0x313C: [0x11B2],  # ??? -> ???
    # 0x313D: [0x11B3],  # ??? -> ???
    # 0x313E: [0x11B4],  # ??? -> ???
    # 0x313F: [0x11B5],  # ??? -> ???
    # 0x3140: [0x111A],  # ??? -> ???
    # 0x3141: [0x1106],  # ??? -> ???
    # 0x3142: [0x1107],  # ??? -> ???
    # 0x3143: [0x1108],  # ??? -> ???
    # 0x3144: [0x1121],  # ??? -> ???
    # 0x3145: [0x1109],  # ??? -> ???
    # 0x3146: [0x110A],  # ??? -> ???
    # 0x3147: [0x110B],  # ??? -> ???
    # 0x3148: [0x110C],  # ??? -> ???
    # 0x3149: [0x110D],  # ??? -> ???
    # 0x314A: [0x110E],  # ??? -> ???
    # 0x314B: [0x110F],  # ??? -> ???
    # 0x314C: [0x1110],  # ??? -> ???
    # 0x314D: [0x1111],  # ??? -> ???
    # 0x314E: [0x1112],  # ??? -> ???
    # 0x314F: [0x1161],  # ??? -> ???
    # 0x3150: [0x1162],  # ??? -> ???
    # 0x3151: [0x1163],  # ??? -> ???
    # 0x3152: [0x1164],  # ??? -> ???
    # 0x3153: [0x1165],  # ??? -> ???
    # 0x3154: [0x1166],  # ??? -> ???
    # 0x3155: [0x1167],  # ??? -> ???
    # 0x3156: [0x1168],  # ??? -> ???
    # 0x3157: [0x1169],  # ??? -> ???
    # 0x3158: [0x116A],  # ??? -> ???
    # 0x3159: [0x116B],  # ??? -> ???
    # 0x315A: [0x116C],  # ??? -> ???
    # 0x315B: [0x116D],  # ??? -> ???
    # 0x315C: [0x116E],  # ??? -> ???
    # 0x315D: [0x116F],  # ??? -> ???
    # 0x315E: [0x1170],  # ??? -> ???
    # 0x315F: [0x1171],  # ??? -> ???
    # 0x3160: [0x1172],  # ??? -> ???
    # 0x3161: [0x1173],  # ??? -> ???
    # 0x3162: [0x1174],  # ??? -> ???
    # 0x3163: [0x1175],  # ??? -> ???
    # 0x3164: [0x1160],  # ??? -> ???
    # 0x3165: [0x1114],  # ??? -> ???
    # 0x3166: [0x1115],  # ??? -> ???
    # 0x3167: [0x11C7],  # ??? -> ???
    # 0x3168: [0x11C8],  # ??? -> ???
    # 0x3169: [0x11CC],  # ??? -> ???
    # 0x316A: [0x11CE],  # ??? -> ???
    # 0x316B: [0x11D3],  # ??? -> ???
    # 0x316C: [0x11D7],  # ??? -> ???
    # 0x316D: [0x11D9],  # ??? -> ???
    # 0x316E: [0x111C],  # ??? -> ???
    # 0x316F: [0x11DD],  # ??? -> ???
    # 0x3170: [0x11DF],  # ??? -> ???
    # 0x3171: [0x111D],  # ??? -> ???
    # 0x3172: [0x111E],  # ??? -> ???
    # 0x3173: [0x1120],  # ??? -> ???
    # 0x3174: [0x1122],  # ??? -> ???
    # 0x3175: [0x1123],  # ??? -> ???
    # 0x3176: [0x1127],  # ??? -> ???
    # 0x3177: [0x1129],  # ??? -> ???
    # 0x3178: [0x112B],  # ??? -> ???
    # 0x3179: [0x112C],  # ??? -> ???
    # 0x317A: [0x112D],  # ??? -> ???
    # 0x317B: [0x112E],  # ??? -> ???
    # 0x317C: [0x112F],  # ??? -> ???
    # 0x317D: [0x1132],  # ??? -> ???
    # 0x317E: [0x1136],  # ??? -> ???
    # 0x317F: [0x1140],  # ??? -> ???
    # 0x3180: [0x1147],  # ??? -> ???
    # 0x3181: [0x114C],  # ??? -> ???
    # 0x3182: [0x11F1],  # ??? -> ???
    # 0x3183: [0x11F2],  # ??? -> ???
    # 0x3184: [0x1157],  # ??? -> ???
    # 0x3185: [0x1158],  # ??? -> ???
    # 0x3186: [0x1159],  # ??? -> ???
    # 0x3187: [0x1184],  # ??? -> ???
    # 0x3188: [0x1185],  # ??? -> ???
    # 0x3189: [0x1188],  # ??? -> ???
    # 0x318A: [0x1191],  # ??? -> ???
    # 0x318B: [0x1192],  # ??? -> ???
    # 0x318C: [0x1194],  # ??? -> ???
    # 0x318D: [0x119E],  # ??? -> ???
    # 0x318E: [0x11A1],  # ??? -> ???
    #  similar double brackets
    # 0xFF5F: [0x2E28],  # ??? -> ???
    0x2E28: [0xFF5F],  # ??? -> ???
    # 0xFF60: [0x2E29],  # ??? -> ???
    0x2E29: [0xFF60],  # ??? -> ???
}


MANUAL_POSES = {
    0x0315: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(232) - COMBINING COMMA ABOVE RIGHT
    0x0340: Pose.LEFT | Pose.ABOVE,  # CCC(230) - COMBINING GRAVE TONE MARK
    0x0341: Pose.RIGHT | Pose.ABOVE,  # CCC(230) - COMBINING ACUTE TONE MARK
    0x0345: Pose.BELOW,  # CCC(240) - COMBINING GREEK YPOGEGRAMMENI
    0x0385: Pose.ABOVE,  # CCC(0) - GREEK DIALYTIKA TONOS
    0x0483: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(230) - COMBINING CYRILLIC TITLO
    0x0484: Pose.CENTERLEFT
    | Pose.ABOVE,  # CCC(230) - COMBINING CYRILLIC PALATALIZATION
    0x0485: Pose.CENTERLEFT
    | Pose.ABOVE,  # CCC(230) - COMBINING CYRILLIC DASIA PNEUMATA
    0x0486: Pose.CENTERLEFT
    | Pose.ABOVE,  # CCC(230) - COMBINING CYRILLIC PSILI PNEUMATA
    0x0488: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING CYRILLIC HUNDRED THOUSANDS SIGN
    0x0489: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING CYRILLIC MILLIONS SIGN
    0x0596: Pose.CENTERRIGHT | Pose.BELOW,  # CCC(220) - HEBREW ACCENT TIPEHA
    0x0599: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT PASHTA
    0x059A: Pose.RIGHTEDGE | Pose.BELOW,  # CCC(222) - HEBREW ACCENT YETIV
    0x059C: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT GERESH
    0x059D: Pose.RIGHTEDGE | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT GERESH MUQDAM
    0x059E: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT GERSHAYIM
    0x05A0: Pose.RIGHTEDGE | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT TELISHA GEDOLA
    0x05A1: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT PAZER
    0x05A5: Pose.CENTERLEFT | Pose.BELOW,  # CCC(220) - HEBREW ACCENT MERKHA
    0x05A6: Pose.CENTERLEFT | Pose.BELOW,  # CCC(220) - HEBREW ACCENT MERKHA KEFULA
    0x05A8: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT QADMA
    0x05A9: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(230) - HEBREW ACCENT TELISHA QETANA
    0x05AD: Pose.RIGHTEDGE | Pose.BELOW,  # CCC(222) - HEBREW ACCENT DEHI
    0x05AE: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(228) - HEBREW ACCENT ZINOR
    0x05B0: Pose.BELOW,  # CCC(10) - HEBREW POINT SHEVA
    0x05B1: Pose.BELOW,  # CCC(11) - HEBREW POINT HATAF SEGOL
    0x05B2: Pose.BELOW,  # CCC(12) - HEBREW POINT HATAF PATAH
    0x05B3: Pose.BELOW,  # CCC(13) - HEBREW POINT HATAF QAMATS
    0x05B4: Pose.BELOW,  # CCC(14) - HEBREW POINT HIRIQ
    0x05B5: Pose.BELOW,  # CCC(15) - HEBREW POINT TSERE
    0x05B6: Pose.BELOW,  # CCC(16) - HEBREW POINT SEGOL
    0x05B7: Pose.BELOW,  # CCC(17) - HEBREW POINT PATAH
    0x05B8: Pose.BELOW,  # CCC(18) - HEBREW POINT QAMATS
    0x05B9: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(19) - HEBREW POINT HOLAM
    0x05BA: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(19) - HEBREW POINT HOLAM HASER FOR VAV
    0x05BB: Pose.BELOW,  # CCC(20) - HEBREW POINT QUBUTS
    0x05BC: Pose.OVERSTRIKE,  # CCC(21) - HEBREW POINT DAGESH OR MAPIQ
    0x05BD: Pose.BELOW,  # CCC(22) - HEBREW POINT METEG
    0x05BF: Pose.ABOVE,  # CCC(23) - HEBREW POINT RAFE
    0x05C1: Pose.RIGHTEDGE | Pose.ABOVE,  # CCC(24) - HEBREW POINT SHIN DOT
    0x05C2: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(25) - HEBREW POINT SIN DOT
    0x05C5: Pose.ABOVE,  # CCC(220) - HEBREW MARK LOWER DOT
    0x05C7: Pose.BELOW,  # CCC(18) - HEBREW POINT QAMATS QATAN
    0x064B: Pose.ABOVE,  # CCC(27) - ARABIC FATHATAN
    0x064C: Pose.ABOVE,  # CCC(28) - ARABIC DAMMATAN
    0x064D: Pose.BELOW,  # CCC(29) - ARABIC KASRATAN
    0x064E: Pose.ABOVE,  # CCC(30) - ARABIC FATHA
    0x064F: Pose.ABOVE,  # CCC(31) - ARABIC DAMMA
    0x0650: Pose.BELOW,  # CCC(32) - ARABIC KASRA
    0x0651: Pose.ABOVE,  # CCC(33) - ARABIC SHADDA
    0x0652: Pose.ABOVE,  # CCC(34) - ARABIC SUKUN
    0x0670: Pose.ABOVE,  # CCC(35) - ARABIC LETTER SUPERSCRIPT ALEF
    0x06DD: Pose.OVERSTRIKE,  # CCC(0) - ARABIC END OF AYAH
    0x06DE: Pose.OVERSTRIKE,  # CCC(0) - ARABIC START OF RUB EL HIZB
    0x0711: Pose.ABOVE,  # CCC(36) - SYRIAC LETTER SUPERSCRIPT ALAPH
    0x0732: Pose.CENTEREDOUTSIDE,  # CCC(230) - SYRIAC PTHAHA DOTTED
    0x0740: Pose.LEFTEDGE | Pose.ABOVE,  # CCC(230) - SYRIAC FEMININE DOT
    0x07A6: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA ABAFILI
    0x07A7: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA AABAAFILI
    0x07A8: Pose.CENTERLEFT | Pose.BELOW,  # CCC(0) - THAANA IBIFILI
    0x07A9: Pose.CENTERLEFT | Pose.BELOW,  # CCC(0) - THAANA EEBEEFILI
    0x07AA: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA UBUFILI
    0x07AB: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA OOBOOFILI
    0x07AC: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA EBEFILI
    0x07AD: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA EYBEYFILI
    0x07AE: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA OBOFILI
    0x07AF: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA OABOAFILI
    0x07B0: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - THAANA SUKUN
    0x0901: Pose.ABOVE,  # CCC(0) - DEVANAGARI SIGN CANDRABINDU
    0x0902: Pose.ABOVE,  # CCC(0) - DEVANAGARI SIGN ANUSVARA
    0x0903: Pose.RIGHT,  # CCC(0) - DEVANAGARI SIGN VISARGA
    0x093C: Pose.BELOW,  # CCC(7) - DEVANAGARI SIGN NUKTA
    0x093E: Pose.RIGHT,  # CCC(0) - DEVANAGARI VOWEL SIGN AA
    0x093F: Pose.LEFT,  # CCC(0) - DEVANAGARI VOWEL SIGN I
    0x0940: Pose.RIGHT,  # CCC(0) - DEVANAGARI VOWEL SIGN II
    0x0941: Pose.BELOW,  # CCC(0) - DEVANAGARI VOWEL SIGN U
    0x0942: Pose.BELOW,  # CCC(0) - DEVANAGARI VOWEL SIGN UU
    0x0943: Pose.BELOW,  # CCC(0) - DEVANAGARI VOWEL SIGN VOCALIC R
    0x0944: Pose.BELOW,  # CCC(0) - DEVANAGARI VOWEL SIGN VOCALIC RR
    0x0945: Pose.ABOVE,  # CCC(0) - DEVANAGARI VOWEL SIGN CANDRA E
    0x0946: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - DEVANAGARI VOWEL SIGN SHORT E
    0x0947: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - DEVANAGARI VOWEL SIGN E
    0x0948: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - DEVANAGARI VOWEL SIGN AI
    0x0949: Pose.RIGHT,  # CCC(0) - DEVANAGARI VOWEL SIGN CANDRA O
    0x094A: Pose.RIGHT,  # CCC(0) - DEVANAGARI VOWEL SIGN SHORT O
    0x094B: Pose.RIGHT,  # CCC(0) - DEVANAGARI VOWEL SIGN O
    0x094C: Pose.RIGHT,  # CCC(0) - DEVANAGARI VOWEL SIGN AU
    0x094D: Pose.CENTERRIGHT | Pose.BELOW,  # CCC(9) - DEVANAGARI SIGN VIRAMA
    0x0962: Pose.BELOW,  # CCC(0) - DEVANAGARI VOWEL SIGN VOCALIC L
    0x0963: Pose.BELOW,  # CCC(0) - DEVANAGARI VOWEL SIGN VOCALIC LL
    0x0981: Pose.ABOVE,  # CCC(0) - BENGALI SIGN CANDRABINDU
    0x0982: Pose.RIGHT,  # CCC(0) - BENGALI SIGN ANUSVARA
    0x0983: Pose.RIGHT,  # CCC(0) - BENGALI SIGN VISARGA
    0x09BC: Pose.BELOW,  # CCC(7) - BENGALI SIGN NUKTA
    0x09BE: Pose.RIGHT,  # CCC(0) - BENGALI VOWEL SIGN AA
    0x09BF: Pose.LEFT,  # CCC(0) - BENGALI VOWEL SIGN I
    0x09C0: Pose.RIGHT,  # CCC(0) - BENGALI VOWEL SIGN II
    0x09C1: Pose.BELOW,  # CCC(0) - BENGALI VOWEL SIGN U
    0x09C2: Pose.BELOW,  # CCC(0) - BENGALI VOWEL SIGN UU
    0x09C3: Pose.BELOW,  # CCC(0) - BENGALI VOWEL SIGN VOCALIC R
    0x09C4: Pose.CENTERRIGHT | Pose.BELOW,  # CCC(0) - BENGALI VOWEL SIGN VOCALIC RR
    0x09C7: Pose.LEFT,  # CCC(0) - BENGALI VOWEL SIGN E
    0x09C8: Pose.LEFT,  # CCC(0) - BENGALI VOWEL SIGN AI
    0x09CB: Pose.OVERSTRIKE,  # CCC(0) - BENGALI VOWEL SIGN O
    0x09CC: Pose.OVERSTRIKE,  # CCC(0) - BENGALI VOWEL SIGN AU
    0x09CD: Pose.BELOW,  # CCC(9) - BENGALI SIGN VIRAMA
    0x09D7: Pose.RIGHT,  # CCC(0) - BENGALI AU LENGTH MARK
    0x09E2: Pose.BELOW,  # CCC(0) - BENGALI VOWEL SIGN VOCALIC L
    0x09E3: Pose.BELOW,  # CCC(0) - BENGALI VOWEL SIGN VOCALIC LL
    0x0A02: Pose.ABOVE,  # CCC(0) - GURMUKHI SIGN BINDI
    0x0A3C: Pose.BELOW,  # CCC(7) - GURMUKHI SIGN NUKTA
    0x0A3E: Pose.RIGHT,  # CCC(0) - GURMUKHI VOWEL SIGN AA
    0x0A3F: Pose.LEFT,  # CCC(0) - GURMUKHI VOWEL SIGN I
    0x0A40: Pose.RIGHT,  # CCC(0) - GURMUKHI VOWEL SIGN II
    0x0A41: Pose.BELOW,  # CCC(0) - GURMUKHI VOWEL SIGN U
    0x0A42: Pose.BELOW,  # CCC(0) - GURMUKHI VOWEL SIGN UU
    0x0A47: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - GURMUKHI VOWEL SIGN EE
    0x0A48: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - GURMUKHI VOWEL SIGN AI
    0x0A4B: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - GURMUKHI VOWEL SIGN OO
    0x0A4C: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - GURMUKHI VOWEL SIGN AU
    0x0A4D: Pose.BELOW,  # CCC(9) - GURMUKHI SIGN VIRAMA
    0x0A70: Pose.ABOVE,  # CCC(0) - GURMUKHI TIPPI
    0x0A71: Pose.ABOVE,  # CCC(0) - GURMUKHI ADDAK
    0x0A81: Pose.ABOVE,  # CCC(0) - GUJARATI SIGN CANDRABINDU
    0x0A82: Pose.ABOVE,  # CCC(0) - GUJARATI SIGN ANUSVARA
    0x0A83: Pose.RIGHT,  # CCC(0) - GUJARATI SIGN VISARGA
    0x0ABC: Pose.BELOW,  # CCC(7) - GUJARATI SIGN NUKTA
    0x0ABE: Pose.RIGHT,  # CCC(0) - GUJARATI VOWEL SIGN AA
    0x0ABF: Pose.LEFT,  # CCC(0) - GUJARATI VOWEL SIGN I
    0x0AC0: Pose.RIGHT,  # CCC(0) - GUJARATI VOWEL SIGN II
    0x0AC1: Pose.BELOW,  # CCC(0) - GUJARATI VOWEL SIGN U
    0x0AC2: Pose.BELOW,  # CCC(0) - GUJARATI VOWEL SIGN UU
    0x0AC3: Pose.BELOW,  # CCC(0) - GUJARATI VOWEL SIGN VOCALIC R
    0x0AC4: Pose.BELOW,  # CCC(0) - GUJARATI VOWEL SIGN VOCALIC RR
    0x0AC5: Pose.ABOVE,  # CCC(0) - GUJARATI VOWEL SIGN CANDRA E
    0x0AC7: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - GUJARATI VOWEL SIGN E
    0x0AC8: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(0) - GUJARATI VOWEL SIGN AI
    0x0AC9: Pose.RIGHT,  # CCC(0) - GUJARATI VOWEL SIGN CANDRA O
    0x0ACB: Pose.RIGHT,  # CCC(0) - GUJARATI VOWEL SIGN O
    0x0ACC: Pose.RIGHT,  # CCC(0) - GUJARATI VOWEL SIGN AU
    0x0ACD: Pose.CENTERRIGHT | Pose.BELOW,  # CCC(9) - GUJARATI SIGN VIRAMA
    0x0B01: Pose.ABOVE,  # CCC(0) - ORIYA SIGN CANDRABINDU
    0x0B02: Pose.ABOVE,  # CCC(0) - ORIYA SIGN ANUSVARA
    0x0B03: Pose.RIGHT,  # CCC(0) - ORIYA SIGN VISARGA
    0x0B3C: Pose.BELOW,  # CCC(7) - ORIYA SIGN NUKTA
    0x0B3E: Pose.RIGHT,  # CCC(0) - ORIYA VOWEL SIGN AA
    0x0B3F: Pose.ABOVE,  # CCC(0) - ORIYA VOWEL SIGN I
    0x0B40: Pose.RIGHT,  # CCC(0) - ORIYA VOWEL SIGN II
    0x0B41: Pose.BELOW,  # CCC(0) - ORIYA VOWEL SIGN U
    0x0B42: Pose.BELOW,  # CCC(0) - ORIYA VOWEL SIGN UU
    0x0B43: Pose.BELOW,  # CCC(0) - ORIYA VOWEL SIGN VOCALIC R
    0x0B47: Pose.LEFT,  # CCC(0) - ORIYA VOWEL SIGN E
    0x0B48: Pose.OUTSIDE | Pose.LEFT | Pose.ABOVE,  # CCC(0) - ORIYA VOWEL SIGN AI
    0x0B4B: Pose.CENTEREDOUTSIDE,  # CCC(0) - ORIYA VOWEL SIGN O
    0x0B4C: Pose.CENTEREDOUTSIDE,  # CCC(0) - ORIYA VOWEL SIGN AU
    0x0B4D: Pose.BELOW,  # CCC(9) - ORIYA SIGN VIRAMA
    0x0B56: Pose.ABOVE,  # CCC(0) - ORIYA AI LENGTH MARK
    0x0B57: Pose.RIGHT,  # CCC(0) - ORIYA AU LENGTH MARK
    0x0B82: Pose.ABOVE,  # CCC(0) - TAMIL SIGN ANUSVARA
    0x0B83: Pose.RIGHT,  # CCC(0) - TAMIL SIGN VISARGA
    0x0BBE: Pose.RIGHT,  # CCC(0) - TAMIL VOWEL SIGN AA
    0x0BBF: Pose.RIGHT,  # CCC(0) - TAMIL VOWEL SIGN I
    0x0BC0: Pose.ABOVE,  # CCC(0) - TAMIL VOWEL SIGN II
    0x0BC1: Pose.RIGHT,  # CCC(0) - TAMIL VOWEL SIGN U
    0x0BC2: Pose.RIGHT,  # CCC(0) - TAMIL VOWEL SIGN UU
    0x0BC6: Pose.LEFT,  # CCC(0) - TAMIL VOWEL SIGN E
    0x0BC7: Pose.LEFT,  # CCC(0) - TAMIL VOWEL SIGN EE
    0x0BC8: Pose.LEFT,  # CCC(0) - TAMIL VOWEL SIGN AI
    0x0BCA: Pose.CENTEREDOUTSIDE,  # CCC(0) - TAMIL VOWEL SIGN O
    0x0BCB: Pose.CENTEREDOUTSIDE,  # CCC(0) - TAMIL VOWEL SIGN OO
    0x0BCC: Pose.CENTEREDOUTSIDE,  # CCC(0) - TAMIL VOWEL SIGN AU
    0x0BCD: Pose.ABOVE,  # CCC(9) - TAMIL SIGN VIRAMA
    0x0BD7: Pose.RIGHT,  # CCC(0) - TAMIL AU LENGTH MARK
    0x0C00: Pose.ABOVE,  # CCC(0) - TELUGU SIGN COMBINING CANDRABINDU ABOVE
    0x0C01: Pose.RIGHT,  # CCC(0) - TELUGU SIGN CANDRABINDU
    0x0C02: Pose.RIGHT,  # CCC(0) - TELUGU SIGN ANUSVARA
    0x0C03: Pose.RIGHT,  # CCC(0) - TELUGU SIGN VISARGA
    0x0C3E: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN AA
    0x0C3F: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN I
    0x0C40: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN II
    0x0C41: Pose.RIGHT,  # CCC(0) - TELUGU VOWEL SIGN U
    0x0C42: Pose.RIGHT,  # CCC(0) - TELUGU VOWEL SIGN UU
    0x0C43: Pose.RIGHT,  # CCC(0) - TELUGU VOWEL SIGN VOCALIC R
    0x0C44: Pose.RIGHT,  # CCC(0) - TELUGU VOWEL SIGN VOCALIC RR
    0x0C46: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN E
    0x0C47: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN EE
    0x0C48: Pose.CENTEREDOUTSIDE,  # CCC(0) - TELUGU VOWEL SIGN AI
    0x0C4A: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN O
    0x0C4B: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN OO
    0x0C4C: Pose.ABOVE,  # CCC(0) - TELUGU VOWEL SIGN AU
    0x0C4D: Pose.ABOVE,  # CCC(9) - TELUGU SIGN VIRAMA
    0x0C55: Pose.ABOVE,  # CCC(84) - TELUGU LENGTH MARK
    0x0C56: Pose.BELOW,  # CCC(91) - TELUGU AI LENGTH MARK
    0x0C82: Pose.RIGHT,  # CCC(0) - KANNADA SIGN ANUSVARA
    0x0C83: Pose.RIGHT,  # CCC(0) - KANNADA SIGN VISARGA
    0x0CBE: Pose.RIGHT,  # CCC(0) - KANNADA VOWEL SIGN AA
    0x0CBF: Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN I
    0x0CC0: Pose.OUTSIDE | Pose.RIGHT | Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN II
    0x0CC1: Pose.RIGHT,  # CCC(0) - KANNADA VOWEL SIGN U
    0x0CC2: Pose.RIGHT,  # CCC(0) - KANNADA VOWEL SIGN UU
    0x0CC3: Pose.RIGHT,  # CCC(0) - KANNADA VOWEL SIGN VOCALIC R
    0x0CC4: Pose.RIGHT,  # CCC(0) - KANNADA VOWEL SIGN VOCALIC RR
    0x0CC6: Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN E
    0x0CC7: Pose.OUTSIDE | Pose.RIGHT | Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN EE
    0x0CC8: Pose.OUTSIDE | Pose.RIGHT | Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN AI
    0x0CCA: Pose.OUTSIDE | Pose.RIGHT | Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN O
    0x0CCB: Pose.OUTSIDE | Pose.RIGHT | Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN OO
    0x0CCC: Pose.ABOVE,  # CCC(0) - KANNADA VOWEL SIGN AU
    0x0CCD: Pose.ABOVE,  # CCC(9) - KANNADA SIGN VIRAMA
    0x0CD5: Pose.RIGHT,  # CCC(0) - KANNADA LENGTH MARK
    0x0CD6: Pose.RIGHT,  # CCC(0) - KANNADA AI LENGTH MARK
    0x0D02: Pose.RIGHT,  # CCC(0) - MALAYALAM SIGN ANUSVARA
    0x0D03: Pose.RIGHT,  # CCC(0) - MALAYALAM SIGN VISARGA
    0x0D3E: Pose.RIGHT,  # CCC(0) - MALAYALAM VOWEL SIGN AA
    0x0D3F: Pose.RIGHT,  # CCC(0) - MALAYALAM VOWEL SIGN I
    0x0D40: Pose.RIGHT,  # CCC(0) - MALAYALAM VOWEL SIGN II
    0x0D41: Pose.RIGHT | Pose.BELOW,  # CCC(0) - MALAYALAM VOWEL SIGN U
    0x0D42: Pose.RIGHT | Pose.BELOW,  # CCC(0) - MALAYALAM VOWEL SIGN UU
    0x0D43: Pose.BELOW,  # CCC(0) - MALAYALAM VOWEL SIGN VOCALIC R
    0x0D46: Pose.LEFT,  # CCC(0) - MALAYALAM VOWEL SIGN E
    0x0D47: Pose.LEFT,  # CCC(0) - MALAYALAM VOWEL SIGN EE
    0x0D48: Pose.LEFT,  # CCC(0) - MALAYALAM VOWEL SIGN AI
    0x0D4A: Pose.OUTSIDE | Pose.RIGHT | Pose.LEFT,  # CCC(0) - MALAYALAM VOWEL SIGN O
    0x0D4B: Pose.OUTSIDE | Pose.RIGHT | Pose.LEFT,  # CCC(0) - MALAYALAM VOWEL SIGN OO
    0x0D4C: Pose.OUTSIDE | Pose.RIGHT | Pose.LEFT,  # CCC(0) - MALAYALAM VOWEL SIGN AU
    0x0D4D: Pose.RIGHT | Pose.ABOVE,  # CCC(9) - MALAYALAM SIGN VIRAMA
    0x0D57: Pose.RIGHT,  # CCC(0) - MALAYALAM AU LENGTH MARK
    0x0D82: Pose.RIGHT,  # CCC(0) - SINHALA SIGN ANUSVARAYA
    0x0D83: Pose.RIGHT,  # CCC(0) - SINHALA SIGN VISARGAYA
    0x0DCA: Pose.RIGHT,  # CCC(9) - SINHALA SIGN AL-LAKUNA
    0x0DCF: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN AELA-PILLA
    0x0DD0: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN KETTI AEDA-PILLA
    0x0DD1: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN DIGA AEDA-PILLA
    0x0DD2: Pose.ABOVE,  # CCC(0) - SINHALA VOWEL SIGN KETTI IS-PILLA
    0x0DD3: Pose.ABOVE,  # CCC(0) - SINHALA VOWEL SIGN DIGA IS-PILLA
    0x0DD4: Pose.BELOW,  # CCC(0) - SINHALA VOWEL SIGN KETTI PAA-PILLA
    0x0DD6: Pose.BELOW,  # CCC(0) - SINHALA VOWEL SIGN DIGA PAA-PILLA
    0x0DD8: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN GAETTA-PILLA
    0x0DD9: Pose.LEFT,  # CCC(0) - SINHALA VOWEL SIGN KOMBUVA
    0x0DDA: Pose.CENTEREDOUTSIDE,  # CCC(0) - SINHALA VOWEL SIGN DIGA KOMBUVA
    0x0DDB: Pose.LEFT,  # CCC(0) - SINHALA VOWEL SIGN KOMBU DEKA
    0x0DDC: Pose.CENTEREDOUTSIDE,  # CCC(0) - SINHALA VOWEL SIGN KOMBUVA HAA AELA-PILLA
    0x0DDD: Pose.CENTEREDOUTSIDE,  # CCC(0) - SINHALA VOWEL SIGN KOMBUVA HAA DIGA AELA-PILLA
    0x0DDE: Pose.CENTEREDOUTSIDE,  # CCC(0) - SINHALA VOWEL SIGN KOMBUVA HAA GAYANUKITTA
    0x0DDF: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN GAYANUKITTA
    0x0DF2: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN DIGA GAETTA-PILLA
    0x0DF3: Pose.RIGHT,  # CCC(0) - SINHALA VOWEL SIGN DIGA GAYANUKITTA
    0x0E31: Pose.ABOVE,  # CCC(0) - THAI CHARACTER MAI HAN-AKAT
    0x0E34: Pose.ABOVE,  # CCC(0) - THAI CHARACTER SARA I
    0x0E35: Pose.ABOVE,  # CCC(0) - THAI CHARACTER SARA II
    0x0E36: Pose.ABOVE,  # CCC(0) - THAI CHARACTER SARA UE
    0x0E37: Pose.ABOVE,  # CCC(0) - THAI CHARACTER SARA UEE
    0x0E38: Pose.RIGHT | Pose.BELOW,  # CCC(103) - THAI CHARACTER SARA U
    0x0E39: Pose.CENTERRIGHT | Pose.BELOW,  # CCC(103) - THAI CHARACTER SARA UU
    0x0E3A: Pose.RIGHT | Pose.BELOW,  # CCC(9) - THAI CHARACTER PHINTHU
    0x0E47: Pose.ABOVE,  # CCC(0) - THAI CHARACTER MAITAIKHU
    0x0E48: Pose.RIGHT | Pose.ABOVE,  # CCC(107) - THAI CHARACTER MAI EK
    0x0E49: Pose.ABOVE,  # CCC(107) - THAI CHARACTER MAI THO
    0x0E4A: Pose.ABOVE,  # CCC(107) - THAI CHARACTER MAI TRI
    0x0E4B: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(107) - THAI CHARACTER MAI CHATTAWA
    0x0E4C: Pose.ABOVE,  # CCC(0) - THAI CHARACTER THANTHAKHAT
    0x0E4D: Pose.RIGHT | Pose.ABOVE,  # CCC(0) - THAI CHARACTER NIKHAHIT
    0x0E4E: Pose.RIGHT | Pose.ABOVE,  # CCC(0) - THAI CHARACTER YAMAKKAN
    0x0EB1: Pose.ABOVE,  # CCC(0) - LAO VOWEL SIGN MAI KAN
    0x0EB4: Pose.ABOVE,  # CCC(0) - LAO VOWEL SIGN I
    0x0EB5: Pose.ABOVE,  # CCC(0) - LAO VOWEL SIGN II
    0x0EB6: Pose.ABOVE,  # CCC(0) - LAO VOWEL SIGN Y
    0x0EB7: Pose.ABOVE,  # CCC(0) - LAO VOWEL SIGN YY
    0x0EB8: Pose.BELOW,  # CCC(118) - LAO VOWEL SIGN U
    0x0EB9: Pose.BELOW,  # CCC(118) - LAO VOWEL SIGN UU
    0x0EBB: Pose.ABOVE,  # CCC(0) - LAO VOWEL SIGN MAI KON
    0x0EBC: Pose.BELOW,  # CCC(0) - LAO SEMIVOWEL SIGN LO
    0x0EC8: Pose.ABOVE,  # CCC(122) - LAO TONE MAI EK
    0x0EC9: Pose.ABOVE,  # CCC(122) - LAO TONE MAI THO
    0x0ECA: Pose.ABOVE,  # CCC(122) - LAO TONE MAI TI
    0x0ECB: Pose.ABOVE,  # CCC(122) - LAO TONE MAI CATAWA
    0x0ECC: Pose.ABOVE,  # CCC(0) - LAO CANCELLATION MARK
    0x0ECD: Pose.ABOVE,  # CCC(0) - LAO NIGGAHITA
    0x0F18: Pose.RIGHT | Pose.BELOW,  # CCC(220) - TIBETAN ASTROLOGICAL SIGN -KHYUD PA
    0x0F3E: Pose.RIGHT | Pose.BELOW,  # CCC(0) - TIBETAN SIGN YAR TSHES
    0x0F3F: Pose.LEFT | Pose.BELOW,  # CCC(0) - TIBETAN SIGN MAR TSHES
    0x0F71: Pose.BELOW,  # CCC(129) - TIBETAN VOWEL SIGN AA
    0x0F72: Pose.ABOVE,  # CCC(130) - TIBETAN VOWEL SIGN I
    0x0F73: Pose.OUTSIDE | Pose.BELOW | Pose.ABOVE,  # CCC(0) - TIBETAN VOWEL SIGN II
    0x0F74: Pose.BELOW,  # CCC(132) - TIBETAN VOWEL SIGN U
    0x0F75: Pose.BELOW,  # CCC(0) - TIBETAN VOWEL SIGN UU
    0x0F76: Pose.OUTSIDE
    | Pose.BELOW
    | Pose.ABOVE,  # CCC(0) - TIBETAN VOWEL SIGN VOCALIC R
    0x0F77: Pose.OUTSIDE
    | Pose.BELOW
    | Pose.ABOVE,  # CCC(0) - TIBETAN VOWEL SIGN VOCALIC RR
    0x0F78: Pose.OUTSIDE
    | Pose.BELOW
    | Pose.ABOVE,  # CCC(0) - TIBETAN VOWEL SIGN VOCALIC L
    0x0F79: Pose.OUTSIDE
    | Pose.BELOW
    | Pose.ABOVE,  # CCC(0) - TIBETAN VOWEL SIGN VOCALIC LL
    0x0F7A: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(130) - TIBETAN VOWEL SIGN E
    0x0F7B: Pose.CENTERLEFT | Pose.ABOVE,  # CCC(130) - TIBETAN VOWEL SIGN EE
    0x0F7C: Pose.ABOVE,  # CCC(130) - TIBETAN VOWEL SIGN O
    0x0F7D: Pose.ABOVE,  # CCC(130) - TIBETAN VOWEL SIGN OO
    0x0F7E: Pose.ABOVE,  # CCC(0) - TIBETAN SIGN RJES SU NGA RO
    0x0F7F: Pose.RIGHT,  # CCC(0) - TIBETAN SIGN RNAM BCAD
    0x0F80: Pose.ABOVE,  # CCC(130) - TIBETAN VOWEL SIGN REVERSED I
    0x0F81: Pose.OUTSIDE
    | Pose.BELOW
    | Pose.ABOVE,  # CCC(0) - TIBETAN VOWEL SIGN REVERSED II
    0x0F84: Pose.LEFT | Pose.BELOW,  # CCC(9) - TIBETAN MARK HALANTA
    0x0F90: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER KA
    0x0F91: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER KHA
    0x0F92: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER GA
    0x0F93: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER GHA
    0x0F94: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER NGA
    0x0F95: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER CA
    0x0F96: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER CHA
    0x0F97: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER JA
    0x0F99: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER NYA
    0x0F9A: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER TTA
    0x0F9B: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER TTHA
    0x0F9C: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER DDA
    0x0F9D: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER DDHA
    0x0F9E: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER NNA
    0x0F9F: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER TA
    0x0FA0: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER THA
    0x0FA1: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER DA
    0x0FA2: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER DHA
    0x0FA3: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER NA
    0x0FA4: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER PA
    0x0FA5: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER PHA
    0x0FA6: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER BA
    0x0FA7: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER BHA
    0x0FA8: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER MA
    0x0FA9: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER TSA
    0x0FAA: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER TSHA
    0x0FAB: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER DZA
    0x0FAC: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER DZHA
    0x0FAD: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER WA
    0x0FAE: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER ZHA
    0x0FAF: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER ZA
    0x0FB0: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER -A
    0x0FB1: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER YA
    0x0FB2: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER RA
    0x0FB3: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER LA
    0x0FB4: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER SHA
    0x0FB5: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER SSA
    0x0FB6: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER SA
    0x0FB7: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER HA
    0x0FB8: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER A
    0x0FB9: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER KSSA
    0x0FBA: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER FIXED-FORM WA
    0x0FBB: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER FIXED-FORM YA
    0x0FBC: Pose.BELOW,  # CCC(0) - TIBETAN SUBJOINED LETTER FIXED-FORM RA
    0x102C: Pose.RIGHT,  # CCC(0) - MYANMAR VOWEL SIGN AA
    0x102D: Pose.ABOVE,  # CCC(0) - MYANMAR VOWEL SIGN I
    0x102E: Pose.ABOVE,  # CCC(0) - MYANMAR VOWEL SIGN II
    0x102F: Pose.BELOW,  # CCC(0) - MYANMAR VOWEL SIGN U
    0x1030: Pose.BELOW,  # CCC(0) - MYANMAR VOWEL SIGN UU
    0x1031: Pose.LEFT,  # CCC(0) - MYANMAR VOWEL SIGN E
    0x1032: Pose.ABOVE,  # CCC(0) - MYANMAR VOWEL SIGN AI
    0x1036: Pose.ABOVE,  # CCC(0) - MYANMAR SIGN ANUSVARA
    0x1037: Pose.BELOW,  # CCC(7) - MYANMAR SIGN DOT BELOW
    0x1038: Pose.RIGHT,  # CCC(0) - MYANMAR SIGN VISARGA
    0x1039: Pose.ABOVE,  # CCC(9) - MYANMAR SIGN VIRAMA
    0x1056: Pose.RIGHT,  # CCC(0) - MYANMAR VOWEL SIGN VOCALIC R
    0x1057: Pose.RIGHT,  # CCC(0) - MYANMAR VOWEL SIGN VOCALIC RR
    0x1058: Pose.BELOW,  # CCC(0) - MYANMAR VOWEL SIGN VOCALIC L
    0x1059: Pose.BELOW,  # CCC(0) - MYANMAR VOWEL SIGN VOCALIC LL
    0x17B4: Pose.OVERSTRIKE,  # CCC(0) - KHMER VOWEL INHERENT AQ
    0x17B5: Pose.OVERSTRIKE,  # CCC(0) - KHMER VOWEL INHERENT AA
    0x17B6: Pose.RIGHT,  # CCC(0) - KHMER VOWEL SIGN AA
    0x17B7: Pose.ABOVE,  # CCC(0) - KHMER VOWEL SIGN I
    0x17B8: Pose.ABOVE,  # CCC(0) - KHMER VOWEL SIGN II
    0x17B9: Pose.ABOVE,  # CCC(0) - KHMER VOWEL SIGN Y
    0x17BA: Pose.ABOVE,  # CCC(0) - KHMER VOWEL SIGN YY
    0x17BB: Pose.BELOW,  # CCC(0) - KHMER VOWEL SIGN U
    0x17BC: Pose.BELOW,  # CCC(0) - KHMER VOWEL SIGN UU
    0x17BD: Pose.BELOW,  # CCC(0) - KHMER VOWEL SIGN UA
    0x17BE: Pose.OUTSIDE | Pose.LEFT | Pose.ABOVE,  # CCC(0) - KHMER VOWEL SIGN OE
    0x17BF: Pose.CENTEREDOUTSIDE,  # CCC(0) - KHMER VOWEL SIGN YA
    0x17C0: Pose.CENTEREDOUTSIDE,  # CCC(0) - KHMER VOWEL SIGN IE
    0x17C1: Pose.LEFT,  # CCC(0) - KHMER VOWEL SIGN E
    0x17C2: Pose.LEFT,  # CCC(0) - KHMER VOWEL SIGN AE
    0x17C3: Pose.LEFT,  # CCC(0) - KHMER VOWEL SIGN AI
    0x17C4: Pose.CENTEREDOUTSIDE,  # CCC(0) - KHMER VOWEL SIGN OO
    0x17C5: Pose.CENTEREDOUTSIDE,  # CCC(0) - KHMER VOWEL SIGN AU
    0x17C6: Pose.ABOVE,  # CCC(0) - KHMER SIGN NIKAHIT
    0x17C7: Pose.RIGHT,  # CCC(0) - KHMER SIGN REAHMUK
    0x17C8: Pose.RIGHT,  # CCC(0) - KHMER SIGN YUUKALEAPINTU
    0x17C9: Pose.ABOVE,  # CCC(0) - KHMER SIGN MUUSIKATOAN
    0x17CA: Pose.ABOVE,  # CCC(0) - KHMER SIGN TRIISAP
    0x17CB: Pose.ABOVE,  # CCC(0) - KHMER SIGN BANTOC
    0x17CC: Pose.ABOVE,  # CCC(0) - KHMER SIGN ROBAT
    0x17CD: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(0) - KHMER SIGN TOANDAKHIAT
    0x17CE: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(0) - KHMER SIGN KAKABAT
    0x17CF: Pose.ABOVE,  # CCC(0) - KHMER SIGN AHSDA
    0x17D0: Pose.CENTERRIGHT | Pose.ABOVE,  # CCC(0) - KHMER SIGN SAMYOK SANNYA
    0x17D1: Pose.ABOVE,  # CCC(0) - KHMER SIGN VIRIAM
    0x17D2: Pose.BELOW,  # CCC(9) - KHMER SIGN COENG
    0x17D3: Pose.ABOVE,  # CCC(0) - KHMER SIGN BATHAMASAT
    0x1AB9: Pose.CENTERLEFT
    | Pose.BELOW,  # CCC(220) - COMBINING LIGHT CENTRALIZATION STROKE BELOW
    0x1ABA: Pose.CENTERLEFT
    | Pose.BELOW,  # CCC(220) - COMBINING STRONG CENTRALIZATION STROKE BELOW
    0x1ABB: Pose.RIGHT
    | Pose.LEFT
    | Pose.ABOVE,  # CCC(230) - COMBINING PARENTHESES ABOVE
    0x1ABC: Pose.RIGHT
    | Pose.LEFT
    | Pose.ABOVE,  # CCC(230) - COMBINING DOUBLE PARENTHESES ABOVE
    0x1ABD: Pose.RIGHT
    | Pose.LEFT
    | Pose.BELOW,  # CCC(220) - COMBINING PARENTHESES BELOW
    0x1ABE: Pose.RIGHT | Pose.LEFT,  # CCC(0) - COMBINING PARENTHESES OVERLAY
    0x1FBD: Pose.ABOVE,  # CCC(0) - GREEK KORONIS
    0x1FBE: Pose.RIGHT,  # CCC(0) - GREEK PROSGEGRAMMENI
    0x1FBF: Pose.ABOVE,  # CCC(0) - GREEK PSILI
    0x1FC0: Pose.ABOVE,  # CCC(0) - GREEK PERISPOMENI
    0x1FC1: Pose.ABOVE,  # CCC(0) - GREEK DIALYTIKA AND PERISPOMENI
    0x1FCD: Pose.ABOVE,  # CCC(0) - GREEK PSILI AND VARIA
    0x1FCE: Pose.ABOVE,  # CCC(0) - GREEK PSILI AND OXIA
    0x1FCF: Pose.ABOVE,  # CCC(0) - GREEK PSILI AND PERISPOMENI
    0x1FDD: Pose.ABOVE,  # CCC(0) - GREEK DASIA AND VARIA
    0x1FDE: Pose.ABOVE,  # CCC(0) - GREEK DASIA AND OXIA
    0x1FDF: Pose.ABOVE,  # CCC(0) - GREEK DASIA AND PERISPOMENI
    0x1FED: Pose.ABOVE,  # CCC(0) - GREEK DIALYTIKA AND VARIA
    0x1FEE: Pose.ABOVE,  # CCC(0) - GREEK DIALYTIKA AND OXIA
    0x1FEF: Pose.ABOVE,  # CCC(0) - GREEK VARIA
    0x1FFD: Pose.ABOVE,  # CCC(0) - GREEK OXIA
    0x1FFE: Pose.ABOVE,  # CCC(0) - GREEK DASIA
    0x20DD: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING ENCLOSING CIRCLE
    0x20DE: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING ENCLOSING SQUARE
    0x20DF: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING ENCLOSING DIAMOND
    0x20E0: Pose.OVERSTRIKE,  # CCC(0) - COMBINING ENCLOSING CIRCLE BACKSLASH
    0x20E2: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING ENCLOSING SCREEN
    0x20E3: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING ENCLOSING KEYCAP
    0x20E4: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING ENCLOSING UPWARD POINTING TRIANGLE
    0x2CEF: Pose.RIGHT | Pose.ABOVE,  # CCC(230) - COPTIC COMBINING NI ABOVE
    0x3099: Pose.RIGHT
    | Pose.ABOVE,  # CCC(8) - COMBINING KATAKANA-HIRAGANA VOICED SOUND MARK
    0x309A: Pose.RIGHT
    | Pose.ABOVE,  # CCC(8) - COMBINING KATAKANA-HIRAGANA SEMI-VOICED SOUND MARK
    0xA670: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING CYRILLIC TEN MILLIONS SIGN
    0xA671: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING CYRILLIC HUNDRED MILLIONS SIGN
    0xA672: Pose.CENTEREDOUTSIDE,  # CCC(0) - COMBINING CYRILLIC THOUSAND MILLIONS SIGN
    0xFB1E: Pose.ABOVE,  # CCC(26) - HEBREW POINT JUDEO-SPANISH VARIKA
}
