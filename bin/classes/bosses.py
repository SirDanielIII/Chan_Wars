class Boss:
    def __init__(self, name, hp, basic, special, phrases):
        self.name = name
        self.hp = hp
        self.basic = basic
        self.special = special
        self.phrases = phrases


chan = Boss("Devil Chan", 50, "Devilish Stab", "A neat little hack", ["Here's a neat little hack"])
mrs_g = Boss("Mrs. G", 100, "", "Send you to Siberia",
             ["Sean", "One of them is a woman, the other has an Indian accent if you’re into it",
              "I'll only give you 100 if you're one of my favourite students", "Do it on Repl", "Go to Siberia!",
              "Don't ask me, use your brain", "Troubleshoot it"])
phone = Boss("Phone", 200, "Disappointment", "Thinking Question",
             ["You need to touch grass", "My son could beat you at this game",
              "Easy choices hard life, hard choices easy life", "It’s only awkward if you make it awkward",
              "Almost everything is a choice…including breathing!", "Reflect, reflect, REFLECT HARDER!!!",
              "Face the Monster… ME!", "Keep your head on a swivel!", "You have to build capacity",
              "Practice perfectly", "My record just increased", "Did you write your TQPs?",
              "You chose that? Come on, that's such CT!!!"])
