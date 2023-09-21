from player import Player
import xml.etree.ElementTree as ET
import xmltodict
import player_pb2 as PlayerList

class PlayerFactory:
    def to_json(self, players):
        '''
            This function should transform a list of Player objects into a list with dictionaries.
        '''
        players_list = [
            {
                "nickname" : player.nickname,
                "email" : player.email,
                "date_of_birth" : player.date_of_birth.strftime("%Y-%m-%d"),
                "xp" : player.xp,
                "class" : player.cls
            }
            for player in players
         ]
        
        return players_list

    def from_json(self, list_of_dict):
        '''
            This function should transform a list of dictionaries into a list with Player objects.
        '''
        player_object_list = [
            Player(
                player_dict["nickname"], 
                player_dict["email"], 
                player_dict["date_of_birth"], 
                player_dict["xp"], 
                player_dict["class"]
            ) 
            for player_dict in list_of_dict
        ]
        return player_object_list

    def from_xml(self, xml_string):
        '''
            This function should transform a XML string into a list with Player objects.
        '''
        list_of_dict = xmltodict.parse(xml_string)
        
        if type(list_of_dict['data']['player']) is list:
            parsed_raw_xml = list_of_dict['data']['player']
        else:
            parsed_raw_xml = [list_of_dict['data']['player']]
        
        player_object_list = [
            Player(
                player_dict["nickname"], 
                player_dict["email"], 
                player_dict["date_of_birth"], 
                int(player_dict["xp"]), 
                player_dict["class"]
            ) 
            for player_dict in parsed_raw_xml
        ]
        return player_object_list

    def to_xml(self, list_of_players):
        '''
            This function should transform a list with Player objects into a XML string.
        '''
        players_list = self.to_json(list_of_players)

        root = ET.Element('data')

        for item in players_list:
            result = ET.SubElement(root, 'player')
            for key, value in item.items():
                element = ET.SubElement(result, key)
                element.text = str(value)
        
        return ET.tostring(root, encoding='utf-8').decode('utf-8')
        

    def from_protobuf(self, binary):
        '''
            This function should transform a binary protobuf string into a list with Player objects.
        '''
        player_list = PlayerList.PlayersList()
        player_list.ParseFromString(binary)
        class_mappings = {int(value): key for key, value in PlayerList.Class.items()}
        new_list = []
        
        for player in player_list.player:
            new_list.append(
                Player(
                    player.nickname,
                    player.email,
                    player.date_of_birth,
                    player.xp,
                    class_mappings[player.cls],
                )
            )
        return new_list

    def to_protobuf(self, list_of_players):
        '''
            This function should transform a list with Player objects intoa binary protobuf string.
        '''
        player_list = PlayerList.PlayersList()
        
        for single_player in list_of_players:
            item = player_list.player.add()
            item.nickname = single_player.nickname
            item.email = single_player.email
            item.date_of_birth = single_player.date_of_birth.strftime("%Y-%m-%d")
            item.xp = single_player.xp
            item.cls = PlayerList.Class.Value(single_player.cls)

        return player_list.SerializeToString()

