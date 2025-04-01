import os
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from api_handler import client, generate_response
import sqlite3
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

class LanguageTutor:
    def __init__(self):
        self.users = {}
        self.languages = ["Spanish", "French", "German", "Italian", "Japanese"]
        self.levels = ["Beginner", "Intermediate", "Advanced"]
        self.conn = sqlite3.connect('chat_history.db')
        self.setup_database()
        self.memory = ConversationBufferMemory()
        self.target_language = None
        self.level = None
        
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input", "level"],
            template="""You are a helpful language tutor teaching {target_language} at {level} level. 
            Maintain conversation in {target_language}, but explain corrections in English.
            Adapt your responses and corrections according to the user's level.
            Previous conversation: {history}
            Human: {input}
            AI: """
        )

    def set_language_and_level(self, language, level):
        self.target_language = language
        self.level = level
        self.save_to_history('system', f'Changed language to {language} at {level} level')

    def chat(self, user_input):
        if user_input.lower() == 'change':
            language = input("\nChoose language: ").strip()
            level = input("Choose level (Beginner/Intermediate/Advanced): ").strip()
            self.set_language_and_level(language, level)
            return f"Switched to {language} ({level} level)"

        self.save_to_history('user', user_input)
        messages = [
            {"role": "user", "content": self.prompt_template.format(
                target_language=self.target_language,
                level=self.level,
                history=self.get_chat_history(),
                input=user_input
            )}
        ]
        
        completion = generate_response(messages)
        response = completion.choices[0].message.content
        self.save_to_history('assistant', response)
        return response

    def setup_database(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history
        (timestamp TEXT, role TEXT, content TEXT)
        ''')
        self.conn.commit()

    def save_to_history(self, role, content):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('INSERT INTO chat_history VALUES (?, ?, ?)',
                      (timestamp, role, content))
        self.conn.commit()

    def get_chat_history(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT role, content FROM chat_history')
        return '\n'.join([f"{role}: {content}" for role, content in cursor.fetchall()])

def main():
    tutor = LanguageTutor()
    print(Fore.CYAN + "\n=== Welcome to Language Tutor! ===\n" + Fore.RESET)
    
    # Display language options
    print(Fore.YELLOW + "Available languages:")
    for idx, lang in enumerate(tutor.languages, 1):
        print(f"{idx}. {lang}")
    
    while True:
        try:
            lang_choice = int(input(Fore.GREEN + "\nChoose language (enter number): " + Fore.RESET))
            if 1 <= lang_choice <= len(tutor.languages):
                language = tutor.languages[lang_choice - 1]
                break
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Please enter a valid number." + Fore.RESET)
    
    # Display level options
    print(Fore.YELLOW + "\nDifficulty levels:")
    for idx, level in enumerate(tutor.levels, 1):
        print(f"{idx}. {level}")
    
    while True:
        try:
            level_choice = int(input(Fore.GREEN + "\nChoose level (enter number): " + Fore.RESET))
            if 1 <= level_choice <= len(tutor.levels):
                level = tutor.levels[level_choice - 1]
                break
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
        except ValueError:
            print(Fore.RED + "Please enter a valid number." + Fore.RESET)

    # Get user's name
    user_name = input(Fore.GREEN + "\nPlease enter your name: " + Fore.RESET).strip()
    
    tutor.set_language_and_level(language, level)
    
    print(Fore.CYAN + f"\n{'='*50}")
    print(f"Welcome, {user_name}!")
    print(f"You're now learning {language} at {level} level!")
    print(f"{'='*50}" + Fore.RESET)
    print(Fore.YELLOW + "Type 'quit' to exit or 'change' to switch language/level\n" + Fore.RESET)
    
    while True:
        user_input = input(Fore.GREEN + f"{user_name} > " + Fore.RESET)
        if user_input.lower() == 'quit':
            print(Fore.CYAN + f"\nGoodbye, {user_name}! Thanks for learning with us!" + Fore.RESET)
            break
        response = tutor.chat(user_input)
        print(Fore.BLUE + "Tutor > " + Fore.RESET + f"{response}\n")

if __name__ == "__main__":
    main()