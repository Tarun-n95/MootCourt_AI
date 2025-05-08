import random

class Judge:
    judge_profiles = [
        {
            'name': 'Justice Patel',
            'age': 60,
            'personality': 'Strict and Methodical',
            'voice_style': 'Formal'
        },
        {
            'name': 'Justice Mehra',
            'age': 45,
            'personality': 'Friendly but Sharp',
            'voice_style': 'Conversational'
        },
        {
            'name': "Justice D'Souza",
            'age': 70,
            'personality': 'Old-school and Stern',
            'voice_style': 'Slow and Emphatic'
        },
        {
            'name': 'Justice Khan',
            'age': 50,
            'personality': 'Aggressive and Logical',
            'voice_style': 'Fast and Assertive'
        }
    ]
    
    @classmethod
    def get_random_judges(cls, number):
        return random.sample(cls.judge_profiles, k=number)
    
    @classmethod
    def get_all_judges(cls):
        return cls.judge_profiles