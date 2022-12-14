from data.jobs import jobs


class GameData:
    """游戏数据类"""

    def __init__(self):
        self.duty = ''
        '''任务名称'''
        self.map = ''
        '''地图区域'''
        self.time_start = ''
        '''起始时间'''
        self.time_end = ''
        '''结束时间'''
        self.combatant = {
            'id': '',
            'name': '',
            'worldId': '',
            'worldName': '',
            'jobId': '',
            'jobName': '',
            'role': '',
            'MaxHp': '',
            'ownerId': ''
        }
        '''
        单个战斗单位数据（缓存用）\n
            'id': \n
            'name': \n
            'worldId': \n
            'worldName': \n
            'jobId': \n
            'jobName': \n
            'role': \n
            'MaxHp': \n
        '''
        self.player = None
        '''玩家自身'''
        self.entity = []
        '''所有战斗单位列表'''
        self.party = []
        '''队友列表'''
        self.boss = []
        '''敌人列表'''

    def getJob(self, _id: str, _type='cn'):
        """
        通过职业id获取职业名或职能\n
        id :职业id\n
        type : cn(默认),en,role
        """
        if _type == 'cn':
            return jobs[_id][1]
        if _type == 'en':
            return jobs[_id][0]
        if _type == 'role':
            return jobs[_id][2]

    def partyList(self, key: str = 'id'):
        """
        返回一个包含小队人员key信息的集合，key可选:
            'id' \n
            'name' \n
            'worldId' \n
            'worldName':\n
            'jobId' \n
            'jobName' \n
            'role' \n
            'MaxHp' \n
        """
        _list = []
        for i in self.party:
            if i[key] not in _list:
                _list.append(i[key])
        return _list

    def bossList(self, key: str = 'id'):
        """
        返回一个包含所有敌方单位key信息的集合，key可选:
            'id' \n
            'name' \n
            'MaxHp' \n
        """
        _list = []
        for i in self.boss:
            if i[key] not in _list:
                _list.append(i[key])
        return _list
