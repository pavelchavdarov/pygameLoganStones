import pygame

def post_event(event_num, args_dict={}):
    event = pygame.event.Event(event_num, args_dict)
    pygame.event.post(event)