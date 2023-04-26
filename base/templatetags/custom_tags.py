from django import template
import random

register = template.Library()

# min = 1  
# max = 10  
# history = set()  
# max_history_length = 5  

# @register.simple_tag(name='generate_random_number')
# def generate_random_number():
#     while True:
#         random_number = random.randint(min, max)  
#         if random_number not in history:  
#             history.add(random_number)  
#             if len(history) > max_history_length:  
#                 history.remove(random.sample(history, 1)[0])  
#             return random_number
        
        
@register.filter(name='has_changed')
def has_changed(value, prev_value):
    return value != prev_value