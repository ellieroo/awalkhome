import pygame
import pygame_menu
from pygame_menu import themes
import getpass
import webbrowser
import sys
real_username = getpass.getuser()
player_name = ""
told_someone = False

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1400, 1050
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Walk Home")

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Custom Font Setup
FONT_NAME = "timesnewroman"
FONT_SIZE_MENU = 40
FONT_SIZE_GAME = 32

def typewriter_text(line, y, delay=30, center=True, font=None, color=WHITE, previous_lines=None):
    """Draws a single line with a typewriter effect, preserving previous lines."""
    if font is None:
        font = game_font
    displayed = ''
    
    for char in line:
        displayed += char
        surface.fill(BLACK)

        # Redraw previous lines (if any)
        if previous_lines:
            for text, line_y in previous_lines:
                rendered = font.render(text, True, color)
                rect = rendered.get_rect(center=(WIDTH // 2, line_y)) if center else rendered.get_rect(topleft=(50, line_y))
                surface.blit(rendered, rect)

        # Render current typing line
        text_surface = font.render(displayed, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y)) if center else text_surface.get_rect(topleft=(50, y))
        surface.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(delay)

def typewriter_paragraph(lines, start_y, line_spacing=60, delay=30):
    """Draws multiple lines with typewriter effect and keeps them on screen."""
    surface.fill(BLACK)
    previous_lines = []

    for i, line in enumerate(lines):
        y = start_y + i * line_spacing
        typewriter_text(line, y=y, delay=delay, previous_lines=previous_lines)
        previous_lines.append((line, y))  # Store full line once typed
        pygame.time.delay(300)  # pause between lines

    pygame.time.delay(1500)  # final pause

menu_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MENU)
game_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_GAME)

# Custom Theme
custom_theme = themes.THEME_DARK.copy()
custom_theme.background_color = BLACK
custom_theme.title_background_color = BLACK
custom_theme.title_font_color = WHITE
custom_theme.widget_font_color = WHITE
custom_theme.widget_selection_effect.color = GRAY
custom_theme.widget_font = menu_font
custom_theme.title_offset = (0, -50)  # Adjusts vertical alignment
custom_theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER  # Aligns widgets

def wait_for_key(valid_keys=None, prompt_type="continue"):
    """
    Waits for a key press.
    If valid_keys is provided (e.g., ['y', 'n']), waits for one of those keys.
    If not, waits for any key (like Enter) to continue.
    
    Returns the pressed key (lowercased) if using valid_keys.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = event.unicode.lower()
                if valid_keys:
                    if key in valid_keys:
                        return key
                else:
                    if prompt_type == "continue":
                        return key

def draw_choices(choices):
    """
    Draws up to 4 choices aligned near the bottom of the screen.
    Accepts a list of up to 4 strings. Empty strings or None will be skipped visually.
    """
    slot_count = 4
    spacing = 60
    start_y = HEIGHT - (spacing * slot_count) - 60  # Leave some bottom margin

    for i in range(slot_count):
        if i < len(choices) and choices[i]:
            text = game_font.render(choices[i], True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, start_y + i * spacing))
            surface.blit(text, text_rect)

def display_exit_ascii_art():
    ascii_art = [
        "                                     +              #####",
        "                                   / \\",
        " _____        _____     __________/ o \\/\\_________      _________",
        "|o o o|_______|    |___|               | | # # #  |____|o o o o  | /\\",
        "|o o o|  * * *|: ::|. .|               |o| # # #  |. . |o o o o  |//\\\\",
        "|o o o|* * *  |::  |. .| []  []  []  []|o| # # #  |. . |o o o o  |((|))",
        "|o o o|**  ** |:  :|. .| []  []  []    |o| # # #  |. . |o o o o  |((|))",
        "|_[]__|__[]___|_||_|__<|____________;;_|_|___/\\___|_.|_|____[]___|"
    ]
    # Use a monospace font (Courier) to preserve spacing in ASCII art.
    ascii_font = pygame.font.SysFont("courier", 20)
    surface.fill(BLACK)
    y_start = HEIGHT // 3
    for i, line in enumerate(ascii_art):
        text_surface = ascii_font.render(line, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_start + i * 24))
        surface.blit(text_surface, text_rect)
    # Draw additional text below the art.
    outside_text = "You're on the street."
    outside_surface = game_font.render(outside_text, True, WHITE)
    outside_rect = outside_surface.get_rect(center=(WIDTH // 2, y_start + len(ascii_art) * 24 + 40))
    surface.blit(outside_surface, outside_rect)
    pygame.display.update()
    

# Start Game Function
def start_the_game():
    global player_name
    player_name = mainmenu.get_input_data().get('name_input', '').strip()
    surface.fill(BLACK)
    typewriter_paragraph([f"Welcome, {player_name}!"], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(2000)  # Show welcome message briefly
    first_prompt_screen()

# First Prompt
def first_prompt_screen():
    surface.fill(BLACK)
    typewriter_paragraph(["It's time to go home.", "(Press Enter to continue)"], HEIGHT // 3)
    pygame.display.update()
    
    wait_for_key(prompt_type="continue")  # <- clean reusable wait
    character_choices()


def character_choices():
    """Handles the player's choice of whether to inform someone before leaving."""
    surface.fill(BLACK)
    typewriter_paragraph([
        "The party is winding down.",
        "The chatter is a low background noise and the floor is sticky.",
        "You have class in the morning.",
        "Find someone to tell you're leaving? (Y/N)"
    ], HEIGHT // 3)
    pygame.display.update()

    # Wait for valid key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressed = event.unicode.lower()
                if key_pressed in ['y', 'n']:
                    choice = "yes" if key_pressed == "y" else "no"

                    surface.fill(BLACK)
                    if choice == "yes":
                        told_someone = True 
                        result_text = ["Someone knows you're leaving. Exit the party?","(Y/N)"]
                    else:
                        result_text = ["You don't know these people anyways.", "Exit the party?", "(Y/N)"]
                    
                    typewriter_paragraph(result_text, HEIGHT // 3)
                    pygame.display.update()

                    # Wait for second choice
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.KEYDOWN:
                                second_key = event.unicode.lower()
                                if second_key == 'y':
                                    display_exit_ascii_art()
                                    pygame.time.delay(2500)
                                    exit_party_path()  
                                elif second_key == 'n':
                                    stay_party_path()  
                                 

def exit_party_path():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You gather your things and wave in the vague direction of whoever is left.",
        "The door clicks closed behind you.",
        "It's humid. You can feel your clothes on your skin."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    first_path_split()
    

def stay_party_path():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The host is looking at you a little sidways. It's clearly time to leave.",
        "Do you really want to be that guy?",
        "(Y/N)",
    ], HEIGHT // 3)
    pygame.display.update()
    choice = wait_for_key(valid_keys=["y", "n"])
    if choice == "y":
        get_out_path()
    else:
        leaving_voluntarily_path()

def get_out_path():
    # Step 1: Display initial loiter message
    surface.fill(BLACK)
    typewriter_paragraph([
        "So you're a game dev's worst nightmare.",
        "You can loiter, I guess."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)  # Let it sit for dramatic effect

    # Step 2: Red shaking text
    font_big = pygame.font.SysFont("timesnewroman", 100, bold=True)
    message = f"YOU CAN'T ESCAPE {real_username}"
    shake_intensity = 12
    shake_frames = 30

    for i in range(shake_frames):
        surface.fill(BLACK)

        # Alternate shake offset
        offset_x = ((-1) ** i) * (shake_intensity if i % 2 == 0 else shake_intensity // 2)
        offset_y = ((-1) ** (i + 1)) * (shake_intensity // 2)

        text_surface = font_big.render(message, True, (255, 0, 0))  # Red
        text_rect = text_surface.get_rect(center=(WIDTH // 2 + offset_x, HEIGHT // 2 + offset_y))
        surface.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(80)  # speed of shake

    # Step 3: Flicker between input name and real username
    flicker_font = pygame.font.SysFont("timesnewroman", 48, bold=True)
    for i in range(12):  # flicker 12 frames
        surface.fill(BLACK)
        if i % 2 == 0:
            text = f"You're leaving, {player_name}."
        else:
            text = f"You're leaving, {real_username}."
        text_surface = flicker_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surface.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(150)

    # Pause on the last message
    surface.fill(BLACK)
    final_surface = flicker_font.render(f"You're leaving, {player_name}.", True, WHITE)
    final_rect = final_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(final_surface, final_rect)
    pygame.display.update()
    pygame.time.delay(1500)

    exit_party_path()


def leaving_voluntarily_path():
    surface.fill(BLACK)
    typewriter_paragraph([
        "Congratulations.",
        "You've achieved basic social awareness.",
        "Stay aware.",
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    first_path_split

def first_path_split():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The air thickens. Something is watching.",
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "Or maybe you're just tired.",
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Take a shortcut home just in case.",
        "2 - Take the long way.",
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    if choice == "1":
        first_shortcut()
    elif choice == "2":
        first_long_way()
    

def first_long_way():
    global told_someone  
    surface.fill(BLACK)
    typewriter_paragraph([
        "There are footsteps behind you.",
        "You don't want to be rude and look behind you.",
        "But there's a reflection in a nearby store window. It's still there two streets later." 
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    surface.fill(BLACK)
    typewriter_paragraph([
        "You don't want to be presumptuous.",
        "But it seems like they're following you."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    # Build the choices list dynamically
    choices = [
        "1 - Zig zag through side streets. Maybe you'll lose them.",
        "2 - Cross the street and slow down to wave at the person. Maybe acknowledging them will spook them.",
        "",  
    ]

    if told_someone:
        choices[2] = "3 - Text the friend you told you were leaving earlier. Maybe they'll help."

    draw_choices(choices)
    pygame.display.update()

    # Build valid keys based on available options
    valid_keys = ["1", "2"]
    if told_someone:
        valid_keys.append("3")

    choice = wait_for_key(valid_keys=valid_keys)

    if choice == "1":
        zig_zag()
    elif choice == "2":
        acknowledged_follower()
    elif choice == "3":
        text_for_help()

def zig_zag():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You look around for options.",
        "You need to make a call quickly.",
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    surface.fill(BLACK)
    typewriter_paragraph([
        "There's a gas station a block away. You can see the profile of the cashier inside.",
        "There's an alley about a hundred feet away.",
        "You're closer to the house you came from than to your campus apartment."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    # Build the choices list dynamically
    choices = [
        "1 - Duck into the gas station.",
        "2 - Cut into the alley.",
        "3 - Loop back towards the party house.",  
    ]

    draw_choices(choices)
    pygame.display.update()

    valid_keys = ["1", "2", "3"]

    choice = wait_for_key(valid_keys=valid_keys)

    if choice == "1":
        gas_station()
    elif choice == "2":
        alley()
    elif choice == "3":
        loop_back()

def text_for_help():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You aren't exactly sure what to say.",
        "You're not even sure anything strange is happening.",
        "How much  should you explain?"
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Send a detailed text explaining that you're not sure what's happening,"
        "but you're stressed.",
        "2 - Send a quick text telling your friend you think someone is following you."
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    if choice == "1":
        long_text()
    elif choice == "2":
        quick_text()

def long_text():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You quickly pull out your phone and start typing.",
        "You start to explain where you are and what you're worried about."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    surface.fill(BLACK)
    typewriter_paragraph([
        "But you take too long.",
        "He's quiet when he approaches",
        "You don't even have a chance to scream."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    typewriter_paragraph([
        "Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def quick_text():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You quickly pull out your phone and start typing.",
        "You tell your friend where you are and that you think you're being followed."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "When you look back up, the person is nowhere to be seen.",
        "But you still feel eyes on you.",
        "You need to move."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Duck into a nearby gas station. You can see the profile of a cashier inside.",
        "2 - Move under a street light and wait for your friend to reply."
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    
    if choice == "1":
        gas_station()
    elif choice == "2":
        street_light()

def gas_station():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You dart into the gas station store. A bell half-jingles brokenly as you enter.",
        "The cashier glances up from his magazine. He can't be older than nineteen.",
        "He looks like he spends a lot of time in his mom's basement."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You're not sure what the best move is.",
        "The cashier clearly has a cell phone. And at least he's another person to be near.",
        "You spot a bathroom near the back of the store."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Approach the cashier to ask for help.",
        "2 - Lock yourself in the bathroom until your friend can get there.",
        "3 - Pretend to shop the crummy protein bars and candy. Stay in the open.",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2", "3"] 
    choice = wait_for_key(valid_keys=valid_keys)
    
    if choice == "1":
        cashier_help()
    elif choice == "2":
        lock_bathroom()
    elif choice == "3":
        pretend_shop()
    

def gas_station_nohelp():
    surface.fill(BLACK)
    typewriter_paragraph([
        "Go back to what else you thought of earlier."
    ])
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Lock yourself in the bathroom until your friend can get there."
        "2 - Pretend to shop the crummy protein bars and candy. Stay in the open.",  
        "",
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    
    if choice == "1":
        lock_bathroom()
    elif choice == "2":
        pretend_shop()

def cashier_help():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The cashier is back to reading his magazine that as you get closer, you notice to be...",
        "Well, let's go with vaguely pornographic. Yuck.",
        "He barely looks at you as you stop in front of the counter. He's smacking his gum.",
        "[Cashier] What can I grab for you? We're out of the Jackpot scratchoffs. Some dumbass bought all of them."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    draw_choices([
        "1 - Ask the cashier if you can wait up front with him. At least near the checkout where he can see you.",
        "2 - Ask him to call the police."
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    
    if choice == "1":
        cashier_front()
    elif choice == "2":
        cashier_police()

def cashier_front():
    return

def stay_with_cashier():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You edge closer to the front counter.",
        "You glance over to find the cashier leering at you, leaning over the counter.",
        "[Cashier] Hey, man, if I saw someone dressed like you, I'd think they were begging me to follow them..",
        "You skitter back from the guy."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "At least this guy is on the clock. He probably won't pull anything. But you're deeply uncomfortable.",
        "As if it was a miracle, your phone rings. It's your friend.",
        "[Friend] {player_name}, I am so, so sorry but I got a freaking flat.",
        "Your heart sinks.",
        "[Friend] I've called you an Uber. Don't worry about paying for it.",
        "{Friend] It's a grey sedan and it should be there in five.",
        "You wait tensely, casting glances back and forth between your follower in the corner",
        "...and this creepy cashier.",
        "Finally, you get the text that the car is here. You hurry outside."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Knock on the passenger window to talk to the driver and ask him to take a different route home.",
        "2 - Call the driver number that your friend sent you.",
        "3 - Approach the car slowly. Try to check the license plate.",
        ""  
        
    ])
    pygame.display.update()
    valid_keys = ["1", "2", "3"] 
    choice = wait_for_key(valid_keys=valid_keys)
    
    if choice == "1":
        driver_different_route()
        
    elif choice == "2":
        call_driver()
    
    elif choice == "3":
        license_plate()

def driver_different_route():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The driver rolls down the window and appraises you.",
        "[Driver] You gonna give me somethin' extra?",
        "You don't know exactly what he means, but you don't have a good feeling about it.",
        "You tell him you'll pay the extra mileage.",
        "He grumbles but nods. You quickly hop into the back seat."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You watch the drive anxiously out the window, gripping your keys tightly.",
        "You keep catching yourself looking at the driver in the rearview mirror.",
        "The car smells vaguely like stale bread.",
        "Finally, you make it home. You wave vaguely at the driver and hurry in.",
        " You can feel his eyes on your back."
    ], HEIGHT // 3)
    curtains_are_open()

def call_driver():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You dial the number your friend sent you.",
        "The driver doesn't react at all.",
        "You get a sinking feeling and slowly back up.",
        "The driver is looking right at you from the shadowed driver's seat.",
        "Before you can react, someone else appears behind you. The follower from the store."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You're in the car before you know it.",
        "Game over, {player_name}."
    ], HEIGHT // 3)
    game_over

def license_plate():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You move quickly to check the license plate.",
        "It doesn't match.",
        "There's a similar colored car across the street, though, and you carefully cross to check it.",
        "The driver is looking right at you from the shadowed driver's seat.",
        "Before you can react, someone else appears behind you. The follower from the store."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You're in the car before you know it.",
        "Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def cashier_police():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The cashier looks at you skeptically.",
        "[Cashier] What for? You thinking of killing someone or something?",
        "You smile nervously. How do you approach this to get him to take you seriously?"
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    draw_choices([
        "1 - Tell him you think a stranger is following you."
        "2 - Lie and tell him you think an ex-boyfriend is following you."
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    
    if choice == "1":
        cashier_stranger()
    elif choice == "2":
        cashier_ex()

def cashier_stranger():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The cashier glances at the person in the back of the store.",
        "[Cashier] That guy? Don't you have a phone? Whatever, as long as I'm not in trouble.",
        "He dials the number and tells the person who answers that you need a safe ride home.",
        "Somewhere in the conversation, the follower disappears out a side door.",
        "A couple of officers show up. After taking a report, they tell you they can't do much.",
        "But they'll give you a ride home.",
        "You eventually make it to your front door after an awkward car ride."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    curtains_are_open()


def cashier_ex():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The cashier laughs.",
        "Right in your face.",
        "[Cashier] Dude, I'm not getting in the middle of that. That's your business.",
        "It feels like a slap in the face. You can see there's no convincing him.",
        "You take a shaky breath. You need to regroup."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    gas_station_nohelp()
    

def lock_bathroom():
    surface.fill(BLACK)
    typewriter_paragraph([
        "The bathroom is in a back hallway.",
        "You take a deep breath and hurry towards it, glancing over your shoulder.",
        "The follower is slowly moving towards you.",
        "Quickly, you duck into the bathroom and pull the door shut.",
        "But at the last second a foot catches the door."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "There's a back doorway out of sight of the cashier.",
        "You're gone and the cashier doesn't even see you go."
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def pretend_shop():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You quickly move towards a center aisle.",
        "You pretend to inspect a pack of expired PopTarts.",
        "You don't hear the cashier leave to go to the back of the store.",
        "And you don't hear your follower until he's already too close.",
        "There's no one to see you get dragged away."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over() 

def street_light():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You pick your way across the street between trash cans and parked cars.",
        "There's one flickering streetlight. You can hear the electricity humming through it.",
        "You don't even hear the follower approach until they call your name from a few feet away.",
        "Apparently the street light has acted a little more like a spotlight than a deterrent."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    name_play_along

def alley():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You hurry towards the alleyway, checking over your shoulder every few seconds.",
        "It's dark.",
        "You can see a brighter street at the other end.",
        "But halfway through you hear a shuffling noise.",
        "The follower appears from an intersecting alley you hadn't even seen mere feet away from you."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def loop_back():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You hesitate for a minute but cut back towards the house.",
        "You know where you're going and you move quickly.",
        "It turns out that someone else knows where you're going too.",
        "You don't even have a chance to scream."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def first_shortcut():
    global told_someone  
    surface.fill(BLACK)
    typewriter_paragraph([
        "There are footsteps behind you.",
        "You don't want to be rude and look behind you.",
        "But there's a reflection in a nearby store window. It's still there two streets later." 
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    surface.fill(BLACK)
    typewriter_paragraph([
        "You don't want to be presumptuous.",
        "But it seems like they're following you."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    # Build the choices list dynamically
    choices = [
        "1 - Zig zag through side streets. Maybe you'll lose them.",
        "2 - Cross the street and slow down to wave at the person. Maybe acknowledging them will spook them.",
        "3 - Call a family member. Just to be on the phone with someone.",  # placeholder for option 3
    ]

    if told_someone:
        choices[3] = "4 - Call the friend you told you were leaving earlier. Maybe they'll help."

    draw_choices(choices)
    pygame.display.update()

    # Build valid keys based on available options
    valid_keys = ["1", "2", "3"]
    if told_someone:
        valid_keys.append("4")

    choice = wait_for_key(valid_keys=valid_keys)

    if choice == "1":
        zig_zag()
    elif choice == "2":
        acknowledged_follower()
    elif choice == "3":
       call_family()
    elif choice == "4" and told_someone: 
        call_friend()

def call_family():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You pull your phone out to start dialing.",
        "But you take your eyes off of your surroundings.",
        "He's quiet. You don't even hear him approach.",
        "There's no time to scream."
    ], HEIGHT // 3)
    surface.fill(BLACK)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()


def call_friend():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You keep your eyes on the follower. They've stopped across the street.",
        "You call your friend. They can be there in five.",
        "You just need to stay safe and calm until they're there."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    draw_choices([
        "1 - Duck into a nearby gas station. You can see the profile of a cashier inside.",
        "2 - Move under a street light and wait for your friend.",
        "",
        ""

    ], HEIGHT // 3)
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    if choice == "1":
        gas_station()
    elif choice == "2":
        street_light() 

def acknowledged_follower():
    surface.fill(BLACK)
    typewriter_paragraph([
        "They wave back, but they don't stop there.",
        "You see them crossing the street towards you. Maybe you know them.",
        "Either way, you're too nervous to start moving away.",
        "It's a person in a hoodie and they call your name cheerfully as they approach.",
        "Their hood casts a shadow over their face."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You can't place this person. In fact, you're pretty sure you've never met.",
        "But there's some intense gleam in their eye",
        "that makes you second guess responding in confusion."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Tell them they must have confused you with someone else- ",
        "that's not your name.",
        "2 - Pretend you recognize them too. [You] Hey! Long time no see!"
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    if choice == "1":
        play_dumb_over()
    elif choice == "2":
        name_play_along()

def play_dumb_over():
    surface.fill(BLACK)
    typewriter_paragraph([
        "Their stare intensifies. They look disappointed, but not for themself-",
        "They look upset... like they think you're lying to them.",
        "[Follower] You're a liar.",
        "They're going to make sure you know that."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def name_play_along(): 
    surface.fill(BLACK)
    typewriter_paragraph([
        "They grin at you.",
        "It's unsettling.",
        "[Follower] I can't believe I'm running into you like this!",
        "[Follower] What are the chances? I lost your number.",
        "[Follower] I've been meaning to try and get it again."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You're almost certain you've never met this person before in your life.",
        "But they sound so sincere.",
        "Their smile is unsettlingly intense."
    ], HEIGHT // 3)
    pygame.display.update()
    draw_choices([
        "1 - Give them a fake phone number. Use the right area code so they're not suspicious.",
        "2 - Maybe you're just misplacing them. Or they're unwell.",
        "Either way, what would they do with your phone number? Give it to them."
        "",  
        ""
    ])
    pygame.display.update()
    valid_keys = ["1", "2"] 
    choice = wait_for_key(valid_keys=valid_keys)
    if choice == "1":
        fake_phone_number()
    elif choice == "2":
        real_phone_number()
    
def fake_phone_number():
    surface.fill(BLACK)
    typewriter_paragraph([
        "They punch the number into their phone as casually as can be.",
        "[Follower] Let me just make sure I got it right.",
        "...",
        "...",
        "[Follower] I'd ask you why your phone isn't ringing.",
        "But I know it's because you're a liar."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def real_phone_number():
    surface.fill(BLACK)
    typewriter_paragraph([
        "They punch in your number into their phone as casually as can be.",
        "They keep looking up to smile at you.",
        "[Follower] I'm so glad I ran into you— you have no idea.",
        "[Follower] Let's catch up soon, okay?",
        "You watch them as they wave goodbye, crossing the street away from you."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    surface.fill(BLACK)
    typewriter_paragraph([
        "You feel unsettled.",
        "How do they know you gave them the right phone number?",
        "You get the feeling it wouldn't have gone well if they thought you were lying.",
        "You should get home. You pick up the pace.",
        "Finally, you reach your front door and fumble for your keys.",
        "As you step inside, you let out a deep breath."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    draw_choices([
        "1 - You still don't feel quite right.",
        "The follower was too familiar with you. Check the house, just in case.",
        "2 - Call someone to report the follower. You're sure you didn't know them.",
        "3 - Call someone in the morning just in case. They were creepy, but harmless. For now, get some sleep.",
    ])
    pygame.display.update()

    valid_keys = ["1", "2", "3"]
    choice = wait_for_key(valid_keys=valid_keys)

    if choice == "1":
        curtains_are_open()
    elif choice == "2":
        report_tonight()
    elif choice == "3":
        report_morning()

def curtains_are_open():
    surface.fill(BLACK)
    typewriter_paragraph([
        "As you carefully pick your way through the apartment, you see something moving out of the corner of your eye.",
        "The living room curtains are moving.",
        "As you move closer, you see that a soft breeze from an open window is the culprit."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    surface.fill(BLACK)
    typewriter_paragraph([
        "You don't think you left that window open.", 
        "But everything has been stressful lately and you've been scatterbrained.",
        "You're not even sure you were followed, exactly."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    draw_choices([
        "1 - Close the window and head to bed.",
        "You don't want to waste anyone's time or money on your paranoia.",
        "2 - Close the window and draw the curtains. Call someone for help. Just in case.",
        "3 - Slowly back away from the window. Call someone for help, but keep your eyes on it."
    ])
    pygame.display.update()
    valid_keys = ["1", "2", "3"]
    choice = wait_for_key(valid_keys=valid_keys)
    if choice == "1":
        curtains_are_open()
    elif choice == "2":
        report_tonight()
    elif choice == "3":
        game_passed()

def report_tonight():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You pull your phone out to start dialing.",
        "But you take your eyes off of your surroundings."
        "They're quiet when they enter your house."
    ], HEIGHT // 3)
    surface.fill(BLACK)
    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)
    game_over()

def report_morning():
    surface.fill(BLACK)
    typewriter_paragraph([
        "You're a little freaked out, sure.",
        "It would be good to talk to someone in the morning and see if you can figure out what happened.",
        "You'll make sure you talk to friends and a professional."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    typewriter_paragraph([
        f"Game over, {player_name}."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    surface.fill(BLACK)
    typewriter_paragraph([
        "You went to sleep.",
        "But you didn't realize the living room window was open.",
        "They entered your apartment quietly. It didn't even wake you up."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    game_over()

   

def game_over(reason="Game Over"):
    surface.fill(BLACK)
    typewriter_paragraph(["You Lost."], HEIGHT // 3)
    draw_choices([
        "1 - Play again",
        "2 - Exit",
        "", ""
    ])
    pygame.display.update()
    choice = wait_for_key(valid_keys=["1", "2"])
    if choice == "1":
        start_the_game()  # restart from main game
    else:
        thank_you()

def thank_you():
    surface.fill(BLACK)
    typewriter_paragraph([
        "This is just a video game...",
        "But stalking affects real people every day.",
        "Repeated, unwanted contact or following of any form—even if someone never reports it—",
        "Can really scare people.",
        "One in every three women and one in every six men experience stalking.",
        "Let's make stalking a fictional problem."
    ], HEIGHT // 3)
    pygame.display.update()
    pygame.time.delay(3500)

    # Font and link setup
    font = pygame.font.SysFont(None, 36)

    links = [
        ("RAINN (Sexual Assault & Stalking Support)", "https://www.rainn.org/", (0, 150, 255), (100, 200, 255)),
        ("Stalking Prevention Awareness & Resource Center", "https://www.stalkingawareness.org/", (0, 150, 255), (100, 200, 255)),
        ("Don't Call The Police - Community-Based Alternatives", "https://dontcallthepolice.com/", (0, 150, 255), (100, 200, 255)),
        ("Quit Game", "QUIT", (200, 50, 50), (255, 100, 100))
    ]

    link_rects = []

    while True:
        surface.fill(BLACK)

        mouse_pos = pygame.mouse.get_pos()
        link_rects.clear()

        for i, (text, action, base_color, hover_color) in enumerate(links):
            is_hovered = False
            temp_text = font.render(text, True, base_color)
            temp_rect = temp_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))

            if temp_rect.collidepoint(mouse_pos):
                is_hovered = True
                rendered_text = font.render(text, True, hover_color)
            else:
                rendered_text = font.render(text, True, base_color)

            surface.blit(rendered_text, temp_rect)
            link_rects.append((temp_rect, action))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in link_rects:
                    if rect.collidepoint(event.pos):
                        if action == "QUIT":
                            pygame.quit()
                            sys.exit()
                        else:
                            webbrowser.open(action)


def game_passed():
    surface.fill(BLACK)
    typewriter_paragraph(["The authorities arrive just in time to detain a man right outside your house.",
                          "You made it."], HEIGHT // 3)
    draw_choices([
        "1 - Play again",
        "2 - Exit",
        "", ""
    ])
    pygame.display.update()
    choice = wait_for_key(valid_keys=["1", "2"])
    if choice == "1":
        start_the_game()  # restart from main game
    else:
        thank_you()


# Home Menu (Fixed Centered Title)
mainmenu = pygame_menu.Menu("", WIDTH, HEIGHT, theme=custom_theme)
mainmenu.add.label("A Walk Home", font_size=50, font_color=WHITE, align=pygame_menu.locals.ALIGN_CENTER)
mainmenu.add.text_input('Name: ', default='', maxchar=20, textinput_id='name_input')
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

# ✅ Main Menu Loop
mainmenu.mainloop(surface)

