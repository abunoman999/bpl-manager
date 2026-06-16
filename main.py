import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window

Window.clearcolor = (0.1, 0.1, 0.15, 1)

class Player:
    def __init__(self, name, role, price, rating):
        self.name = name
        self.role = role
        self.price = price
        self.rating = rating

class BPLManagerGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        
        self.budget = 120000000  
        self.my_team = []
        
        self.available_players = [
            Player("Shakib Al Hasan", "All-Rounder", 25000000, 92),
            Player("Tamim Iqbal", "Batsman", 20000000, 88),
            Player("Mushfiqur Rahim", "Wicket-Keeper", 18000000, 87),
            Player("Mustafizur Rahman", "Bowler", 22000000, 89),
            Player("Mahmudullah", "All-Rounder", 15000000, 85),
            Player("Litton Das", "Wicket-Keeper", 16000000, 86),
            Player("Taskin Ahmed", "Bowler", 17000000, 87),
            Player("Mehidy Hasan Miraz", "All-Rounder", 16000000, 86),
            Player("Najmul Hossain Shanto", "Batsman", 14000000, 84),
            Player("Towhid Hridoy", "Batsman", 13000000, 83),
            Player("Shoriful Islam", "Bowler", 14000000, 84),
            Player("Hasan Mahmud", "Bowler", 12000000, 82),
            Player("Nasum Ahmed", "Bowler", 10000000, 80),
            Player("Mahedi Hasan", "All-Rounder", 11000000, 81),
            Player("Anamul Haque Bijoy", "Batsman", 9000000, 79),
            Player("Soumya Sarkar", "All-Rounder", 10000000, 80),
            Player("Afif Hossain", "Batsman", 11000000, 81),
            Player("Ebadot Hossain", "Bowler", 12000000, 82),
            Player("Tanzid Hasan Tamim", "Batsman", 8500000, 78),
            Player("Rishad Hossain", "Bowler", 11500000, 83)
        ]
        
        self.dashboard = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        self.budget_label = Label(text=f"Budget: {self.budget:,} BDT", bold=True, color=(0.2, 0.8, 0.2, 1))
        self.squad_label = Label(text="Squad: 0/11 Players", bold=True, color=(0.2, 0.6, 1, 1))
        self.dashboard.add_widget(self.budget_label)
        self.dashboard.add_widget(self.squad_label)
        self.add_widget(self.dashboard)
        
        self.scroll_view = ScrollView(size_hint_y=0.7)
        self.player_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.player_grid.bind(minimum_height=self.player_grid.setter('height'))
        self.scroll_view.add_widget(self.player_grid)
        self.add_widget(self.scroll_view)
        
        self.controls = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        self.play_match_btn = Button(text="Play Match", background_color=(0, 0.7, 0.3, 1), font_size=16)
        self.play_match_btn.bind(on_press=self.play_match)
        
        self.medical_btn = Button(text="Medical Camp", background_color=(0.9, 0.6, 0, 1), font_size=16)
        self.medical_btn.bind(on_press=self.open_medical_camp)
        
        self.reset_btn = Button(text="Reset", background_color=(0.8, 0.2, 0.2, 1), font_size=16)
        self.reset_btn.bind(on_press=self.reset_game)
        
        self.controls.add_widget(self.play_match_btn)
        self.controls.add_widget(self.medical_btn)
        self.controls.add_widget(self.reset_btn)
        self.add_widget(self.controls)
        
        self.load_player_market()

    def load_player_market(self):
        self.player_grid.clear_widgets()
        for player in self.available_players:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=5, spacing=10)
            
            info_text = f"{player.name} ({player.role})\nRating: {player.rating} | Price: {player.price:,} BDT"
            lbl = Label(text=info_text, halign='left', valign='middle', size_hint_x=0.7)
            lbl.bind(size=lbl.setter('text_size'))
            
            btn = Button(text="Buy", size_hint_x=0.3, background_color=(0.2, 0.5, 0.9, 1))
            btn.bind(on_press=lambda instance, p=player: self.buy_player(p, instance))
            
            row.add_widget(lbl)
            row.add_widget(btn)
            self.player_grid.add_widget(row)

    def buy_player(self, player, button_instance):
        if player in self.my_team:
            self.show_popup("Already Drafted", f"{player.name} is already in your squad!")
            return
        if len(self.my_team) >= 11:
            self.show_popup("Squad Full", "You cannot select more than 11 players!")
            return
        if self.budget < player.price:
            self.show_popup("Insufficient Funds", "You do not have enough budget to buy this player!")
            return
        
        self.budget -= player.price
        self.my_team.append(player)
        button_instance.text = "Drafted"
        button_instance.disabled = True
        button_instance.background_color = (0.4, 0.4, 0.4, 1)
        
        self.budget_label.text = f"Budget: {self.budget:,} BDT"
        self.squad_label.text = f"Squad: {len(self.my_team)}/11 Players"

    def play_match(self, instance):
        if len(self.my_team) < 11:
            self.show_popup("Match Denied", f"You need exactly 11 players to play a match! Currently you have {len(self.my_team)}.")
            return
        
        total_rating = sum(p.rating for p in self.my_team)
        team_strength = total_rating / 11
        opponent_strength = random.randint(80, 90)
        
        if team_strength > opponent_strength + 3:
            result = "Win! Your team dominated the match."
            bonus = 15000000
        elif team_strength < opponent_strength - 3:
            result = "Loss! Opponent tactics outsmarted your squad."
            bonus = 5000000
        else:
            result = "Draw! It was a nail-biting close encounter."
            bonus = 8000000
            
        self.budget += bonus
        self.budget_label.text = f"Budget: {self.budget:,} BDT"
        
        self.show_popup("Match Result", f"Your Team Strength: {team_strength:.1f}\nOpponent Strength: {opponent_strength}\n\nResult: {result}\nMatch Revenue Earned: +{bonus:,} BDT")

    def open_medical_camp(self, instance):
        if not self.my_team:
            self.show_popup("Medical Camp", "Your squad is empty. No players to treat!")
            return
            
        boosted_player = random.choice(self.my_team)
        boost_amount = random.randint(1, 3)
        boosted_player.rating += boost_amount
        
        self.show_popup("Medical Camp Update", f"Fitness camp successful!\n\n{boosted_player.name}'s fitness level recovered.\nRating increased by +{boost_amount}! (New Rating: {boosted_player.rating})")
        self.load_player_market()

    def reset_game(self, instance):
        self.budget = 120000000
        self.my_team = []
        for p in self.available_players:
            if "Shakib" in p.name: p.rating = 92
            elif "Tamim" in p.name: p.rating = 88
            elif "Mushfiqur" in p.name: p.rating = 87
            elif "Mustafizur" in p.name: p.rating = 89
            
        self.budget_label.text = f"Budget: {self.budget:,} BDT"
        self.squad_label.text = "Squad: 0/11 Players"
        self.load_player_market()
        self.show_popup("Game Reset", "The market has been refreshed and budget restored to 12 Crore BDT!")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, halign='center', valign='middle'))
        
        close_btn = Button(text="OK", size_hint_y=0.3, background_color=(0.2, 0.6, 1, 1))
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

class BPLManagerApp(App):
    def build(self):
        self.title = "BPL Football Manager"
        return BPLManagerGame()

if __name__ == '__main__':
    BPLManagerApp().run()
