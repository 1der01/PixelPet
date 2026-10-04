"""Random events system for PixelPet."""
import random


class EventSystem:
    """Manages random events for the pet."""

    EVENTS = [
        {"name": "get_hungry", "message": "I'm getting hungry...", "action": "feed"},
        {"name": "fall_asleep", "message": "*yawn* So sleepy...", "action": "sleep"},
        {"name": "ask_attention", "message": "Pay attention to me!", "action": "pet"},
        {"name": "find_item", "message": "Look what I found!", "action": None},
        {"name": "get_bored", "message": "I'm bored...", "action": "play"},
        {"name": "dance", "message": "*dances*", "action": None},
        {"name": "complain", "message": "Why have you been staring at that screen for three hours?", "action": "pet"},
        {"name": "mystery", "message": "I discovered a mysterious object!", "action": None},
        {"name": "ask_food", "message": "Can I have a snack?", "action": "feed"},
        {"name": "change_position", "message": "*moves to a new spot*", "action": None},
    ]

    def __init__(self):
        self.current_event = None
        self.event_timer = 0
        self.event_interval = 180  # 3 minutes in seconds

    def update(self, dt):
        """Update event timer and trigger events."""
        self.event_timer += dt
        if self.event_timer >= self.event_interval:
            self.event_timer = 0
            if random.random() < 0.3:  # 30% chance when timer hits
                return self.trigger_random_event()
        return None

    def trigger_random_event(self):
        """Trigger a random event."""
        event = random.choice(self.EVENTS)
        self.current_event = event
        return event

    def clear_event(self):
        """Clear current event."""
        self.current_event = None

    def get_dialogue_for_event(self, event, personality):
        """Get personality-specific dialogue for an event."""
        if event is None:
            return None

        personality_dialogues = {
            "Lazy": {
                "get_hungry": "I was going to get food. Then I remembered I'd have to move.",
                "fall_asleep": "Nap time. Best time.",
                "ask_attention": "Can you pet me from there? No? Okay.",
                "find_item": "I found this on the floor. It's mine now.",
                "get_bored": "Being lazy is hard work.",
                "dance": "Too much effort.",
                "complain": "You've been working too hard. I should nap more.",
                "mystery": "A mysterious object. I'll investigate... tomorrow.",
                "ask_food": "Food? Here? No, too far.",
                "change_position": "I moved. It was exhausting.",
            },
            "Energetic": {
                "get_hungry": "FOOD! LET'S GO!",
                "fall_asleep": "Who needs sleep? NOT ME! *falls asleep*",
                "ask_attention": "PLAY WITH ME! NOW!",
                "find_item": "I found a thing! IT'S AMAZING!",
                "get_bored": "LET'S DO SOMETHING! ANYTHING!",
                "dance": "WATCH ME DANCE! *spins*",
                "complain": "YOU'VE BEEN SITTING THERE FOREVER! MOVE!",
                "mystery": "MYSTERIOUS OBJECT! MUST INVESTIGATE!",
                "ask_food": "GIVE ME FOOD! GIVE ME ENERGY!",
                "change_position": "NEW LOCATION! NEW ADVENTURE!",
            },
            "Shy": {
                "get_hungry": "Um... could I have some food? Please?",
                "fall_asleep": "I'm just going to rest my eyes...",
                "ask_attention": "If you want to... you could pet me...",
                "find_item": "I found something. Do you want to see?",
                "get_bored": "Maybe we could do something quiet?",
                "dance": "I'll just... sway a little bit...",
                "complain": "You've been working a lot... are you okay?",
                "mystery": "I found something strange. Should I look?",
                "ask_food": "I'm a little hungry...",
                "change_position": "I moved a little bit. Is that okay?",
            },
            "Playful": {
                "get_hungry": "Hungry! Feed me! Let's play with food!",
                "fall_asleep": "Sleep is boring! Unless we dream about playing!",
                "ask_attention": "Play with me! Play with me!",
                "find_item": "New toy! Let's play with it!",
                "get_bored": "BORED! ENTERTAIN ME!",
                "dance": "DANCE PARTY! WOO!",
                "complain": "You're boring! Play with me instead!",
                "mystery": "A mystery! Let's solve it! Adventure!",
                "ask_food": "Food time! Play time! Same thing!",
                "change_position": "I moved! Tag, you're it!",
            },
            "Chaotic": {
                "get_hungry": "I have made a decision. I will eat everything.",
                "fall_asleep": "I will sleep. Or maybe not. Who knows!",
                "ask_attention": "LOOK AT ME! OR DON'T! I DON'T CARE!",
                "find_item": "I found this. It's mine now. No take-backs.",
                "get_bored": "I'm going to do something unpredictable. Watch this.",
                "dance": "*performs ancient ritual dance*",
                "complain": "WHY ARE YOU STILL THERE? DO SOMETHING!",
                "mystery": "THE OBJECT KNOWS. DON'T TRUST IT.",
                "ask_food": "FEED ME OR I WILL MAKE CHAOS.",
                "change_position": "I am now elsewhere. Deal with it.",
            },
            "Curious": {
                "get_hungry": "I wonder what food tastes like today?",
                "fall_asleep": "I wonder what dreams are like?",
                "ask_attention": "What are you doing? Can I watch?",
                "find_item": "What is this? How does it work?",
                "get_bored": "I want to learn something new!",
                "dance": "I wonder if I can dance like this?",
                "complain": "What are you working on? Is it interesting?",
                "mystery": "A mystery! I must investigate thoroughly!",
                "ask_food": "What's for food? I'm curious!",
                "change_position": "I wonder what it's like over here?",
            },
            "Grumpy": {
                "get_hungry": "Feed me. Now.",
                "fall_asleep": "I'm tired. Leave me alone.",
                "ask_attention": "Why are you looking at me?",
                "find_item": "I found something. Whatever.",
                "get_bored": "Everything is annoying.",
                "dance": "I don't dance.",
                "complain": "You've been there for hours. It's annoying.",
                "mystery": "A mysterious object. Probably useless.",
                "ask_food": "Food. Give it to me.",
                "change_position": "I moved. Happy now?",
            },
        }

        dialogues = personality_dialogues.get(personality, {})
        return dialogues.get(event["name"], event["message"])
