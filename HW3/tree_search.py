import random

def main():
    # A self defined undirected graph
    adjacent = [
        [1, 2, 3, 4],
        [0, 2],
        [0, 1, 5],
        [0],
        [0, 5],
        [2, 4]
    ]

    def tree_search(init_node, target):
        print('Initiating Tree-Search algoirhtm...')
        frontier = [*adjacent[init_node]]
        i = 0
        while frontier:
            i += 1
            print(f'Current iteration: {i}')
            print(f'Current frontier: {frontier}')
            random.shuffle(frontier)
            to_be_expanded = frontier.pop()
            print(f'Chosen node: {to_be_expanded}\n')
            if to_be_expanded == target:
                print('Target found.')
                return True
            frontier += adjacent[to_be_expanded]
        print('Target not found.')
        return False
    
    print('Adjacent List of given graph: ')
    print(adjacent)
    print('Starting at node 0, find node 5.\n')
    tree_search(0, 5)

if __name__ == '__main__':
    main()