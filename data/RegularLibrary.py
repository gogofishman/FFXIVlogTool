import json

regular_library = {
    '00': {
        'regular': r'^(?<type>00)\|(?<timestamp>[^|]*)\|(?<code>[^|]*)\|(?<name>[^|]*)\|(?<line>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) ChatLog (?<type>00):(?<code>[^:]*):(?<name>[^:]*):(?<line>[^:]*)(?:$|:)',
        'type': '00',
        '0xtype': '00',
        'name': 'LogLine',
        'description': '显示游戏聊天窗口的"游戏日志"记录',
        'translation': ['【游戏信息】{0[1]} 频道{0[2]}:{0[3]}', 'code', 'name', 'line']
    },
    '01': {
        'regular': r'^(?<type>01)\|(?<timestamp>[^|]*)\|(?<id>[^|]*)\|(?<name>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) Territory (?<type>01):(?<id>[^:]*):(?<name>[^:]*)(?:$|:)',
        'type': '01',
        '0xtype': '01',
        'name': 'ChangeZone',
        'description': '改变区域或登入游戏',
        'translation': ['来到地图 "{0[1]}"({0[2]})', 'name', 'id']
    },
    '02': {
        'regular': r'^(?<type>02)\|(?<timestamp>[^|]*)\|(?<id>[^|]*)\|(?<name>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) ChangePrimaryPlayer (?<type>02):(?<id>[^:]*):(?<name>[^:]*)(?:$|:)',
        'type': '02',
        '0xtype': '02',
        'name': 'ChangePrimaryPlayer',
        'description': '玩家（队友）发生变化',
        'translation': ['玩家发生改变 "{0[1]}"({0[2]})', 'name', 'id']
    },
    '03': {
        'regular': r'^(?<type>03)\|(?<timestamp>[^|]*)\|(?<id>[^|]*)\|(?<name>[^|]*)\|(?<job>[^|]*)\|(?<level>[^|]*)\|(?<ownerId>[^|]*)\|(?<worldId>[^|]*)\|(?<world>[^|]*)\|(?<npcNameId>[^|]*)\|(?<npcBaseId>[^|]*)\|(?<currentHp>[^|]*)\|(?<hp>[^|]*)\|(?<currentMp>[^|]*)\|(?<mp>[^|]*)\|(?:[^|]*\|){2}(?<x>[^|]*)\|(?<y>[^|]*)\|(?<z>[^|]*)\|(?<heading>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) AddCombatant (?<type>03):(?<id>[^:]*):(?<name>[^:]*):(?<job>[^:]*):(?<level>[^:]*):(?<ownerId>[^:]*):(?<worldId>[^:]*):(?<world>[^:]*):(?<npcNameId>[^:]*):(?<npcBaseId>[^:]*):(?<currentHp>[^:]*):(?<hp>[^:]*):(?<currentMp>[^:]*):(?<mp>[^:]*)(?::[^:]*){2}:(?<x>[^:]*):(?<y>[^:]*):(?<z>[^:]*):(?<heading>[^:]*)(?:$|:)',
        'type': '03',
        '0xtype': '03',
        'name': 'AddCombatant',
        'description': '添加新物体',
        'translation': ['添加新物体 "{0[2]}"({0[1]})\nHp:{0[3]} ; pos:({0[4]},{0[5]},{0[6]})', 'id', 'name', 'hp', 'x', 'y',
                        'z']
    },
    '04': {
        'regular': r'^(?<type>04)\|(?<timestamp>[^|]*)\|(?<id>[^|]*)\|(?<name>[^|]*)\|(?<job>[^|]*)\|(?<level>[^|]*)\|(?<owner>[^|]*)\|(?:[^|]*\|)(?<world>[^|]*)\|(?<npcNameId>[^|]*)\|(?<npcBaseId>[^|]*)\|(?:[^|]*\|)(?<hp>[^|]*)\|(?:[^|]*\|){4}(?<x>[^|]*)\|(?<y>[^|]*)\|(?<z>[^|]*)\|(?<heading>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) RemoveCombatant (?<type>04):(?<id>[^:]*):(?<name>[^:]*):(?<job>[^:]*):(?<level>[^:]*):(?<owner>[^:]*):[^:]*:(?<world>[^:]*):(?<npcNameId>[^:]*):(?<npcBaseId>[^:]*):[^:]*:(?<hp>[^:]*)(?::[^:]*){4}:(?<x>[^:]*):(?<y>[^:]*):(?<z>[^:]*):(?<heading>[^:]*)(?:$|:)',
        'type': '04',
        '0xtype': '04',
        'name': 'RemoveCombatant',
        'description': '移除物体',
        'translation': ['移除物体 "{0[2]}"({0[1]})', 'id', 'name']
    },
    '11': {
        'regular': r'^(?<type>11)\|(?<timestamp>[^|]*)\|(?<partyCount>[0-9]*)\|(?<id0>[0-9A-F]{8})?(?:\|)?(?<id1>[0-9A-F]{8})?(?:\|)?(?<id2>[0-9A-F]{8})?(?:\|)?(?<id3>[0-9A-F]{8})?(?:\|)?(?<id4>[0-9A-F]{8})?(?:\|)?(?<id5>[0-9A-F]{8})?(?:\|)?(?<id6>[0-9A-F]{8})?(?:\|)?(?<id7>[0-9A-F]{8})?(?:\|)?(?<id8>[0-9A-F]{8})?(?:\|)?(?<id9>[0-9A-F]{8})?(?:\|)?(?<id10>[0-9A-F]{8})?(?:\|)?(?<id11>[0-9A-F]{8})?(?:\|)?(?<id12>[0-9A-F]{8})?(?:\|)?(?<id13>[0-9A-F]{8})?(?:\|)?(?<id14>[0-9A-F]{8})?(?:\|)?(?<id15>[0-9A-F]{8})?(?:\|)?(?<id16>[0-9A-F]{8})?(?:\|)?(?<id17>[0-9A-F]{8})?(?:\|)?(?<id18>[0-9A-F]{8})?(?:\|)?(?<id19>[0-9A-F]{8})?(?:\|)?(?<id20>[0-9A-F]{8})?(?:\|)?(?<id21>[0-9A-F]{8})?(?:\|)?(?<id22>[0-9A-F]{8})?(?:\|)?(?<id23>[0-9A-F]{8})?(?:\|)?',
        '0xregular': r'^(?<timestamp>^.{14}) PartyList (?<type>0B):?(?<partyCount>[0-9]*):(?<id0>[0-9A-F]{8})?:?(?<id1>[0-9A-F]{8})?:?(?<id2>[0-9A-F]{8})?:?(?<id3>[0-9A-F]{8})?:?(?<id4>[0-9A-F]{8})?:?(?<id5>[0-9A-F]{8})?:?(?<id6>[0-9A-F]{8})?:?(?<id7>[0-9A-F]{8})?:?(?<id8>[0-9A-F]{8})?:?(?<id9>[0-9A-F]{8})?:?(?<id10>[0-9A-F]{8})?:?(?<id11>[0-9A-F]{8})?:?(?<id12>[0-9A-F]{8})?:?(?<id13>[0-9A-F]{8})?:?(?<id14>[0-9A-F]{8})?:?(?<id15>[0-9A-F]{8})?:?(?<id16>[0-9A-F]{8})?:?(?<id17>[0-9A-F]{8})?:?(?<id18>[0-9A-F]{8})?:?(?<id19>[0-9A-F]{8})?:?(?<id20>[0-9A-F]{8})?:?(?<id21>[0-9A-F]{8})?:?(?<id22>[0-9A-F]{8})?:?(?<id23>[0-9A-F]{8})?:?',
        'type': '11',
        '0xtype': '0B',
        'name': 'PartyList',
        'description': '队伍中的玩家发生变化',
        'translation': ['队伍发生变化，当前人数:{0[1]}', 'partyCount']
    },
    '12': {
        'regular': r'^(?<type>12)\|(?<timestamp>[^|]*)\|(?<job>[^|]*)\|(?<strength>[^|]*)\|(?<dexterity>[^|]*)\|(?<vitality>[^|]*)\|(?<intelligence>[^|]*)\|(?<mind>[^|]*)\|(?<piety>[^|]*)\|(?<attackPower>[^|]*)\|(?<directHit>[^|]*)\|(?<criticalHit>[^|]*)\|(?<attackMagicPotency>[^|]*)\|(?<healMagicPotency>[^|]*)\|(?<determination>[^|]*)\|(?<skillSpeed>[^|]*)\|(?<spellSpeed>[^|]*)\|(?:[^|]*\|)(?<tenacity>[^|]*)\|(?<localContentId>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) PlayerStats (?<type>0C):(?<job>[^:]*):(?<strength>[^:]*):(?<dexterity>[^:]*):(?<vitality>[^:]*):(?<intelligence>[^:]*):(?<mind>[^:]*):(?<piety>[^:]*):(?<attackPower>[^:]*):(?<directHit>[^:]*):(?<criticalHit>[^:]*):(?<attackMagicPotency>[^:]*):(?<healMagicPotency>[^:]*):(?<determination>[^:]*):(?<skillSpeed>[^:]*):(?<spellSpeed>[^:]*):[^:]*:(?<tenacity>[^:]*):(?<localContentId>[^:]*)(?:$|:)',
        'type': '12',
        '0xtype': '0C',
        'name': 'PlayerStats',
        'description': '玩家状态属性发生变化或来到新区域',
        'translation': ['当前职业:{0[1]} ; 技速:{0[5]} ; 咏唱:{0[6]}\n直击:{0[2]} ; 暴击:{0[3]} ; 信念:{0[4]}', 'job', 'directHit',
                        'criticalHit', 'determination', 'skillSpeed', 'spellSpeed']
    },
    '20': {
        'regular': r'^(?<type>20)\|(?<timestamp>[^|]*)\|(?<sourceId>[^|]*)\|(?<source>[^|]*)\|(?<id>[^|]*)\|(?<ability>[^|]*)\|(?<targetId>[^|]*)\|(?<target>[^|]*)\|(?<castTime>[^|]*)\|(?<x>[^|]*)\|(?<y>[^|]*)\|(?<z>[^|]*)\|(?<heading>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) StartsCasting (?<type>14):(?<sourceId>[^:]*):(?<source>[^:]*):(?<id>[^:]*):(?<ability>(?:[^:]|: )*?):(?<targetId>[^:]*):(?<target>[^:]*):(?<castTime>[^:]*):(?<x>[^:]*):(?<y>[^:]*):(?<z>[^:]*):(?<heading>[^:]*)(?:$|:)',
        'type': '20',
        '0xtype': '14',
        'name': 'StartsCasting',
        'description': '读条施法',
        'translation': ['{0[1]}正在读条施法\n"{0[2]}"({0[5]})。\n(施法时间) {0[3]} 秒\n(目标) {0[4]}', 'source', 'ability',
                        'castTime',
                        'target', 'id']
    },
    '21': {
        'regular': r'^(?<type>21)\|(?<timestamp>[^|]*)\|(?<sourceId>[^|]*)\|(?<source>[^|]*)\|(?<id>[^|]*)\|(?<ability>[^|]*)\|(?<targetId>[^|]*)\|(?<target>[^|]*)\|(?<flags>[^|]*)\|(?<damage>[^|]*)\|(?:[^|]*\|){14}(?<targetCurrentHp>[^|]*)\|(?<targetMaxHp>[^|]*)\|(?<targetCurrentMp>[^|]*)\|(?<targetMaxMp>[^|]*)\|(?:[^|]*\|){2}(?<targetX>[^|]*)\|(?<targetY>[^|]*)\|(?<targetZ>[^|]*)\|(?<targetHeading>[^|]*)\|(?<currentHp>[^|]*)\|(?<maxHp>[^|]*)\|(?<currentMp>[^|]*)\|(?<maxMp>[^|]*)\|(?:[^|]*\|){2}(?<x>[^|]*)\|(?<y>[^|]*)\|(?<z>[^|]*)\|(?<heading>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) ActionEffect (?<type>15):(?<sourceId>[^:]*):(?<source>[^:]*):(?<id>[^:]*):(?<ability>(?:[^:]|: )*?):(?<targetId>[^:]*):(?<target>[^:]*):(?<flags>[^:]*):(?<damage>[^:]*)(?::[^:]*){14}:(?<targetCurrentHp>[^:]*):(?<targetMaxHp>[^:]*):(?<targetCurrentMp>[^:]*):(?<targetMaxMp>[^:]*)(?::[^:]*){2}:(?<targetX>[^:]*):(?<targetY>[^:]*):(?<targetZ>[^:]*):(?<targetHeading>[^:]*):(?<currentHp>[^:]*):(?<maxHp>[^:]*):(?<currentMp>[^:]*):(?<maxMp>[^:]*)(?::[^:]*){2}:(?<x>[^:]*):(?<y>[^:]*):(?<z>[^:]*):(?<heading>[^:]*):',
        'type': '21',
        '0xtype': '15',
        'name': 'Ability',
        'description': '技能释放',
        'translation': ['{0[1]} → {0[2]}释放了\n"{0[3]}"({0[4]})。\n(造成伤害) {0[5]}', 'source', 'target', 'ability', 'id',
                        'damage']
    },
    '22': {
        'regular': r'^(?<type>22)\|(?<timestamp>[^|]*)\|(?<sourceId>[^|]*)\|(?<source>[^|]*)\|(?<id>[^|]*)\|(?<ability>[^|]*)\|(?<targetId>[^|]*)\|(?<target>[^|]*)\|(?<flags>[^|]*)\|(?<damage>[^|]*)\|(?:[^|]*\|){14}(?<targetCurrentHp>[^|]*)\|(?<targetMaxHp>[^|]*)\|(?<targetCurrentMp>[^|]*)\|(?<targetMaxMp>[^|]*)\|(?:[^|]*\|){2}(?<targetX>[^|]*)\|(?<targetY>[^|]*)\|(?<targetZ>[^|]*)\|(?<targetHeading>[^|]*)\|(?<currentHp>[^|]*)\|(?<maxHp>[^|]*)\|(?<currentMp>[^|]*)\|(?<maxMp>[^|]*)\|(?:[^|]*\|){2}(?<x>[^|]*)\|(?<y>[^|]*)\|(?<z>[^|]*)\|(?<heading>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) AOEActionEffect (?<type>16):(?<sourceId>[^:]*):(?<source>[^:]*):(?<id>[^:]*):(?<ability>(?:[^:]|: )*?):(?<targetId>[^:]*):(?<target>[^:]*):(?<flags>[^:]*):(?<damage>[^:]*)(?::[^:]*){14}:(?<targetCurrentHp>[^:]*):(?<targetMaxHp>[^:]*):(?<targetCurrentMp>[^:]*):(?<targetMaxMp>[^:]*)(?::[^:]*){2}:(?<targetX>[^:]*):(?<targetY>[^:]*):(?<targetZ>[^:]*):(?<targetHeading>[^:]*):(?<currentHp>[^:]*):(?<maxHp>[^:]*):(?<currentMp>[^:]*):(?<maxMp>[^:]*)(?::[^:]*){2}:(?<x>[^:]*):(?<y>[^:]*):(?<z>[^:]*):(?<heading>[^:]*):',
        'type': '21',
        '0xtype': '15',
        'name': 'Ability(AOE)',
        'description': 'AOE技能释放',
        'translation': ['{0[1]} → {0[2]}释放了\n"{0[3]}"({0[4]})。\n(造成伤害) {0[5]}', 'source', 'target', 'ability', 'id',
                        'damage']
    },
    '23': {
        'regular': r'^(?<type>23)\|(?<timestamp>[^|]*)\|(?<sourceId>[^|]*)\|(?<source>[^|]*)\|(?<id>[^|]*)\|(?<name>[^|]*)\|(?<reason>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) CancelAction (?<type>17):(?<sourceId>[^:]*):(?<source>[^:]*):(?<id>[^:]*):(?<name>[^:]*):(?<reason>[^:]*)',
        'type': '23',
        '0xtype': '17',
        'name': 'CancelAbility',
        'description': '技能中断',
        'translation': ['{0[1]} 中断释放"{0[2]}"({0[3]})\n(原因) {0[4]}', 'source', 'name', 'id', 'reason']
    },
    '24': {
        'regular': r'^(?<type>24)\|(?<timestamp>[^|]*)\|(?<id>[^|]*)\|(?<name>[^|]*)\|(?<which>[^|]*)\|(?<effectId>[^|]*)\|(?<damage>[^|]*)\|(?<currentHp>[^|]*)\|(?<maxHp>[^|]*)\|(?<currentMp>[^|]*)\|(?<maxMp>[^|]*)\|(?:[^|]*\|){2}(?<x>[^|]*)\|(?<y>[^|]*)\|(?<z>[^|]*)\|(?<heading>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) DoTHoT (?<type>18):(?<id>[^:]*):(?<name>[^:]*):(?<which>[^:]*):(?<effectId>[^:]*):(?<damage>[^:]*):(?<currentHp>[^:]*):(?<maxHp>[^:]*):(?<currentMp>[^:]*):(?<maxMp>[^:]*)(?::[^:]*){2}:(?<x>[^:]*):(?<y>[^:]*):(?<z>[^:]*):(?<heading>[^:]*)(?:$|:)',
        'type': '24',
        '0xtype': '18',
        'name': 'DoT',
        'description': 'HoT或DoT在该时间时的总量',
        'translation': ['"{0[1]}"({0[2]})跳了{0[3]}\n(总量) {0[4]}', 'name', 'id', 'which', 'damage']
    },
    '25': {
        'regular': r'^(?<type>25)\|(?<timestamp>[^|]*)\|(?<targetId>[^|]*)\|(?<target>[^|]*)\|(?<sourceId>[^|]*)\|(?<source>[^|]*)\|',
        '0xregular': r'(?<timestamp>^.{14}) Death (?<type>19):(?<targetId>[^:]*):(?<target>[^:]*):(?<sourceId>[^:]*):(?<source>[^:]*)(?:$|:)',
        'type': '25',
        '0xtype': '19',
        'name': 'Death',
        'description': '单位死亡',
        'translation': ['"{0[1]}"杀死了"{0[2]}"', 'source', 'target']
    },
}

