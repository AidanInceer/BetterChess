l_merge = list(zip([90 for _ in range(34)], [80 for _ in range(34)]))
flat_list = [item for sublist in l_merge for item in sublist]
game_move_acc = flat_list.append(90)
print(flat_list)
