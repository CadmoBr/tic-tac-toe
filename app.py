import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Jogo da Velha", layout="centered")

# Inicializar estado do jogo
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
if "current_player" not in st.session_state:
    st.session_state.current_player = "X"
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "scores" not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0, "draw": 0}
if "game_mode" not in st.session_state:
    st.session_state.game_mode = "human"  # "human" ou "bot"

def check_winner(board):
    """Verifica vencedor"""
    # Linhas
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]
    # Colunas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]
    # Diagonais
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    # Empate
    if all(cell != "" for row in board for cell in row):
        return "draw"
    return None

def reset_game():
    """Reseta o jogo"""
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None

def bot_move():
    """Movimento simples do bot (aleatório com bloqueio básico)"""
    empty_cells = [(r, c) for r in range(3) for c in range(3) if st.session_state.board[r][c] == ""]
    if empty_cells:
        return random.choice(empty_cells)
    return None

# Título
st.title("🎮 Jogo da Velha")
