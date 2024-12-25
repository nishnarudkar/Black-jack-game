import random
import streamlit as st

# Function to deal cards
def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

# Function to calculate the score
def calculate_score(cards):
    total = sum(cards)
    if total == 21 and len(cards) == 2:  # Blackjack check
        return 0  # Blackjack has a special value of 0 in the comparison function

    if 11 in cards and total > 21:  # Adjust for Ace
        cards.remove(11)
        cards.append(1)

    return sum(cards)

# Function to compare scores
def compare(u_score, c_score):
    if u_score == c_score:
        return "🤝 It's a Draw!"
    elif c_score == 0:
        return "💻 Computer Wins with a Blackjack!"
    elif u_score == 0:
        return "🎉 You Win with a Blackjack!"
    elif u_score > 21:
        return "💻 Computer Wins! You busted 😢"
    elif c_score > 21:
        return "🎉 You Win! Computer busted 💥"
    elif u_score > c_score:
        return "🎉 You Win! 🏆"
    else:
        return "💻 Computer Wins! Better luck next time 🤖"

# Function to initialize game state
def reset_game():
    st.session_state["user_cards"] = [deal_card(), deal_card()]
    st.session_state["computer_cards"] = [deal_card(), deal_card()]
    st.session_state["is_game_over"] = False

# Main function
def main():
    # Title and header
    st.title("🃏 Blackjack Game 🎲")
    st.markdown(
        """
        <div style="background-color:#FFC300; padding:10px; border-radius:10px;">
            <h3 style="color:#333333; text-align:center;">Welcome to the Classic Game of Blackjack!</h3>
            <p style="text-align:center;">Try to beat the computer by getting closer to 21 without going over. Good luck! 🍀</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state
    if "user_cards" not in st.session_state:
        reset_game()

    user_cards = st.session_state["user_cards"]
    computer_cards = st.session_state["computer_cards"]
    is_game_over = st.session_state["is_game_over"]

    # Calculate scores
    user_score = calculate_score(user_cards)
    computer_score = calculate_score(computer_cards)

    # Display user cards and score
    st.subheader("🎴 Your Cards")
    st.write(f"🃏 **Your Hand:** {user_cards}")
    st.write(f"💯 **Your Score:** {user_score}")

    # Display computer's first card
    st.subheader("💻 Computer's Cards")
    st.write(f"🃏 **Computer's First Card:** {computer_cards[0]}")

    # Game logic
    if not is_game_over:
        if user_score == 0 or computer_score == 0 or user_score > 21:
            st.session_state["is_game_over"] = True
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🎯 Hit (Get another card)"):
                    user_cards.append(deal_card())
                    st.session_state["user_cards"] = user_cards
            with col2:
                if st.button("🛑 Stand (End your turn)"):
                    st.session_state["is_game_over"] = True

    if st.session_state["is_game_over"]:
        # Computer's turn
        while computer_score != 0 and computer_score < 17:
            computer_cards.append(deal_card())
            computer_score = calculate_score(computer_cards)

        # Display final results
        st.subheader("📊 Final Results")
        st.write(f"🎴 **Your Final Hand:** {user_cards}, **Final Score:** {user_score}")
        st.write(f"💻 **Computer's Final Hand:** {computer_cards}, **Final Score:** {computer_score}")
        result = compare(user_score, computer_score)
        st.markdown(
            f"""
            <div style="background-color:#D4F1F4; padding:15px; border-radius:10px; text-align:center;">
                <h2>{result}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Restart option
        if st.button("🔄 Restart Game"):
            reset_game()

# Run the app
if __name__ == "__main__":
    main()
