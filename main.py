from pathlib import Path

from quizmaster import (
    JsonStorage,
    Leaderboard,
    Player,
    Question,
    Quiz,
)


DATA_FILE = Path(__file__).parent / "data" / "leaderboard.json"


def create_questions() -> list[Question]:
    """Create the question bank."""

    return [
        Question(
            "What is the capital of Thailand?",
            ["Bangkok", "Tokyo", "Seoul", "Beijing"],
            "A",
            "Geography",
            "Easy",
        ),
        Question(
            "What is the chemical symbol for gold?",
            ["Ag", "Fe", "Au", "Cu"],
            "C",
            "Science",
            "Medium",
        ),
        Question(
            "Which planet is closest to the Sun?",
            ["Venus", "Earth", "Mars", "Mercury"],
            "D",
            "Science",
            "Hard",
        ),
        Question(
            "What is the largest ocean on Earth?",
            ["Atlantic", "Indian", "Pacific", "Arctic"],
            "C",
            "Geography",
            "Easy",
        ),
        Question(
            "Which gas do plants absorb during photosynthesis?",
            ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"],
            "B",
            "Science",
            "Medium",
        ),
        Question(
            "What is the square root of 144?",
            ["10", "11", "12", "14"],
            "C",
            "Mathematics",
            "Easy",
        ),
        Question(
            "What is the derivative of x squared?",
            ["x", "2x", "x squared", "2"],
            "B",
            "Mathematics",
            "Hard",
        ),
        Question(
            "Which country is home to the city of Kyoto?",
            ["China", "South Korea", "Japan", "Thailand"],
            "C",
            "Geography",
            "Medium",
        ),
        Question(
            "How many sides does a hexagon have?",
            ["Five", "Six", "Seven", "Eight"],
            "B",
            "Mathematics",
            "Easy",
        ),
        Question(
            "Which organelle is responsible for producing ATP?",
            ["Nucleus", "Ribosome", "Mitochondrion", "Golgi apparatus"],
            "C",
            "Science",
            "Hard",
        ),
        Question(
            "What is the capital of Australia?",
            ["Sydney", "Melbourne", "Canberra", "Perth"],
            "C",
            "Geography",
            "Medium",
        ),
        Question(
            "What is 15 multiplied by 8?",
            ["100", "110", "120", "130"],
            "C",
            "Mathematics",
            "Medium",
        ),
    ]


def ask_name() -> str:
    """Ask for a valid player name."""

    while True:
        name = input("Enter your name: ").strip()

        if name:
            return name

        print("Name cannot be empty. Please try again.")


def choose_option(title: str, options: list[str]) -> str:
    """Display numbered options and return the player's choice."""

    print(f"\n{title}")

    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")

    while True:
        choice = input("Choose an option: ").strip()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(options):
                return options[number - 1]

        print(f"Please enter a number from 1 to {len(options)}.")


def ask_question(
    quiz: Quiz,
    question: Question,
    player: Player,
    number: int,
) -> None:
    """Display a question, collect an answer, and update the score."""

    letters = ["A", "B", "C", "D"]

    print(f"\n{'-' * 45}")
    print(f"Question {number}: {question.text}")
    print(f"Category: {question.category}")
    print(f"Difficulty: {question.difficulty}")
    print(f"Points available: {question.points}")
    print()

    for letter, option in zip(letters, question.options):
        print(f"{letter}. {option}")

    while True:
        answer = input("\nYour answer (A/B/C/D): ").strip().upper()

        if answer in letters:
            break

        print("Invalid answer. Enter A, B, C, or D.")

    if quiz.play_question(question, answer, player):
        print(f"Correct! +{question.points} points.")
    else:
        print(f"Incorrect! The correct answer was {question.correct_answer}.")

    print(f"Your current score: {player.score}")


def display_leaderboard(leaderboard: Leaderboard) -> None:
    """Display the highest-scoring players."""

    print("\n========== LEADERBOARD ==========")

    top_players = leaderboard.top_players(5)

    if not top_players:
        print("No scores recorded yet.")
        return

    for rank, player in enumerate(top_players, start=1):
        print(f"{rank}. {player.name} - {player.score} points")


def main() -> None:
    """Run the QuizMaster application."""

    storage = JsonStorage(DATA_FILE)
    leaderboard = Leaderboard(storage.load_players())

    quiz = Quiz(create_questions())

    print("=" * 45)
    print("           WELCOME TO QUIZMASTER")
    print("=" * 45)

    player = Player(ask_name())

    print(f"\nWelcome, {player.name}!")

    categories = sorted({question.category for question in quiz.questions})
    category = choose_option(
        "Choose a category:",
        ["All Categories"] + categories,
    )

    if category == "All Categories":
        category = None

    available_questions = quiz.select_questions(category=category)

    difficulties = sorted(
        {question.difficulty for question in available_questions}
    )

    difficulty = choose_option(
        "Choose a difficulty:",
        ["All Difficulties"] + difficulties,
    )

    if difficulty == "All Difficulties":
        difficulty = None

    available_questions = quiz.select_questions(
        category=category,
        difficulty=difficulty,
    )

    amount_options = [
        str(number)
        for number in range(1, len(available_questions) + 1)
    ]

    amount = int(
        choose_option(
            f"How many questions? (Available: {len(available_questions)})",
            amount_options,
        )
    )

    print("\n========== LET'S START ==========")
    print("Easy = 1 point | Medium = 2 points | Hard = 3 points")

    questions = quiz.iter_questions(
        category=category,
        difficulty=difficulty,
        amount=amount,
    )

    for number, question in enumerate(questions, start=1):
        ask_question(quiz, question, player, number)

    print("\n" + "=" * 45)
    print("              QUIZ COMPLETED")
    print("=" * 45)
    print(f"Player: {player.name}")
    print(f"Final score: {player.score} points")

    leaderboard.add_player(player)

    if storage.save_players(leaderboard.players):
        print("Your score has been saved.")
    else:
        print("Warning: Your score could not be saved.")

    display_leaderboard(leaderboard)


if __name__ == "__main__":
    main()