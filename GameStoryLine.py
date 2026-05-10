
def print_storyline(text):
    """Displays a paragraph and waits for the user to press Enter."""
    print(text)
    input("\nPress enter to continue...\n")

def main():

    print_storyline( 
        "A famous historical figure who was remembered in the mortal world for his influence, ambition, and power met his inevitable death a long time ago.\n"
        "However, his story did not end with death."
    )

    print_storyline(
        "He woke up in the depths of the Underground, a place of never-ending hallways, flaming skies, and loud screams, rather than quietly entering the afterlife.\n"
        "This was no ordinary afterlife.\n"
        "The Labyrinth was a twisted realm that served as both a prison and a testing ground."
    )

    print_storyline(
        "Hades, the ruler of the underworld and creator of endless punishment, sits at its core.\n"
        "The purpose of the Labyrinth is to test and confine the cursed.\n"
        "Every floor is an experiment.\n"
        "Every shade conceals a regretful and sinful memory." 
    ) 

    print_storyline(
        "The protagonist soon discovers a harsh reality:\n"
        "No door is visible. No compassion. No redemption."
    )

    print_storyline(
        "Fighting is the only way ahead."
    )

    print_storyline(
        "He must defeat the creatures that serve Hades's will in order to reach each floor:\n"
        "Wraiths bound by despair, Hellhounds formed in fire, Fallen Angels devoured by pride, and Imps born of curses.\n"
        "The opposition gets more intense the farther he goes, as though the Labyrinth itself feels defiance."
    )

    print_storyline(
        "Whispers circulated among the imprisoned souls:\n"
        "The Labyrinth will crumble if Hades falls." 
    )

    print_storyline(
        "Because Hades is the central figure that unites the realm, he is more than just a king.\n"
        "The Underground will collapse if he is vanquished.\n"
        "The never-ending cycle of suffering will end.\n"
        "The souls incarcerated will be freed from their never-ending agony."
    )

    print_storyline(
        "All of the spirits will be reincarnated into the mortal world at that collapse."
    )

    print_storyline(
        "But the Labyrinth's design includes a darker law:"
    )

    print_storyline(
        "The cycle is restarted if Hades is replaced on his throne by another soul.\n"
        "The world becomes stable.\n"
        "The pain is still present."
    )

    print_storyline(
        "Even still, the souls will still be reincarnated when the balance is changed;\n"
        "their memories will be vanished their destinies will be changed, and their previous lives will only exist in dreams."
    )

    print_storyline(
        "Victory in the depths of Hades Labyrinth involves more than just getting out.\n"
        "Every soul imprisoned in the Underground has its destiny decided by it."
    )

    print("And maybe the destiny of history itself.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame description interrupted.")
   