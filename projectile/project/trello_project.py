import os

from .project import Project

__all__ = ('TrelloProject', 'NoProjectManagerError')


# Exceptions
class NoProjectManagerError(RuntimeError): pass


class TrelloProject(Project):
    def __init__(self, url, trello, design_list_id, quality_member_card_url, quality_chief_card_url, *args, **kwargs):
        self.card_url = url
        self.design_list_id = design_list_id
        self.quality_member_card_url = quality_member_card_url
        self.quality_chief_card_url = quality_chief_card_url
        self.trello = trello
        self.card = None

        self.read_card()

        super().__init__(self.card['name'], *args, **kwargs)


    def read_card(self):
        self.card = self.trello.get_card_from_url(self.card_url)
    

    def filter_quality_ids(self, ids):
        quality_ids = self.trello.get_card_members(url=self.quality_member_card_url)
        return list(set(ids) & set(quality_ids))


    def get_quality_chief_id(self):
        return self.trello.get_card_members(url=self.quality_chief_card_url)[0]
    

    def is_project_manager_on_card(self):
        return self.trello.get_member(id="me")["id"] in self.trello.get_card_members(card=self.card)


    def get_quality_member_id(self):
        ids = self.trello.get_card_members(card=self.card)

        try:
            member_id = self.filter_quality_ids(ids)[0]
        except IndexError:
            member_id = self.get_quality_chief_id()
        
        return member_id


    def get_quality_member_mail(self):
        return self.trello.get_mail_from_id(self.get_quality_member_id())


    def add_members(self, ids):
        self.trello.add_members_to_card(ids, card=self.card)


    def insert_in_list(self, list_id):
        self.trello.insert_card_in_list(list_id, card=self.card)


    def design(self):
        super().design()

        if not self.is_project_manager_on_card():
            raise NoProjectManagerError("Vous n'êtes pas sur la tuile. Merci de demander au DC de vous ajouter.")

        self.add_members([self.get_quality_member_id()])
        self.insert_in_list(self.design_list_id)
