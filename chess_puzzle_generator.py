# some generated puzzles
# 6q1/4Q1B1/4p3/n4knr/p1B5/2KR4/3N4/R2b2q1 w - - 0 1
# 7k/2bP1P2/6P1/P1N1pQnN/R4P2/1R3p2/2P1n1p1/K2q4 w - - 0 1
# k4B2/b7/1n4P1/4Q3/4qK2/P2pP3/1prb3R/8 w - - 0 1
# 1R3R1r/3QK3/8/4b2k/2n2r2/B5p1/q1pb2Bp/1n6 w - - 0 1
# 7N/p3P1P1/B7/3K3p/k1p4P/3N2p1/n6q/1B1rRR2 w - - 0 1

import random

import chess
import chess.engine

POPULATION_SIZE = 100


with open("stockfish_path.txt", "r") as f:
    stockfish_path = f.read().strip()

if not stockfish_path:
    print("Please provide the path for Stockfish engine in 'stockfish_path.txt'")
    exit()

engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
# engine = chess.engine.SimpleEngine.popen_uci(r"D:\Project\stockfish\stockfish-windows-x86-64-avx2.exe")

print("More Depth! More Fun! And More time to Generate Puzzle!")
max_stockfish_depth_input = int(input(f"Enter the maximum depth for Stockfish analysis (recommended 20) : "))

file_path = input("File Path to store puzzles : ")

try:
    file = open(file_path,"a")
except:
    print("Invalid Path")
    engine.quit()
    exit(0)

class Individual:
    def __init__(self,board : chess.Board = None):
        self.board = board
        if not board:
            self.board = self.random_board()
        self.fitness = self.calculate_fitness(engine)

    def random_square(self):
        x = random.randint(0,7)
        y = random.randint(0,7)
        square = chess.square(x, y)
        return square

    def place_random_peice(self,board : chess.Board,color,peice,n):
        k = random.randint(0,n)
        for i in range(k):
            square = self.random_square()
            board.set_piece_at(square, chess.Piece(peice, color))

    def random_board_c(self,color,board : chess.Board):
        # generate a random board and put color pieces at random positions
        q = 1
        b = 2
        r = 2
        n = 2
        p = 8

        self.place_random_peice(board,color,chess.ROOK,r)
        self.place_random_peice(board,color,chess.BISHOP,b)
        self.place_random_peice(board,color,chess.KNIGHT,n)
        self.place_random_peice(board,color,chess.QUEEN,q)

        square = self.random_square()
        board.set_piece_at(square, chess.Piece(chess.KING, color))

        r = random.randint(0,p)
        for i in range(r):
            x = random.randint(0,7)
            y = random.randint(1,6)
            square = chess.square(x, y)
            board.set_piece_at(square, chess.Piece(chess.PAWN, color))

    def random_board(self):
        board = chess.Board(None)
        self.random_board_c(chess.WHITE,board)
        self.random_board_c(chess.BLACK,board)
        return board

    def place_piece(self,board : chess.Board,w_pieces,b_pieces,color,piece):
        arr = w_pieces + b_pieces
        # n = random.randint(0,len(arr))
        if color == chess.BLACK:
            m = max (len(w_pieces),len(b_pieces))
            n = random.randint(int(m/2),m)
        else:
            n = random.randint(0,max(len(w_pieces),len(b_pieces)))
        if not len(arr):
            return
        selected = random.sample(arr,n)
        for sq in selected:
            board.set_piece_at(sq, chess.Piece(piece, color))

    def mate(self,board : chess.Board):
        # producing a child from two parent
        white_pawns_1 = self.board.pieces(chess.PAWN, chess.WHITE)
        white_knight_1 = self.board.pieces(chess.KNIGHT, chess.WHITE)
        white_bishop_1 = self.board.pieces(chess.BISHOP, chess.WHITE)
        white_rook_1 = self.board.pieces(chess.ROOK, chess.WHITE)
        white_queen_1 = self.board.pieces(chess.QUEEN, chess.WHITE)
        white_king_1 = self.board.pieces(chess.KING, chess.WHITE)

        black_pawns_1 = self.board.pieces(chess.PAWN, chess.BLACK)
        black_knight_1 = self.board.pieces(chess.KNIGHT, chess.BLACK)
        black_bishop_1 = self.board.pieces(chess.BISHOP, chess.BLACK)
        black_rook_1 = self.board.pieces(chess.ROOK, chess.BLACK)
        black_queen_1 = self.board.pieces(chess.QUEEN, chess.BLACK)
        black_king_1 = self.board.pieces(chess.KING, chess.BLACK)

        white_pawns_2 = board.pieces(chess.PAWN, chess.WHITE)
        white_knight_2= board.pieces(chess.KNIGHT, chess.WHITE)
        white_bishop_2 = board.pieces(chess.BISHOP, chess.WHITE)
        white_rook_2 = board.pieces(chess.ROOK, chess.WHITE)
        white_queen_2 = board.pieces(chess.QUEEN, chess.WHITE)
        white_king_2 = board.pieces(chess.KING, chess.WHITE)

        black_pawns_2 = board.pieces(chess.PAWN, chess.BLACK)
        black_knight_2 = board.pieces(chess.KNIGHT, chess.BLACK)
        black_bishop_2 = board.pieces(chess.BISHOP, chess.BLACK)
        black_rook_2 = board.pieces(chess.ROOK, chess.BLACK)
        black_queen_2 = board.pieces(chess.QUEEN, chess.BLACK)
        black_king_2 = board.pieces(chess.KING, chess.BLACK)

        new_board = chess.Board(None)
        self.place_piece(new_board,list(white_pawns_1),list(white_pawns_2),chess.WHITE,chess.PAWN)
        self.place_piece(new_board,list(white_knight_1),list(white_knight_2),chess.WHITE,chess.KNIGHT)
        self.place_piece(new_board,list(white_bishop_1),list(white_bishop_2),chess.WHITE,chess.BISHOP)
        self.place_piece(new_board,list(white_rook_1),list(white_rook_2),chess.WHITE,chess.ROOK)

        self.place_piece(new_board, list(black_pawns_1), list(black_pawns_2), chess.BLACK, chess.PAWN)
        self.place_piece(new_board, list(black_knight_1), list(black_knight_2), chess.BLACK, chess.KNIGHT)
        self.place_piece(new_board, list(black_bishop_1), list(black_bishop_2), chess.BLACK, chess.BISHOP)
        self.place_piece(new_board, list(black_rook_1), list(black_rook_2), chess.BLACK, chess.ROOK)

        w_k = list(white_king_1) + list(white_king_2)
        w_q = list(white_queen_1) + list(white_queen_2)
        b_k = list(black_king_1) + list(black_king_2)
        b_q = list(black_queen_1) + list(black_queen_2)
        if len(w_k):
            p1 = random.choice(w_k)
            new_board.set_piece_at(p1, chess.Piece(chess.KING, chess.WHITE))
        if len(b_k):
            p2 = random.choice(b_k)
            new_board.set_piece_at(p2, chess.Piece(chess.KING, chess.BLACK))

        if len(w_q):
            pq1 = random.choice(w_q)
            new_board.set_piece_at(pq1, chess.Piece(chess.QUEEN, chess.BLACK))
        if len(b_q):
            pq2 = random.choice(b_q)
            new_board.set_piece_at(pq2, chess.Piece(chess.QUEEN, chess.BLACK))
        return new_board

    def add_random_piece(self,board: chess.Board, color):
        # add a random piece at random position
        piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP,
                       chess.ROOK, chess.QUEEN, chess.KING]
        random.shuffle(piece_types)

        for piece_type in piece_types:
            count = len(board.pieces(piece_type, color))

            if piece_type == chess.KING and count >= 1:
                continue
            elif piece_type == chess.PAWN and count >= 8:
                continue
            elif piece_type == chess.QUEEN and count >= 1:
                continue
            elif piece_type == chess.KNIGHT and count >= 2:
                continue
            elif piece_type == chess.BISHOP and count >= 2:
                continue
            elif piece_type == chess.ROOK and count >= 2:
                continue


            empty_squares = [sq for sq in chess.SQUARES if board.piece_at(sq) is None]
            if not empty_squares:
                return
            if piece_type == chess.PAWN:
                empty_squares = [sq for sq in empty_squares if chess.square_rank(sq) not in (0, 7)]


            sq = random.choice(empty_squares)
            board.set_piece_at(sq, chess.Piece(piece_type, color))
            return

    def move_random_peice(self, board: chess.Board):
        # moves a random piece
        pieces = [sq for sq in chess.SQUARES if board.piece_at(sq)]
        if not pieces:
            return
        from_sq = random.choice(pieces)
        piece = board.piece_at(from_sq)
        to_sq = random.choice([sq for sq in chess.SQUARES if sq != from_sq])
        board.remove_piece_at(from_sq)
        board.set_piece_at(to_sq, piece)

    def mated_gene(self,board : chess.Board):
        new_board = self.mate(board)
        p = random.randint(0,100)
        if p < 70:
            for _ in range(random.randint(1, 10)):
                    self.move_random_peice(new_board)

        if p < 70:
            if p%2:
                for _ in range(random.randint(1, 5)):
                        self.add_random_piece(new_board,chess.WHITE)
            else:
                for _ in range(random.randint(1,5)):
                    self.add_random_piece(new_board,chess.BLACK)
        return Individual(new_board)

    def material_value(self,board: chess.Board):
        white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
        white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
        white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
        white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
        white_pawns = board.pieces(chess.PAWN, chess.WHITE)
        white_pawns_on_7 = len([sq for sq in white_pawns if chess.square_rank(sq) == 6])

        black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))
        black_rook = len(board.pieces(chess.ROOK, chess.BLACK))
        black_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
        black_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
        black_pawns = len(board.pieces(chess.PAWN, chess.BLACK))

        score = (white_queen - black_queen) * 0.25 + (white_rook - black_rook) * 0.23 + (
            white_bishop + white_knight - black_bishop - black_knight) *0.2 + (len(white_pawns) - black_pawns) * 0.18

        return score + white_pawns_on_7 * 0.27 - (self.pseudo_legal_moves(self.board,chess.BLACK)-self.pseudo_legal_moves(self.board,chess.WHITE))*0.04

    def pseudo_legal_moves(self,board, color):
        original_turn = board.turn
        board.turn = color
        moves = list(board.pseudo_legal_moves)
        board.turn = original_turn
        return len(moves)

    # def calculate_fitness(self,engine):
    #     # total_pieces = len(self.board.piece_map())
    #     white_pieces_len = bin(self.board.occupied_co[chess.WHITE]).count('1')
    #     black_pieces_len = bin(self.board.occupied_co[chess.BLACK]).count('1')
    #     total_pieces = white_pieces_len + black_pieces_len
    #     penalty = 0
    #     if white_pieces_len < 3 or black_pieces_len < 3:
    #         # penalty = 10
    #         penalty = 5
    #     else:
    #         # penalty = len(self.board.piece_map())*0.1
    #         # penalty = (white_pieces_len-black_pieces_len)*0.1
    #         penalty = self.material_value(self.board)
    #         penalty += (white_pieces_len-black_pieces_len)*0.1
    #     if not self.board.is_valid():
    #         return 10 + penalty
    #
    #     # info = engine.analyse(self.board, chess.engine.Limit(depth=20), multipv=2)
    #     info = engine.analyse(self.board, chess.engine.Limit(depth=20), multipv=3)
    #
    #     # If there are no moves (meaning the game is over), return a high penalty
    #     if len(info) < 1:
    #         return 90 + penalty
    #
    #     # Also heavily penalize having only 1 move, puzzles are only interesting
    #     #   if we have a choice to make
    #     if len(info) < 2:
    #         return 8 + penalty
    #     elif len(info) > 10:
    #         return 6 + penalty
    #
    #     penalty += len(info)*0.05
    #
    #
    #     score = info[0]["score"].pov(self.board.turn)
    #
    #     if not score.is_mate() or score.mate() <= 0:
    #         return 6 + penalty
    #
    #     mate_in = score.mate()
    #     if mate_in <= 3:
    #             penalty += 5  # trivial, penalize
    #     elif 4 <= mate_in <= 6:
    #         penalty -= 5  # ideal, reward
    #     elif 5 <= mate_in <= 10:
    #         penalty -= 2  # okay, small reward
    #     else:
    #         penalty += 2
    #
    #     print("mate : " ,score.mate())
    #     second_move_score = info[1]["score"].pov(self.board.turn).score(mate_score=1000)
    #     ss = score.score(mate_score=1000)
    #     diff1 = ss - second_move_score
    #     # if 0 < diff1 < 200:  # small advantage - hard
    #     #     penalty -= 5
    #     if 0 < diff1 < 100:  # small advantage - hard
    #         penalty -= 6
    #     elif 100 <= diff1 < 200:
    #         penalty -= 3
    #
    #     #
    #     if ss > 200:
    #         if (ss - second_move_score) < 100:  # second-best is close
    #             penalty -= 2  # makes puzzle trickier
    #
    #     try:
    #         third_move_score = info[2]["score"].pov(self.board.turn).score(mate_score=1000)
    #         diff2 = second_move_score - third_move_score
    #         if 0 < diff2 < 200:  # small advantage - hard
    #             penalty -= 5
    #     except:
    #         pass
    #
    #     return penalty
    def calculate_fitness(self,engine):
        black_pieces_len = bin(self.board.occupied_co[chess.BLACK]).count('1')
        penalty = 0
        if not self.board.is_valid():
            return 100 + penalty

        penalty -= black_pieces_len * 4

        info10 = engine.analyse(self.board, chess.engine.Limit(depth=15))
        # info20 = engine.analyse(self.board, chess.engine.Limit(depth=20))
        info20 = engine.analyse(self.board, chess.engine.Limit(depth=max_stockfish_depth_input))

        score10 = info10["score"].pov(chess.WHITE).score(mate_score=10000)
        score20 = info20["score"].pov(chess.WHITE)
        mate_score20 = score20.score(mate_score=10000)

        # stockfish says at lower depth about 10 you are loosing but at upon analysis at greater depth
        # maybe 20 it says you are wining
        if score10 < -50 and mate_score20 > 100:  # bigger difference
            penalty -= 40

        if score10 < 0 < mate_score20:
            penalty -= 5

        swing = abs(mate_score20 - score10)
        penalty -= swing / 100

        if len(info10) < 1:
            return 100 + penalty

        # Also heavily penalize having only 1 move puzzles are only interesting
        # if we have a choice to make
        if len(info10) < 2:
            return 80 + penalty

        penalty += len(info10)*0.05

        score = score20

        if not score.is_mate() or score.mate() <= 0:
            return 100 + penalty

        mate_in = score.mate()
        if mate_in <= 3:
            penalty += 20
        elif 4 <= mate_in <= 6:
            penalty -= 30
        elif 6 <= mate_in <= 10:
            penalty -= 20
        else:
            penalty += 20

        # print("mate : " ,score.mate())

        return penalty

    def print(self):
        return self.board.fen()




def Evolution():
    POPULATION_SIZE = 100
    stored_fen = []
    generation = 1
    found = False
    population = []
    print("starting...")

    for _ in range(POPULATION_SIZE):
        gnome = Individual()
        population.append(gnome)

    while not found:
        population = sorted(population,key=lambda x:x.fitness)
        if generation >= 30:
            break

        new_generation = []
        percentage = 20
        s = int(POPULATION_SIZE*percentage/100)

        random_drop = random.randint(0,100)

        # randomly drop the top parent
        # so to avoid convergence at local minima
        if random_drop < 20:
            drop = random.randint(1, 2)
            new_generation.extend(population[drop:s+drop])
        else:
            new_generation.extend(population[:s])

        s = int(((100-percentage)*POPULATION_SIZE)/100)
        for _ in range(s):
            parent1 = random.choice(population[:int(POPULATION_SIZE/2)])
            parent2 = random.choice(population[:int(POPULATION_SIZE/2)])
            child = parent1.mated_gene(parent2.board)
            new_generation.append(child)

        population = new_generation
        fen_ = str(population[0].print())
        print("Generation : ",generation, "FEN : " + fen_ + " Fitness : " ,population[0].fitness/100)
        if fen_ not in stored_fen:
            file.write(str(population[0].print()) + "\n")
            file.flush()
            stored_fen.append(fen_)

        generation += 1

    print("Generation : ",generation, " String : " + str(population[0].print()) + " Fitness : " ,population[0].fitness/100)
    for f in population:
        fen_ = str(f.print())
        if fen_ not in stored_fen:
            stored_fen.append(fen_)
            file.write(fen_ + "\n")
    file.flush()


Evolution()

engine.quit()
file.close()
